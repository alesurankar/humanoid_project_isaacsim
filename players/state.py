class ControlState:
    def __init__(self):
        self.mode = "udp"   # "udp" | "ik" | "motion"

        self.udp_action = None
        self.ik_action = None
        self.motion_action = None