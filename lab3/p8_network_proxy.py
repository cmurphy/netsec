# Problem 8: There is a server at 192.168.14.10 on port 3008. Some clients in the network are unable to connect to this address themselves, so they must use your VM as a proxy. Listen on port 3808 for connections from the clients. When a client connects to your proxy, you should make a new connection to the server and relay messages back and forth between the client and server. There are two flags for this problem: one from the server and one from the client. You can extract them from the messages passed back and forth, but to obtain the flags, you must pass each message accurately and without too much delay.

import socket

TCP_IP = '192.168.14.10'
TCP_PORT = 3008
LOCAL_PORT = 3808

sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_loc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock_loc.bind(('0.0.0.0', LOCAL_PORT))
sock_loc.listen(1)
conn, addr = sock_loc.accept()
sock_serv.connect((TCP_IP, TCP_PORT))
print "Accepting data from " + addr[0]
payload = conn.recv(1024)
print "Forwarding request: " + payload
sock_serv.send(payload)
response = sock_serv.recv(1024)
print "Returning response: " + response
conn.send(response)
payload = conn.recv(1024)
print "Received request: " + payload
