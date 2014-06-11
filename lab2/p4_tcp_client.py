# Problem 4: Follow the example code at python.org to write a TCP client. Connect to IP address 192.168.14.20 on TCP port 2004. Send it the message "GET FLAG", and the server will send you the flag.

import socket

TCP_IP = '192.168.14.20'
TCP_PORT = 2004

sock = socket.socket(socket.AF_INET,
      socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send("GET FLAG")
data = sock.recv(1024)
sock.close()

print "received data: ", data
