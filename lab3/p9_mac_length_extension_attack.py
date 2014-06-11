# Problem 9: There is a server at 192.168.14.10 on port 3009. Some clients in the network are unable to connect to this address themselves, so they must use your VM as a proxy. Listen on port 3909 for connections from the clients. When a client connects to your proxy, you should make a new connection to the server and relay messages back and forth between the client and server. The clients will request the values of several items from the server. The clients' requests will have the form "GET item1 item2 ... itemN mac", where the MAC is a secret-prefix MAC computed using an unknown, 64-bit secret value secret and an MD5 hash, like this: mac = MD5(secret||"GET item1 item2 ... itemN"). The server will only provide the items' values if the MAC is correct. One of the items on the server is "FLAG", but the client will never request it on its own. Your task is to perform a length extension attack on MD5 to add "FLAG" to the list of requested items. See this blog post for an in-depth description of the attack. (Fortunately for you, the request parser in the server is very liberal in what it accepts as a valid request.) Note that this exercise is very similar to a real vulnerability in Flickr in 2009. See the linked PDF for another description of the vulnerability and the attack technique.

import socket
import md5py
import sys
import time
import struct

TCP_IP = '192.168.14.10'
TCP_PORT = 3009
LOCAL_PORT = 3909
debug = 0

payload = ""
sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if not debug:
    sock_loc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connected = 0
    sleep_time = 8
    while not connected:
        try:
            sock_loc.bind(('0.0.0.0', LOCAL_PORT))
            print "Successfully created socket."
            connected = 1
        except socket.error:
            print "Failed to create socket, retrying in " + str(sleep_time) + " seconds..."
            time.sleep(sleep_time)
            sleep_time *= 2
            continue
        break

    sock_loc.listen(1)
    conn, addr = sock_loc.accept()
    print "Accepting data from " + addr[0]

    payload = conn.recv(1024)
    payload = payload.strip()
else:
    payload = "GET SHEEP THEFLOCK PIG FLY FITTER FIG GRIP APPLE 300caeb5b1c43bb17b3f0fdc5a949e57"

sock_serv.connect((TCP_IP, TCP_PORT))
print "Received " + payload + " from client."
message, mac = payload.rsplit(' ', 1)
A = mac[0:8]
B = mac[8:16]
C = mac[16:24]
D = mac[24:32]
message_len = len(message)
padding_length = 64 - 8 - 8 - message_len - 1
while padding_length < 0:
    padding_length += 64
message = message + struct.pack('1s', '\x80')
message = message + struct.pack(str(padding_length) + "s", '\x00')
bitsize = (message_len + 8) * 8
size_padding = 7
message = message + struct.pack('<Q', bitsize)
hac = md5py.MD5()
hac.update('AAAAAAAA' + message)
hac.A = socket.htonl(long(A, 16))
hac.B = socket.htonl(long(B, 16))
hac.C = socket.htonl(long(C, 16))
hac.D = socket.htonl(long(D, 16))
hac.update(" FLAG")
payload = message + " FLAG " + hac.hexdigest()
print "Sending " + payload + " to server."
sock_serv.send(payload)
response = sock_serv.recv(1024)
print "Received response " + response
