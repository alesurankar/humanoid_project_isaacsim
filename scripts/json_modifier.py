import json
import keyboard
import time

JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)

JOINT_NAME = "waist_pitch_joint"
STEP = 0.1


def load_motion():

    with open(JSON_PATH, "r") as f:
        return json.load(f)


def save_motion(motion):

    with open(JSON_PATH, "w") as f:
        json.dump(motion, f, indent=2)


def add_to_joint(delta):

    motion = load_motion()

    current_value = motion["joints"][JOINT_NAME]

    new_value = current_value + delta

    motion["joints"][JOINT_NAME] = new_value

    save_motion(motion)

    print(f"{JOINT_NAME}: {new_value}")


print("CONTROLS:")
print("Q = +0.1")
print("E = -0.1")
print("ESC = quit")

while True:

    # INCREASE
    if keyboard.is_pressed("q"):

        add_to_joint(+STEP)

        time.sleep(0.2)

    # DECREASE
    if keyboard.is_pressed("e"):

        add_to_joint(-STEP)

        time.sleep(0.2)

    # EXIT
    if keyboard.is_pressed("esc"):

        print("EXIT")
        break