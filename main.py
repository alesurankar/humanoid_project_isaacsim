from isaacsim import SimulationApp

simulation_app = SimulationApp(
    {"headless": False}
)

from isaacsim.core.utils.stage import open_stage
import omni.timeline

USD_PATH = (
    r"C:\Users\proje\Desktop\Max\Unity - Projects\RobotAndroidController\Assets\RobotSim\Collected_WalkerS2\s2_v1.usd"
)

# LOAD USD
open_stage(USD_PATH)

print("USD loaded!")

# TIMELINE
timeline = omni.timeline.get_timeline_interface()

timeline.play()

counter = 0

# MAIN LOOP
while simulation_app.is_running():

    simulation_app.update()

    counter += 1

    if counter % 1000 == 0:

        print("MAIN LOOP RUNNING")

simulation_app.close()