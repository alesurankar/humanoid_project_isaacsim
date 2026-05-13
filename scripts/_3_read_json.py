import json
import asyncio
import omni.kit.app
import omni.timeline

from isaacsim.core.prims import SingleArticulation

timeline = omni.timeline.get_timeline_interface()

# START SIMULATION
if not timeline.is_playing():
    timeline.play()

robot = SingleArticulation("/s2_v1/base_link")
robot.initialize()


# JOINT NAME -> INDEX
joint_map = {
    "L_hip_roll_joint": 0,
    "R_hip_roll_joint": 1,
    "waist_yaw_joint": 2,
    "L_hip_yaw_joint": 3,
    "R_hip_yaw_joint": 4,
    "waist_pitch_joint": 5,
    "L_hip_pitch_joint": 6,
    "R_hip_pitch_joint": 7,
    "L_knee_pitch_joint": 8,
    "R_knee_pitch_joint": 9,
    "L_shoulder_pitch_joint": 10,
    "R_shoulder_pitch_joint": 11,
    "head_yaw_joint": 12,
    "L_ankle_pitch_joint": 13,
    "R_ankle_pitch_joint": 14,
    "L_shoulder_roll_joint": 15,
    "R_shoulder_roll_joint": 16,
    "head_pitch_joint": 17,
    "L_ankle_roll_joint": 18,
    "R_ankle_roll_joint": 19,
    "L_shoulder_yaw_joint": 20,
    "R_shoulder_yaw_joint": 21,
    "L_elbow_roll_joint": 22,
    "R_elbow_roll_joint": 23,
    "L_elbow_yaw_joint": 24,
    "R_elbow_yaw_joint": 25,
    "L_wrist_pitch_joint": 26,
    "R_wrist_pitch_joint": 27,
    "L_wrist_roll_joint": 28,
    "R_wrist_roll_joint": 29,
}


# LOAD JSON
with open(
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json",
    "r"
) as f:

    motion = json.load(f)


async def move_from_json(steps=120):

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
    for step in range(steps):

        alpha = (step + 1) / steps

        interpolated = (
            current_positions * (1 - alpha)
            + target_positions * alpha
        )

        robot.set_joint_positions(interpolated)

        await omni.kit.app.get_app().next_update_async()


# RUN
asyncio.ensure_future(
    move_from_json()
)