# Problem 10: There is a server at 192.168.14.10 on port 3010. Some clients in the network are unable to connect to this address themselves, so they must use your VM as a proxy. Listen on port 3110 for connections from the clients. When a client connects to your proxy, you should make a new connection to the server and relay messages back and forth between the client and server. The clients' requests are encrypted using AES-128 in OFB mode using an unknown secret key. The request plaintexts have the form "GET item1 item2 ... itemN". The server only provides the requested values if the encrypted message decrypts to a valid request. Server responses are not encrypted. Your task is to modify a client request so that the server provides the value of FLAG in its response. Fortunately for you, we have reports that the clients always request the same items in the same order. These are: DOG, FROG, GRIP, STOP, and FLY.

import socket
import time

TCP_IP = '192.168.14.10'
TCP_PORT = 3010
LOCAL_PORT = 3110
debug = 0

def xor(xs, ys):
    maxlen = max(len(xs), len(ys))
    if len(xs) < maxlen:
        xs += '\x00' * (maxlen - len(xs))
    else:
        ys += '\x00' * (maxlen - len(ys))
    x = ""
    for i in range(0,maxlen):
        x += chr(ord(xs[i]) ^ ord(ys[i]))
    return x

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
    ciphertext = conn.recv(1024)
else:
    ciphertext = '\x7fnQs\xba\x11x\xdf\xc3`\xaa\x8bVr:\x04\x8e\x93\xacv\xb3\xc0\x18\x83F\xc3<^\xea\xaaK\xe0\xb9\x08\x13\x9f\x12Dg\xa1\x88\r^.V4\xfc\x16'
sock_serv.connect((TCP_IP, TCP_PORT))
print "ciphertext:    " + repr(ciphertext)
iv = ciphertext[:16]
data = ciphertext[16:]
plaintext = "GET DOG FROG GRIP STOP FLY"
desired = "GET DOG FLAG GRIP STOP FLY"
attack = xor(plaintext, desired)
print "attack string: " + repr(attack)
payload = xor(data.strip(), attack)
#payload = data
print "payload:       " + repr(payload)
print "Forwarding request: " + payload
sock_serv.send(iv + payload)
response = sock_serv.recv(1024)
print "Received response: " + response
