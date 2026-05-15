from isaacsim import SimulationApp

simulation_app = SimulationApp(
    {"headless": False}
)

import asyncio
import omni.timeline

from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.stage import open_stage

# from players.motion_player import (
#     live_json_motion
# )

import players.udp_receiver as udp_receiver


USD_PATH = (
    r"C:\Users\proje\Desktop\Max\Unity - Projects\RobotAndroidController\Assets\RobotSim\Collected_WalkerS2\s2_v1.usd"
)

# LOAD USD
open_stage(USD_PATH)

print("USD loaded!")

# START TIMELINE
timeline = omni.timeline.get_timeline_interface()
timeline.play()

# WAIT FOR PHYSICS
for _ in range(10):
    simulation_app.update()

# CREATE ROBOT
robot = SingleArticulation("/s2_v1/base_link")
robot.initialize()

print("Robot initialized!")

# START JSON MOTION PLAYER
# asyncio.ensure_future(
#     live_json_motion(robot)
# )

print("Motion player started!")

# TRACK PHYSICS STATE
robot_ready = True

# MAIN LOOP
while simulation_app.is_running():

    simulation_app.update()

    # RECEIVE UDP
    udp_receiver.udp_spin_once()

    # HANDLE STOP/PLAY
    if timeline.is_playing():

        # Physics restarted
        if not robot_ready:

            try:
                robot.initialize()
                robot_ready = True
                print("ROBOT REINITIALIZED")

            except Exception as e:
                print("ROBOT INIT ERROR:", e)

    else:
        # Physics stopped
        robot_ready = False

    # APPLY UDP JOINTS
    if (
        robot_ready
        and udp_receiver.latest_joint_positions is not None
    ):

        try:
            robot.set_joint_positions(
                udp_receiver.latest_joint_positions
            )

            print("APPLIED")

        except Exception as e:
            print("SET JOINT ERROR:", e)

simulation_app.close()