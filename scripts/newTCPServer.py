import os
import sqlite3
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import socket
import json

data = {
    'distance1': 0,
    'distance2': 0,
    'count': 0
}

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distance1 INTEGER,
            distance2 INTEGER,
            count INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(distance1, distance2, count):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO counts (distance1, distance2, count)
        VALUES (?, ?, ?)
    ''', (distance1, distance2, count))
    conn.commit()
    conn.close()

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
                    insert_data(data['distance1'], data['distance2'], data['count'])
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
    init_db()  # Initialize the database
    tcp_thread = threading.Thread(target=tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()

    run_http_server()
