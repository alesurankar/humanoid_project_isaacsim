from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from isaacsim.core.utils.stage import open_stage
from isaacsim.core.utils.stage import get_current_stage
from isaacsim.core.prims import SingleArticulation
import omni.timeline
import time
import omni.usd


USD_PATH = "/home/proj/RobotAssets/Collected_WalkerS2/s2_v1.usd"

# -----------------------------
# LOAD SCENE
# -----------------------------
open_stage(USD_PATH)
print("USD loaded")

for _ in range(120):
    simulation_app.update()

# -----------------------------
# START SIMULATION
# -----------------------------
timeline = omni.timeline.get_timeline_interface()
timeline.play()

for _ in range(120):
    simulation_app.update()

print("Simulation running")

# -----------------------------
# ROBOT INIT (SAFE)
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
# TIMED LOGGER (every 4 sec)
# -----------------------------
last_print_time = time.time()

# -----------------------------
# MAIN LOOP
# -----------------------------
while simulation_app.is_running():

    simulation_app.update()

    # print every 4 seconds
    if robot is not None and (time.time() - last_print_time) > 4.0:

        try:
            # -------------------------
            # JOINT STATES
            # -------------------------
            joints = robot.get_joint_positions()

            print("\n===== JOINT STATES =====")
            print(joints)

            # -------------------------
            # TF (base_link world pose)
            # -------------------------
            stage = get_current_stage()
            base_prim = stage.GetPrimAtPath(robot_path)

            tf_matrix = omni.usd.get_world_transform_matrix(base_prim)

            pos = tf_matrix.ExtractTranslation()
            rot = tf_matrix.ExtractRotation()

            print("===== TF (base_link) =====")
            print("Position:", pos)
            print("Rotation:", rot)

            last_print_time = time.time()

        except Exception as e:
            print("LOG ERROR:", e)

simulation_app.close()