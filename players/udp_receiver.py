import socket
import json
import time

latest_joint_positions = None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5005))
sock.setblocking(False)

print("[UDP] Receiver started on 0.0.0.0:5005")
print("[UDP] Socket fd:", sock.fileno())


def udp_spin_once():
    global latest_joint_positions

    try:
        data, addr = sock.recvfrom(65535)

        try:
            message = json.loads(data.decode("utf-8"))
        except Exception as e:
            #print("[UDP] JSON PARSE FAILED:", e)
            return

        #print("[UDP] PARSED:", message)

        if "joint_positions" not in message:
            #print("[UDP] WARNING: missing joint_positions key")
            return

        latest_joint_positions = message["joint_positions"]

        #print("[UDP] STORED JOINTS:", len(latest_joint_positions))
        #print("==============================\n")

    except BlockingIOError:
        pass

    except Exception as e:
        print("[UDP ERROR]", type(e).__name__, e)