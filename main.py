from isaacsim import SimulationApp

simulation_app = SimulationApp(
    {"headless": False}
)

import asyncio
import omni.timeline

from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.stage import open_stage

from players.motion_player import live_json_motion
#from players.ik_player import live_ik_motion
import players.udp_receiver as udp_receiver
from players.state import ControlState


state = ControlState()

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
asyncio.ensure_future(
    live_json_motion(robot, state)
)
# asyncio.ensure_future(
#     live_ik_motion(robot, state)
# )

print("Motion player started!")

# MAIN LOOP
while simulation_app.is_running():

    simulation_app.update()

    # RECEIVE UDP
    udp_receiver.udp_spin_once(state)

    # =========================
    # PRIORITY SYSTEM
    # =========================

    if state.mode == "udp" and state.udp_action is not None:
        robot.apply_action(state.udp_action)

    # elif state.mode == "ik" and state.ik_action is not None:
    #     robot.apply_action(state.ik_action)

    elif state.mode == "motion" and state.motion_action is not None:
        robot.apply_action(state.motion_action)

simulation_app.close()