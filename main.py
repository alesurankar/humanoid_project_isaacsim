from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": False})

import omni.kit.app
import omni.timeline
from isaacsim.core.utils.stage import open_stage, get_current_stage
from isaacsim.core.prims import SingleArticulation
import time
import sys

# -----------------------------
# ENABLE ROS2 BRIDGE (SAFE WAY)
# -----------------------------
app = omni.kit.app.get_app()

# IMPORTANT: correct API (NOT enable_extension)
app.get_extension_manager().set_extension_enabled_immediate(
    "isaacsim.ros2.bridge",
    True
)

print("ROS2 bridge enabled")

# -----------------------------
# LOAD USD
# -----------------------------
USD_PATH = "/home/proj/RobotAssets/Collected_WalkerS2/s2_v1.usd"

open_stage(USD_PATH)

for _ in range(120):
    simulation_app.update()

timeline = omni.timeline.get_timeline_interface()
timeline.play()

for _ in range(120):
    simulation_app.update()

# -----------------------------
# ROBOT
# -----------------------------
robot_path = "/s2_v1/base_link"

stage = get_current_stage()
prim = stage.GetPrimAtPath(robot_path)

robot = None

if prim.IsValid():
    robot = SingleArticulation(robot_path)
    robot.initialize()
    print("Robot ready")

else:
    print("Robot not found")
    simulation_app.close()
    exit()

# -----------------------------
# MAIN LOOP (NO ROS YET)
# -----------------------------
print("Running simulation...")

while simulation_app.is_running():
    simulation_app.update()

    # TEMP TEST MOTION (IMPORTANT DEBUG STEP)
    if robot:
        import numpy as np
        robot.set_joint_positions(np.zeros(len(robot.dof_names)))

simulation_app.close()