import json
import os
import omni.kit.app
from isaacsim.core.prims import SingleArticulation


JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)

async def live_json_motion():
    # WAIT UNTIL STAGE LOADS
    await omni.kit.app.get_app().next_update_async()
    await omni.kit.app.get_app().next_update_async()
    await omni.kit.app.get_app().next_update_async()
    print("INITIALIZING ROBOT")

    # CREATE ROBOT AFTER USD EXISTS
    robot = SingleArticulation("/s2_v1/base_link")
    robot.initialize()
    joint_map = {
        name: i
        for i, name in enumerate(robot.dof_names)
    }
    print(joint_map)

    print("ROBOT INITIALIZED")
    last_modified = 0

    while True:
        try:
            # print("READING JSON")

            with open(JSON_PATH, "r") as f:
                motion = json.load(f)

            current_positions = robot.get_joint_positions()
            target_positions = current_positions.copy()

            joints = motion["joints"]

            for joint_name, value in joints.items():

                if joint_name in joint_map:

                    joint_index = joint_map[joint_name]
                    target_positions[joint_index] = value

            robot.set_joint_positions(target_positions)

        except Exception as e:
            print("ERROR:", e)

        await omni.kit.app.get_app().next_update_async()