import socket
import json

latest_joint_positions = None

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind(("0.0.0.0", 5005))

sock.setblocking(False)

print("UDP receiver listening on port 5005")


def udp_spin_once():
    global latest_joint_positions
    try:
        data, addr = sock.recvfrom(65535)

        print("RAW UDP:", data)

        message = json.loads(
            data.decode("utf-8")
        )

        print("PARSED:", message)

        latest_joint_positions = message["joint_positions"]

        print("JOINTS RECEIVED")

    except BlockingIOError:
        pass

    except Exception as e:
        print("UDP ERROR:", e)