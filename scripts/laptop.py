import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import socket
import json

data = {
    'distance1': 0,
    'distance2': 0,
    'count': 0
}

def tcp_server():
    global data
    server_ip = '0.0.0.0'
    server_port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((server_ip, server_port))
    sock.listen(1)
    print('TCP server listening on', server_ip, server_port)
    
    while True:
        client, addr = sock.accept()
        print('Connected by', addr)
        buffer = ''
        while True:
            try:
                recv_data = client.recv(1024)
                if not recv_data:
                    break
                buffer += recv_data.decode()
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    data = json.loads(line)
                    print(f"Received data: {data}")
            except Exception as e:
                print(f"Error receiving data: {e}")
                break
        client.close()

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            if self.path == '/':
                self.path = '/index.html'
            super().do_GET()

def run_http_server():
    http_server = HTTPServer(('0.0.0.0', 80), RequestHandler)
    print('HTTP server listening on port 80')
    http_server.serve_forever()

if __name__ == '__main__':
    tcp_thread = threading.Thread(target=tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()

    run_http_server()
