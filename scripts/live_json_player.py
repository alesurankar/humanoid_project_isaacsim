import json
import asyncio
import os

import omni.kit.app
import omni.timeline

from isaacsim.core.prims import SingleArticulation
from joint_map import joint_map

# TIMELINE
timeline = omni.timeline.get_timeline_interface()

# START SIMULATION
if not timeline.is_playing():
    timeline.play()

# ROBOT
robot = SingleArticulation("/s2_v1/base_link")
robot.initialize()

# JSON FILE
JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)


async def live_json_motion():

    last_modified = 0

    while True:

        try:

            # CHECK FILE MODIFICATION TIME
            modified = os.path.getmtime(JSON_PATH)

            # ONLY UPDATE WHEN FILE CHANGES
            if modified != last_modified:

                last_modified = modified

                print("JSON UPDATED")

                # LOAD JSON
                with open(JSON_PATH, "r") as f:
                    motion = json.load(f)

                # CURRENT ROBOT POSE
                current_positions = robot.get_joint_positions()

                # COPY CURRENT POSE
                target_positions = current_positions.copy()

                # JSON JOINT DATA
                joints = motion["joints"]

                # APPLY JSON VALUES
                for joint_name, value in joints.items():
                    if joint_name in joint_map:
                        joint_index = joint_map[joint_name]
                        target_positions[joint_index] = value

                    else:
                        print(f"UNKNOWN JOINT: {joint_name}")

                # SEND TARGETS TO ROBOT
                robot.set_joint_position_targets(target_positions)

        except Exception as e:

            print("ERROR:", e)

        # WAIT ONE FRAME
        await omni.kit.app.get_app().next_update_async()


# START ASYNC TASK
asyncio.ensure_future(
    live_json_motion()
)