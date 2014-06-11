# Problem 5: Connect to the server at 192.168.14.10 on port 3005 and request the flag as in previous problems. The server's response will be provided in plain text, but it will include a hash to let you verify the integrity of the message. The message format for the server's response is: "FLAG flag hash", where hash = H("FLAG flag"). The hash is computed using SHA-256 and is encoded in the message as hexadecimal ASCII characters.

import socket
import hashlib

TCP_IP = '192.168.14.10'
TCP_PORT = 3005

while True:
    sock = socket.socket(socket.AF_INET,
          socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send("GET FLAG")
    data = sock.recv(1024)
    sock.close()

    print "Got message: " + data
    keyword, data, hash = data.split(' ')
    verified = hashlib.sha256(keyword + " " + data)
    if verified.hexdigest().strip() == hash.strip():
        break
    else:
        print "Got bad flag. Retrying."
print "Got flag: " + data
