from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": False})

import rclpy
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory
import numpy as np
import time
import threading

from isaacsim.core.utils.stage import open_stage
from isaacsim.core.utils.stage import get_current_stage
from isaacsim.core.prims import SingleArticulation
import omni.timeline
import omni.usd


# -----------------------------
# ROS2 SUBSCRIBER NODE
# -----------------------------
class TrajectorySubscriber(Node):

    def __init__(self):
        super().__init__("isaac_trajectory_subscriber")

        self.latest_traj = None
        self.start_time = None

        self.sub = self.create_subscription(
            JointTrajectory,
            "/walker/joint_trajectory",
            self.callback,
            10
        )

        self.get_logger().info("Subscribed to /walker/joint_trajectory")

    def callback(self, msg):
        self.get_logger().info(f"Received trajectory with {len(msg.points)} points")
        self.latest_traj = msg
        self.start_time = time.time()


# -----------------------------
# LOAD SCENE
# -----------------------------
USD_PATH = "/home/proj/RobotAssets/Collected_WalkerS2/s2_v1.usd"

open_stage(USD_PATH)
print("USD loaded")

for _ in range(120):
    simulation_app.update()

timeline = omni.timeline.get_timeline_interface()
timeline.play()

for _ in range(120):
    simulation_app.update()

print("Simulation running")


# -----------------------------
# ROBOT INIT
# -----------------------------
robot_path = "/s2_v1/base_link"

stage = get_current_stage()
prim = stage.GetPrimAtPath(robot_path)

print("Robot prim valid:", prim.IsValid())

robot = None

if prim.IsValid():
    robot = SingleArticulation(robot_path)
    robot.initialize()
    print("Robot initialized")
else:
    print("Robot NOT found — check prim path")


# -----------------------------
# START ROS2
# -----------------------------
rclpy.init()
node = TrajectorySubscriber()

threading.Thread(target=rclpy.spin, args=(node,), daemon=True).start()


# -----------------------------
# EXECUTION LOOP
# -----------------------------
dt = 1.0 / 120.0

while simulation_app.is_running():

    simulation_app.update()

    if robot is not None and node.latest_traj is not None:

        traj = node.latest_traj
        t = time.time() - node.start_time

        points = traj.points
        if len(points) > 0:

            # simple playback (no interpolation yet)
            idx = min(int(t * 30), len(points) - 1)

            q = points[idx].positions

            robot.set_joint_positions(np.array(q))

    time.sleep(dt)


# -----------------------------
# SHUTDOWN
# -----------------------------
rclpy.shutdown()
simulation_app.close()