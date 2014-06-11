# Problem 6: Follow the example code at python.org to write a TCP client. Connect to IP address 192.168.14.40 on TCP port 2006 and the server will send you a math puzzle. Send the correct answer back, and then you may demand the flag.

import socket

TCP_IP = '192.168.14.40'
TCP_PORT = 2006

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
data = sock.recv(16)
print "received data: " + data
arg1, op, arg2, _, _ = data.split(' ')
ans = 0
if   op == "+":
    ans = int(arg1) + int(arg2)
elif op == "-":
    ans = int(arg1) - int(arg2)
elif op == "*":
    ans = int(arg1) * int(arg2)
elif op == "/":
    ans = int(arg1) / int(arg2)
else:
    print "Operation not defined"
sock.send(str(ans))
data = sock.recv(16)
print "received data: " + data
sock.send("GET FLAG")
data = sock.recv(25)
print "received data: " + data
