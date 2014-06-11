# Problem 1: Connect to the server at 192.168.14.10 on port 3001 and request the flag as in Lab 02. Unlike in Lab 02, where the flags were always ASCII text, this flag will be sent to you as raw binary bytes. The format of the server's response message will be "FLAG length flag", where length is the length of the flag in bytes, written as a standard decimal integer. Encode the flag as ASCII characters using hexadecimal encoding with Python's binascii module or a similar facility. 

import socket
import binascii

TCP_IP = '192.168.14.10'
TCP_PORT = 3001

sock = socket.socket(socket.AF_INET,
      socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send("GET FLAG")
data = sock.recv(1024)
sock.close()

_, len, data = data.split(' ')
print "received data: ", len + " " + binascii.b2a_hex(data)
