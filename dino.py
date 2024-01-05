import socket

port = 53
ip = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))

while True:
    data, addr = s.recvfrom(1024)
    print(data)
    print(addr)