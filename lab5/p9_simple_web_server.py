# Problem 9: Write a simple web server and listen for HTTP connections on port 80. You can either write your own server from scratch using the basic socket API's, or you can build on Python's BaseHTTPServer or SimpleHTTPServer classes. A client will connect to your VM and request the resource /stuff.txt. If you give him the contents of this file in a valid HTTP response, he will then make a second HTTP request containing the flag.

import BaseHTTPServer

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        response = "ABCDEF\r\n123456\r\n!@#$%^"
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.send_header("Content-length", str(len(response)))
        s.end_headers()
        s.wfile.write(response)

handler = Handler
server_addr = ('', 80)
httpd = BaseHTTPServer.HTTPServer(server_addr, handler)
httpd.serve_forever()
