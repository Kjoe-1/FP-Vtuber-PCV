import socket
import json

class UDPSender:
    def __init__(self, ip="127.0.0.1", port=5052):
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data: dict):
        self.sock.sendto(json.dumps(data).encode(), self.addr)

    