import socket
from czujnik import measure
# from logika import control_agv
import struct

target_host = "192.168.0.101"
target_port = 4000

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
message = bytes([0xFF,0x88,0xFF,0x88])
client.sendto(message, (target_host, target_port))
#
# data, addr = client.recvfrom(4096)
# print("halo")
#
# print(f"odebrano: {data.decode()} z adresu: {addr}")
print(measure().split(";"))



# wheel1 = control_agv(int(measure().split(";")[2]), int(measure().split(";")[1]),int(measure().split(";")[3]))[0]
# wheel2 = control_agv(int(measure().split(";")[2]), int(measure().split(";")[1]),int(measure().split(";")[3]))[1]
#
#
# while measure().split(";")[2]<="500" and measure().split(";")[3]<="500" :
#     client.sendto(message,(target_host,target_port))
#
#     data,addr = client.recvfrom(4096)
#     print("halo")
#
#     print(f"odebrano: {data.decode()} z adresu: {addr}")
#     print(measure().split(";"))
while True :
    # client.sendto(message,(target_host,target_port))

    # data,addr = client.recvfrom(4096)
    print("halo")

    # print(f"odebrano: {data.decode()} z adresu: {addr}")
    print(measure().split(";"))
    import time

    time.sleep(5)

client.close()