import socket
from czujnik import measure
from logika import Controller
import struct

target_host = "192.168.0.101"
target_port = 4000

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
message = bytes([0xFF,0x88,0xFF,0x88])


X = Controller(5000,5000,5000,500,500)

print(X.control_agv(1000,1000,1000))

client.close()