import os
import sqlite3
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import socket
import json
from datetime import datetime

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
            total_visitors INTEGER,
            visitors_today INTEGER,
            visitors_this_month INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def reset_daily_and_monthly_counts():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    first_day_of_month = now.strftime('%Y-%m-01')

    # Reset daily count if it's a new day
    c.execute('''
        SELECT MAX(timestamp) FROM counts
    ''')
    last_timestamp = c.fetchone()[0]
    if last_timestamp and last_timestamp.split(' ')[0] < today:
        c.execute('''
            UPDATE counts SET visitors_today = 0 WHERE id = 1
        ''')

    # Reset monthly count if it's a new month
    if last_timestamp and last_timestamp.split(' ')[0] < first_day_of_month:
        c.execute('''
            UPDATE counts SET visitors_this_month = 0 WHERE id = 1
        ''')

    conn.commit()
    conn.close()

def update_counts(count_difference):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    first_day_of_month = now.strftime('%Y-%m-01')

    c.execute('''
        SELECT * FROM counts WHERE id = 1
    ''')
    row = c.fetchone()
    if row:
        total_visitors = row[1] + count_difference
        visitors_today = row[2] + count_difference if row[4].split(' ')[0] == today else count_difference
        visitors_this_month = row[3] + count_difference if row[4].split(' ')[0] >= first_day_of_month else count_difference

        c.execute('''
            UPDATE counts SET total_visitors = ?, visitors_today = ?, visitors_this_month = ?, timestamp = CURRENT_TIMESTAMP WHERE id = 1
        ''', (total_visitors, visitors_today, visitors_this_month))
    else:
        c.execute('''
            INSERT INTO counts (total_visitors, visitors_today, visitors_this_month) VALUES (?, ?, ?)
        ''', (count_difference, count_difference, count_difference))

    conn.commit()
    conn.close()

def get_counts():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT total_visitors, visitors_today, visitors_this_month FROM counts WHERE id = 1
    ''')
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'total_visitors': row[0],
            'visitors_today': row[1],
            'visitors_this_month': row[2]
        }
    else:
        return {
            'total_visitors': 0,
            'visitors_today': 0,
            'visitors_this_month': 0
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
                    count_difference = data.get('count', 0) - data['count']
                    update_counts(count_difference)
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
            counts = get_counts()
            self.wfile.write(json.dumps(counts).encode())
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
