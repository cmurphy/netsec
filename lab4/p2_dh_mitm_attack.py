# Problem 2: There is a server at 192.168.14.40 on port 4002. To retrieve its flag, clients must first perform a Diffie-Hellman key exchange with the server to derive a shared secret key. The client can then use the shared secret key to send an encrypted request ("GET FLAG cookie") and decrypt the server's encrypted response (the plaintext will be "FLAG flag"). Note that this server only provides the flag if a valid cookie is included in the request. Some clients cannot connect to this server directly, so they will attempt to connect to your IP address on port 4202. Your job is to proxy their connections to the server and perform a man-in-the-middle attack to extract the flag.

import socket
import binascii
import time
import sys
from Crypto.Cipher import AES
from Crypto.Hash import MD5

def listen():
    LOCAL_PORT = 4202
    sock_loc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_loc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    connected = 0
    sleep_time = 8
    while not connected:
        try:
            sock_loc.bind(('0.0.0.0', LOCAL_PORT))
            print "Successfully created local socket."
            connected = 1
        except socket.error:
            print "Failed to create socket, retrying in " + str(sleep_time) + " seconds..."
            time.sleep(sleep_time)
            sleep_time *= 2
            continue
        break

    sock_loc.listen(1)
    print "Listening on local socket"
    conn, addr = sock_loc.accept()
    print "Accepting data from " + addr[0]
    return conn

def connect():
    TCP_IP = '192.168.14.40'
    TCP_PORT = 4002
    sock_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_serv.connect((TCP_IP, TCP_PORT))
    print "Successfully connected to remote server."
    return sock_serv

debug = 0

g = 2
p = 999959
privatekey = 20
my_publickey = pow(g, privatekey, p)

# Open connections
if not debug:
    conn_loc = listen()
    # Initialize session with client
    client_request = conn_loc.recv(1024)
    _,client_publickey = client_request.split(' ')
    print "Received request from client: " + client_request
    client_response = "PUBKEY " + str(my_publickey)
    conn_loc.send(client_response)  # Send client our own public key
else:
    client_publickey = 906884

sock_serv = connect()

# Initialize session with server
server_request = "PUBKEY " + str(my_publickey)
print "Forwarding request to server: " + server_request
sock_serv.send(server_request)  # Exchange our public key
server_response = sock_serv.recv(1024)  # Get server public key
print "Got message from server: " + server_response
_,server_publickey = server_response.strip().split(' ')
print "Server public key: " + server_publickey

# Calculate session keys
client_session_key = MD5.new(str(pow(int(client_publickey),privatekey,p))).hexdigest()
server_session_key = MD5.new(str(pow(int(server_publickey),privatekey,p))).hexdigest()
client_key_aes = binascii.a2b_hex(client_session_key)
server_key_aes = binascii.a2b_hex(server_session_key)

if not debug:
    # Get request from client
    client_request = conn_loc.recv(1024)
    print "Received request from client: " + repr(client_request)
else:
    client_request = ')\x1d\xe0\x8c\xab\x86\x98\xce\xd8\xde\xc3]\x1e\xc1%L\xc0\xe5[\xf3n\x104\xb9\xdfX\x84\xf8\xf5\x9c\xc4i#\x91\x8eqU\x94.\xee\xa0\x1bs\xa3:(\xb7q'

# Decrypt request from client with client session key
iv = client_request[:16]
client_request = client_request[16:]
cipher = AES.new(client_key_aes, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(client_request)
print "Decrypted request from client: " + repr(plaintext)

# Reencrypt request to server with server session key
cipher = AES.new(server_key_aes, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(plaintext)

# Send request to server
server_request = iv + ciphertext
print "Forwarding request to server: " + repr(server_request)
sock_serv.send(server_request)

# Get server's response
server_response = sock_serv.recv(1024)
print "Received response from server: " + server_response
iv = server_response[:16]
server_response = server_response[16:]
cipher = AES.new(server_key_aes, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(server_response)
print "Decrypted message: " + plaintext
sock_serv.close()
if not debug:
    conn_loc.close();
