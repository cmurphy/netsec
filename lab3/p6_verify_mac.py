# Problem 6: Connect to the server at 192.168.14.10 on port 3006 and request the flag as in previous problems. The server's response will be provided in plain text, but it will include a message authentication code to let you verify the integrity of the message. The message format for the server's response is: "FLAG flag mac", where mac = MAC("FLAG flag"). The MAC is computed using HMAC-SHA1 and is encoded in the message as hexadecimal ASCII characters. The key, as a hexadecimal string, is 20 14 03 06 20 14 03 06 20 14 03 06 20 14 03 06 20 14 03 06.

import socket
from Crypto.Hash import HMAC
from Crypto.Hash import SHA
import binascii

TCP_IP = '192.168.14.10'
TCP_PORT = 3006

while True:
    sock = socket.socket(socket.AF_INET,
          socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send("GET FLAG")
    data = sock.recv(2048)
    sock.close()

    key = "20 14 03 06 20 14 03 06 20 14 03 06 20 14 03 06 20 14 03 06"
    key = key.replace(' ','')
    key = binascii.unhexlify(key)
    print "Got message: " + data
    keyword, data, mac = data.split(' ')
    print keyword + " " + data
    verified = HMAC.new(key, keyword + " " + data, SHA.new())
    print "Got MAC digest " + verified.hexdigest()
    if verified.hexdigest().strip() == mac.strip():
        break
    else:
        print "Got bad flag. Retrying."
print "Got flag: " + data
