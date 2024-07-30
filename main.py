import socket
import time

from czujnik import meaure
from logika import control_agv
import struct

target_host = "192.168.0.101"
target_port = 4000
message = bytes([0xFF,0x88,0xFF,0x88])

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# client.sendto(message, (target_host, target_port))


while True:

    try :
        print("\n")

        print(meaure())

        wheel1 = control_agv(int(meaure().split(";")[1]), int(meaure().split(";")[2]), int(meaure().split(";")[3]))[0]
        wheel2 = control_agv(int(meaure().split(";")[1]), int(meaure().split(";")[2]), int(meaure().split(";")[3]))[1]
        print(control_agv(int(meaure().split(";")[1]), int(meaure().split(";")[3])))


        message = bytes([0xFF,int(wheel1),0xFF,int(wheel2)])
        client.sendto(message,(target_host,target_port))
        time.sleep(3)
        print("\n")
    except:
        time.sleep(3)

client.close()