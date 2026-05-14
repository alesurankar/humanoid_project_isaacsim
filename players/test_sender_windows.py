import socket
import json

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

message = {
    "joint_positions": [0.3] * 30
}

sock.sendto(
    json.dumps(message).encode(),
    ("127.0.0.1", 5005)
)

print("sent")


