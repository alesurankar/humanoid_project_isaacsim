import json
import asyncio
import os

import omni.kit.app
import omni.timeline

from isaacsim.core.prims import SingleArticulation
from joint_map import joint_map

timeline = omni.timeline.get_timeline_interface()

# START SIMULATION
if not timeline.is_playing():
    timeline.play()

robot = SingleArticulation("/s2_v1/base_link")
robot.initialize()

JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)


async def live_json_motion():

    last_modified = 0

    while True:

        try:
            modified = os.path.getmtime(JSON_PATH)

            # FILE CHANGED
            if modified != last_modified:

                last_modified = modified

                print("JSON UPDATED")

                # LOAD JSON
                with open(JSON_PATH, "r") as f:
                    motion = json.load(f)

                current_positions = robot.get_joint_positions()
                target_positions = current_positions.copy()

                # READ JOINTS FROM JSON
                joints = motion["joints"]

                # CONVERT NAMES -> INDICES
                for joint_name, value in joints.items():

                    if joint_name in joint_map:

                        joint_index = joint_map[joint_name]

                        target_positions[joint_index] = value

                # SMOOTH INTERPOLATION
                steps = 120

                for step in range(steps):

                    alpha = (step + 1) / steps

                    interpolated = (
                        current_positions * (1 - alpha)
                        + target_positions * alpha
                    )

                    robot.set_joint_positions(interpolated)

                    await omni.kit.app.get_app().next_update_async()

        except Exception as e:

            print("ERROR:", e)

        # CHECK EVERY FRAME
        await omni.kit.app.get_app().next_update_async()


# RUN
asyncio.ensure_future(
    live_json_motion()
)