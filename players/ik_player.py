import json
import os
import numpy as np

import omni.kit.app

from omni.isaac.motion_generation import (
    LulaKinematicsSolver,
    ArticulationKinematicsSolver
)

JSON_PATH = (
    "/home/aleur/ros2_ws/src/humanoid_project_isaacsim/data/ik_test_move.json"
)

# CHANGE THESE
URDF_PATH = (
    "/home/aleur/robot.urdf"
)

ROBOT_DESCRIPTION_PATH = (
    "/home/aleur/robot_descriptor.yaml"
)

END_EFFECTOR_NAME = "L_hand"
TORSO_LINK_NAME = "base_link"

async def live_ik_motion(robot, state):

    for _ in range(5):
        await omni.kit.app.get_app().next_update_async()

    lula_solver = LulaKinematicsSolver(
        robot_description_path=ROBOT_DESCRIPTION_PATH,
        urdf_path=URDF_PATH
    )

    ik_solver = ArticulationKinematicsSolver(
        robot_articulation=robot,
        kinematics_solver=lula_solver,
        end_effector_frame_name=END_EFFECTOR_NAME
    )

    last_modified = 0

    while True:

        try:
            modified = os.path.getmtime(JSON_PATH)

            if modified != last_modified:
                last_modified = modified

                with open(JSON_PATH, "r") as f:
                    packet = json.load(f)

                left_hand = packet["left_hand"]
                local_position = np.array(left_hand["position"])

                torso_index = robot.get_link_index(TORSO_LINK_NAME)
                torso_pos, torso_quat = robot.get_link_world_pose(torso_index)

                world_position = torso_pos + local_position

                action, success = ik_solver.compute_inverse_kinematics(
                    target_position=world_position,
                    target_orientation=np.array([0,0,0,1])
                )

                if success:
                    state.ik_action = action

        except Exception as e:
            print("IK ERROR:", e)

        await omni.kit.app.get_app().next_update_async()