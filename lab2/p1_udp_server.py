# Problem 1: Follow the example code at python.org to write a UDP server. Listen on UDP port 2001 for a packet containing the flag.

import socket

UDP_IP = "192.168.14.149"
UDP_PORT = 2001

sock = socket.socket(socket.AF_INET,
      socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024)
  print "received message:", data
