from isaacsim.core.prims import SingleArticulation
import numpy as np

robot = SingleArticulation("/s2_v1/base_link")
robot.initialize()

# reusable function
def move_joints(joint_values):
    positions = robot.get_joint_positions()

    for joint_index, value in joint_values.items():
        positions[joint_index] = value

    robot.set_joint_positions(positions)


# POSE
move_joints({

    # ===== HIP ROLL =====
    0: 0.0,   # L_hip_roll_joint
    1: 0.0,   # R_hip_roll_joint

    # ===== WAIST =====
    2: 0.0,   # waist_yaw_joint
    5: -0.1,   # waist_pitch_joint

    # ===== HIP YAW =====
    3: 0.0,   # L_hip_yaw_joint
    4: 0.0,   # R_hip_yaw_joint

    # ===== HIP PITCH =====
    6: 0.0,   # L_hip_pitch_joint
    7: 0.0,   # R_hip_pitch_joint

    # ===== KNEES =====
    8: 0.0,   # L_knee_pitch_joint
    9: 0.0,   # R_knee_pitch_joint

    # ===== SHOULDERS PITCH =====
    10: 0.0,  # L_shoulder_pitch_joint
    11: 0.0,  # R_shoulder_pitch_joint

    # ===== HEAD =====
    12: 0.0,  # head_yaw_joint
    17: 0.0,  # head_pitch_joint

    # ===== ANKLES PITCH =====
    13: 0.0,  # L_ankle_pitch_joint
    14: 0.0,  # R_ankle_pitch_joint

    # ===== SHOULDERS ROLL =====
    15: 0.0,  # L_shoulder_roll_joint
    16: 0.0,  # R_shoulder_roll_joint

    # ===== ANKLES ROLL =====
    18: 0.0,  # L_ankle_roll_joint
    19: 0.0,  # R_ankle_roll_joint

    # ===== SHOULDERS YAW =====
    20: 0.0,  # L_shoulder_yaw_joint
    21: 0.0,  # R_shoulder_yaw_joint

    # ===== ELBOW ROLL =====
    22: 0.0,  # L_elbow_roll_joint
    23: 0.0,  # R_elbow_roll_joint

    # ===== ELBOW YAW =====
    24: 0.0,  # L_elbow_yaw_joint
    25: 0.0,  # R_elbow_yaw_joint

    # ===== WRIST PITCH =====
    26: 0.0,  # L_wrist_pitch_joint
    27: 0.0,  # R_wrist_pitch_joint

    # ===== WRIST ROLL =====
    28: 0.0,  # L_wrist_roll_joint
    29: 0.0,  # R_wrist_roll_joint

})