from isaacsim import SimulationApp

simulation_app = SimulationApp(
    {"headless": False}
)

import asyncio
import omni.timeline

from isaacsim.core.utils.stage import open_stage
from players.motion_player import live_json_motion


USD_PATH = (
    r"C:\Users\proje\Desktop\Max\Unity - Projects\RobotAndroidController\Assets\RobotSim\Collected_WalkerS2\s2_v1.usd"
)

# LOAD USD
open_stage(USD_PATH)

print("USD loaded!")

# START TIMELINE
timeline = omni.timeline.get_timeline_interface()
timeline.play()

# START MOTION PLAYER
asyncio.ensure_future(
    live_json_motion()
)

print("Motion player started!")

# MAIN LOOP
while simulation_app.is_running():

    simulation_app.update()

simulation_app.close()