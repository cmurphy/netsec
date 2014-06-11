# Problem 4: Connect to the server at 192.168.14.10 on port 3004 and request the flag as in previous problems. The server's response will be encrypted with AES in CBC mode and transmitted as raw bytes. The key, as a hexadecimal string, is 20 14 03 04 20 14 03 04 20 14 03 04 20 14 03 04. Use binasii to convert these hex digits to 16 raw bytes in order to use them as an AES-128 key. Decrypt the message and recover the flag.

import socket
import binascii
from Crypto.Cipher import AES

TCP_IP = '192.168.14.10'
TCP_PORT = 3004

sock = socket.socket(socket.AF_INET,
      socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send("GET FLAG")
data = sock.recv(1024)
sock.close()

key = "20 14 03 04 20 14 03 04 20 14 03 04 20 14 03 04"
key_aes = binascii.a2b_hex(key.replace(' ', ''))[:16]
iv = data[:16]
data = data[16:]
print len(data)
print iv
print data
#_, len, data = data.split(' ')
cipher = AES.new(key_aes, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(data)
print "Got message: " + plaintext
print len(plaintext)
