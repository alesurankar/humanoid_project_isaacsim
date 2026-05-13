import json

JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)


def set_joint(joint_name, value):

    # LOAD JSON
    with open(JSON_PATH, "r") as f:
        motion = json.load(f)

    # MODIFY
    motion["joints"][joint_name] = value

    # SAVE
    with open(JSON_PATH, "w") as f:
        json.dump(motion, f, indent=2)

    print(f"{joint_name} -> {value}")


# EXAMPLES
set_joint("waist_pitch_joint", 0.1)