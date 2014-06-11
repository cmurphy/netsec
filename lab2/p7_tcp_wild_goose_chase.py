# Problem 7: Follow the example code at python.org to write a TCP client. Connect to IP address 192.168.14.10 on TCP port 2007 and demand the flag. The server will reply in one of two ways. Either it will give you the flag, or it will point you to another server that can help you find the flag. Follow the clues until you find the flag!

import socket

TCP_IP = '192.168.14.10'
TCP_PORT = 2007

data = ""
while "FLAG" not in data:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send("GET FLAG")
    data = sock.recv(28)
    print "received data: " + data
    if "FLAG" in data:
        break
    else:
        _, dest = data.split(' ')
        TCP_IP, TCP_PORT = dest.split(':')
        TCP_PORT = int(TCP_PORT)
print "FLAG: " + data
