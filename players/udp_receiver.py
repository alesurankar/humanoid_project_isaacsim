import socket
import json
from isaacsim.core.utils.types import ArticulationAction

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5005))
sock.setblocking(False)

print("UDP listening on 5005")


def udp_spin_once(state):

    try:
        data, addr = sock.recvfrom(65535)
        message = json.loads(data.decode("utf-8"))

        joint_positions = message["joint_positions"]

        state.udp_action = ArticulationAction(
            joint_positions=joint_positions
        )

    except BlockingIOError:
        pass

    except Exception as e:
        print("UDP ERROR:", e)