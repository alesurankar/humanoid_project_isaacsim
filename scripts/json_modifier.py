import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

JSON_PATH = ROOT / "data" / "motion.json"


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