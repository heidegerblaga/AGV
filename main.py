import socket

target_host = "192.168.0.100"
target_port = 4000

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

i = 0



message = bytes([0xFF,0x88,0x88,0xFF])

client.sendto(message,(target_host,target_port))


client.close()