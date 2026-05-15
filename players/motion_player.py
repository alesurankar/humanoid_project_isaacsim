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

    last_modified = 0

    while True:

        try:
            modified = os.path.getmtime(JSON_PATH)

            if modified != last_modified:
                last_modified = modified

                with open(JSON_PATH, "r") as f:
                    motion = json.load(f)

                target_positions = robot.get_joint_positions().copy()

                for joint_name, value in motion["joints"].items():
                    if joint_name in joint_map:
                        idx = joint_map[joint_name]
                        target_positions[idx] = value

                state.motion_action = ArticulationAction(
                    joint_positions=target_positions
                )

        except Exception as e:
            print("MOTION ERROR:", e)

        await omni.kit.app.get_app().next_update_async()