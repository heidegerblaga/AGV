import socket
from czujnik import meaure

target_host = "192.168.0.100"
target_port = 4000

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
message = bytes([0xFF,0x88,0xFF,0x88])

while meaure().split(";")[2]<="500" and meaure().split(";")[3]<="500" :
    client.sendto(message,(target_host,target_port))

    data,addr = client.recvfrom(4096)


#print(f"odebrano: {data.decode()} z adresu: {addr}")

client.close()