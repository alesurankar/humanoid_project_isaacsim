import json
import keyboard

JSON_PATH = (
    r"C:\Users\proje\Desktop\alesurankar\scripts\humanoid_project_isaacsim\data\motion.json"
)

JOINT_NAME = "waist_pitch_joint"
STEP = 0.02


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


def increase(event):

    add_to_joint(+STEP)


def decrease(event):

    add_to_joint(-STEP)


keyboard.on_press_key("q", increase)
keyboard.on_press_key("e", decrease)

print("Q = increase")
print("E = decrease")
print("ESC = quit")

keyboard.wait("esc")