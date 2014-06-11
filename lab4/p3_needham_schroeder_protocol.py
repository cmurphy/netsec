# Problem 3: In this problem, you must use a simplified version of the Needham-Schroeder protocol to authenticate yourself to Bob. After you have authenticated, you can ask Bob for the flag ("GET FLAG") and he will send it to you ("FLAG flag").

# Bob's address is 192.168.14.20, and he's listening on port 4333. Your trusted third party, the server S, is at 192.168.14.40, listening on port 4003.

# The protocol proceeds as follows: (Here, {xyz}_K means that xyz is encrypted with key K.)
# 1. A sends to S: A, B, Na
# 2. S sends to A: {Na, Kab, B, {Kab, A}_Kbs }_Kas
# 3. A sends to B: {Kab, A}_Kbs
# 4. B sends to A: CHALLENGE {Nb}_Kab
# 5. A sends to B: RESPONSE {Nb - 1}_Kab
# 6. A sends to B: GET FLAG
# 7. B sends to A: FLAG flag

# The server knows you as "student" and knows Bob as "bob". So for Message 1, you might send "student bob 1234". Your secret key which you share with the server is (in hex) 20 14 04 03 20 14 04 03 20 14 04 03 20 14 04 03. All encryption is performed using AES-128 in CBC mode with PKCS7 padding.

# To simplify debugging, all binary data (keys, ciphertext, etc.) are encoded in hexadecimal ASCII in the messages. So, for example, you can print Kab exactly as you receive it. But before using it to encrypt anything, you must transform it back to its native binary format using binascii.a2b_hex().

import socket
import binascii
import time
import sys
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import struct

def connect(ip, port):
    sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_serv.connect((ip, port))
    print "Successfully connected to remote server."
    return sock_serv


bob_ip = '192.168.14.20'
bob_port = 4333
server_ip = '192.168.14.40'
server_port = 4003
kas = binascii.a2b_hex("20 14 04 03 20 14 04 03 20 14 04 03 20 14 04 03".replace(' ',''))

# Initialize connections
bob = connect(bob_ip, bob_port)
server = connect(server_ip, server_port)

# 1. A sends to S: A, B, Na
my_nonce = 1234
server.send("student bob " + str(my_nonce))

# 2. S sends to A: {Na, Kab, B, {Kab, A}_Kbs }_Kas
server_response = server.recv(1024)
print "Received response from server: " + server_response

# 3. A sends to B: {Kab, A}_Kbs
iv = binascii.a2b_hex(server_response)[:16]
server_response = binascii.a2b_hex(server_response)[16:]
cipher = AES.new(kas, AES.MODE_CBC, iv)
my_nonce_serv, kab, _, bob_request = cipher.decrypt(server_response).strip().split(' ')
print "Decrypted response from server: " + repr(bob_request)

# 4. B sends to A: CHALLENGE {Nb}_Kab
bob.send(bob_request.strip('\x06'))
bob_response = bob.recv(1024)
print "Received response from Bob: " + bob_response
_, challenge = bob_response.split(' ')

# Decrypt challenge
iv = binascii.a2b_hex(challenge)[:16]
challenge = binascii.a2b_hex(challenge)[16:]
cipher = AES.new(binascii.a2b_hex(kab), AES.MODE_CBC, iv)
bob_nonce = cipher.decrypt(challenge)
print "Decrypted nonce from Bob: " + repr(bob_nonce)

# A sends to B: RESPONSE {Nb - 1}_Kab
response_nonce = str(int(bob_nonce)-1) + '\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'
cipher = AES.new(binascii.a2b_hex(kab), AES.MODE_CBC, iv)
bob_request = "RESPONSE " + binascii.b2a_hex(iv + cipher.encrypt(response_nonce))
print "Sending request to Bob: " + bob_request
bob.send(bob_request)
print "Requesting flag"
bob.send("GET FLAG")
bob_response = bob.recv(1024)
print "Received response from Bob: " + bob_response
