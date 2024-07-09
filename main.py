import socket
from czujnik import meaure
from logika import control_agv
import struct

target_host = "192.168.0.101"
target_port = 4000

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
message = bytes([0xFF,0x88,0xFF,0x88])

print(control_agv(int(meaure().split(";")[1]),int(meaure().split(";")[3])))
wheel1 = control_agv(int(meaure().split(";")[1]),int(meaure().split(";")[3]))[0]
wheel2 = control_agv(int(meaure().split(";")[1]),int(meaure().split(";")[3]))[1]

while True:
    print(control_agv(int(meaure().split(";")[1]), int(meaure().split(";")[3])))
    print(meaure().split(";"))
    message = bytes([0xFF,int(wheel1),0xFF,int(wheel2)])
    client.sendto(message,(target_host,target_port))
# while meaure().split(";")[2]<="500" and meaure().split(";")[3]<="500" :
#     client.sendto(message,(target_host,target_port))
#
#     data,addr = client.recvfrom(4096)
#     print("halo")
#
#     print(f"odebrano: {data.decode()} z adresu: {addr}")
#     print(meaure().split(";"))

client.close()