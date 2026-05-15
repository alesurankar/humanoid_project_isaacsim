import json
import os
import omni.kit.app
from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.types import ArticulationAction


JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)

async def live_json_motion(robot, state):

    await omni.kit.app.get_app().next_update_async()

    joint_map = {name: i for i, name in enumerate(robot.dof_names)}

    print("DOF NAMES:", robot.dof_names)

    while True:

        try:
            with open(JSON_PATH, "r") as f:
                motion = json.load(f)

            target_positions = robot.get_joint_positions().copy()

            updated_count = 0

            for joint_name, value in motion["joints"].items():

                if joint_name in joint_map:
                    target_positions[joint_map[joint_name]] = value
                    updated_count += 1
                else:
                    print("[MISSING JOINT]", joint_name)

            if updated_count > 0:

                state.motion_action = ArticulationAction(
                    joint_positions=target_positions
                )

                state.mode = "motion"

                print(f"Applied {updated_count} joints")

        except Exception as e:
            print("MOTION ERROR:", e)

        await omni.kit.app.get_app().next_update_async()