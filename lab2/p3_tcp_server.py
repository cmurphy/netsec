# Problem 3: Follow the example code at python.org to write a TCP server. Listen on TCP port 2003 for a message containing the flag.

import socket

TCP_IP = '192.168.14.149'
TCP_PORT = 2003

sock = socket.socket(socket.AF_INET,
      socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

conn, addr = sock.accept()
#conn.send("GET FLAG")
while True:
    data = conn.recv(1024)
    if not data: break
    print "received data: ", data
conn.close()
