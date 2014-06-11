# Problem 1: There is a server at 192.168.14.40 on port 4001. To retrieve its flag, you must first perform a Diffie-Hellman key exchange with the server to derive a shared secret key. You can then use the shared secret key to send an encrypted request ("GET FLAG") and decrypt the server's encrypted response (the plaintext will be "FLAG flag").

# For a review of the Diffie-Hellman key exchange, see Mark Loiseau's tutorial. Here, our server uses the prime p = 999,959 and the generator g = 2.

# Note: In order to make this exercise possible without importing additional libraries, we're using small numbers that are NOT safe for use in the real world. (Using g = 2 is OK. In practice, p should be much larger.)

# The protocol works as follows:

# 1. When you connect, the server immediately sends you its public key: "PUBKEY pubkey", where pubkey is a standard decimal ASCII-encoded integer. If the server's private key is s, then the server's public key is equal to g^s mod p.

# 2. You should reply with your public key in the same format: "PUBKEY pubkey". If your private key is c, then you can compute your public key as g^c mod p.

# 3. Both sides then derive the session key as MD5(g^(sc) mod p). (Note: The PyCrypto MD5 implementation wants a string for its input, so be sure to call str() on your integer g^(sc) before passing it to MD5.)

# 4. You can now encrypt your request ("GET FLAG") with AES-128 in CBC mode using the session key. You send your encrypted request to the server as raw binary bytes.

# 5. The server attempts to decrypt your request, and if successful, it sends back a response ("FLAG flag") encrypted with the same key in the same way.

import socket
import binascii
from Crypto.Cipher import AES
from Crypto.Hash import MD5

TCP_IP = '192.168.14.40'
TCP_PORT = 4001

g = 2
p = 999959
privatekey = 20
my_publickey = pow(g, privatekey, p)

sock = socket.socket(socket.AF_INET,
      socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
data = sock.recv(1024)
print "Got message: " + data
_,server_publickey = data.split(' ')
print "Sending message: " + "PUBKEY " + str(my_publickey)
sock.send("PUBKEY " + str(my_publickey))

session_key = MD5.new(str(pow(int(server_publickey),privatekey,p))).hexdigest()
print "Using session key: " + session_key
key_aes = binascii.a2b_hex(session_key)
iv = binascii.a2b_hex("123456789abcdef0123456789abcdef0")
cipher = AES.new(key_aes, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt("GET FLAG\x00\x00\x00\x00\x00\x00\x00\x00")
request = iv + ciphertext
print "Sending encrypted request: " + request
sock.send(request)
data = sock.recv(1024)
print "Got message: " + data
iv = data[:16]
data = data[16:]
cipher = AES.new(key_aes, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(data)
print "Decrypted message: " + plaintext

sock.close()
