# Problem 4: For this problem, you can use the same trusted third party as in Problem 3. This time, your job is to get the flag from Charlie. Unfortunately, Charlie does not want to give you the flag. However, he is willing to share the flag with Bob. Charlie is listening on TCP port 4004 at 192.168.14.30. To help with your attack, you can look at a pcap file containing traces of a session between Bob and Charlie using an older version of the program with a critical security flaw. The pcap file has been posted on the testbed network at http://192.168.14.10:8000/bc.pcap

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

charlie_ip = '192.168.14.30'
charlie_port = 4004

# Initialize connections
charlie = connect(charlie_ip, charlie_port)

# 3. A sends to B: {Kab, A}_Kbs
secret_request_from_bob = 'cda284a357d2e7f0ae81f88499c29820e50cbb8c3d7b669a6c5784a5667aa09d1669275067ebb1c9314c89fe9383bd966354f01ad82f46b5a0ddf09ecc40599d'
kab = '1482e4982b566028102db2635cc4f936'

# 4. B sends to A: CHALLENGE {Nb}_Kab
charlie.send(secret_request_from_bob)
charlie_response = charlie.recv(1024)
print "Received response from Charlie: " + charlie_response
_, challenge = charlie_response.split(' ')

# Decrypt challenge
iv = binascii.a2b_hex(challenge)[:16]
challenge = binascii.a2b_hex(challenge)[16:]
cipher = AES.new(binascii.a2b_hex(kab), AES.MODE_CBC, iv)
charlie_nonce = cipher.decrypt(challenge)
print "Decrypted nonce from Charlie: " + repr(charlie_nonce)

# A sends to B: RESPONSE {Nb - 1}_Kab
response_nonce = str(int(charlie_nonce)-1) + '\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'
cipher = AES.new(binascii.a2b_hex(kab), AES.MODE_CBC, iv)
charlie_request = "RESPONSE " + binascii.b2a_hex(iv + cipher.encrypt(response_nonce))
print "Sending request to Charlie: " + charlie_request
charlie.send(charlie_request)
print "Requesting flag"
charlie.send("GET FLAG")
charlie_response = charlie.recv(1024)
print "Received response from Charlie: " + charlie_response
