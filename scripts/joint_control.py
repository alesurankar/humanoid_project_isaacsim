import json
import keyboard
import time

JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)

JOINT_NAME = "waist_pitch_joint"

STEP = 0.01

MIN_VALUE = -1.5
MAX_VALUE = 1.5


def load_motion():

    with open(JSON_PATH, "r") as f:
        return json.load(f)


def save_motion(motion):

    with open(JSON_PATH, "w") as f:

        json.dump(motion, f, indent=4)

        # FORCE IMMEDIATE WRITE
        f.flush()


def add_to_joint(delta):

    motion = load_motion()

    if JOINT_NAME not in motion["joints"]:
        motion["joints"][JOINT_NAME] = 0.0

    current_value = motion["joints"][JOINT_NAME]

    new_value = current_value + delta

    # CLAMP
    new_value = max(MIN_VALUE, min(MAX_VALUE, new_value))

    motion["joints"][JOINT_NAME] = new_value

    save_motion(motion)

    print(f"{JOINT_NAME}: {new_value:.3f}")


print("HOLD Q = increase")
print("HOLD E = decrease")
print("ESC = quit")


while True:

    if keyboard.is_pressed("q"):

        add_to_joint(+STEP)

    if keyboard.is_pressed("e"):

        add_to_joint(-STEP)

    if keyboard.is_pressed("esc"):

        print("EXIT")

        break

    # UPDATE RATE
    time.sleep(0.01)