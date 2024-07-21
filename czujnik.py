import socket


def measure() :
    target_host = "192.168.0.100"
    target_port = 4000

    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    client.sendto(b"x",(target_host,target_port))

    data,addr = client.recvfrom(4096)


    return data.decode()