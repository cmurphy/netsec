# Problem 2: Follow the example code at python.org to write a UDP client. Send a packet to IP address 192.168.14.10 on UDP port 2002 and listen on the same UDP port (2002) for a response packet containing the flag.

import socket

UDP_IP = "192.168.14.10"
UDP_PORT = 2002

sock_request = socket.socket(socket.AF_INET,
      socket.SOCK_DGRAM)

sock_listen = socket.socket(socket.AF_INET,
      socket.SOCK_DGRAM)

sock_listen.bind(("192.168.14.149", UDP_PORT))

while True:
    sock_request.sendto("GET FLAG", (UDP_IP, UDP_PORT))
    print "listening"
    data, addr = sock_listen.recvfrom(1024)
    print "received message: ", data
