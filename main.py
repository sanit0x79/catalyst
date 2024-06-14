import network
import time
from machine import Pin, I2C
import ujson
from VL53L0X import *
import socket

# Wi-Fi credentials
SSID = 'pixel1234'
PASSWORD = 'test1234'

# Initialize the sensors
i2c1 = I2C(scl=Pin(22), sda=Pin(21))
tof1 = VL53L0X(i2c1)
tof1.start()

i2c2 = I2C(scl=Pin(19), sda=Pin(18))
tof2 = VL53L0X(i2c2)
tof2.start()

# Variables
peopleCount = 0
thresholdDistance = 750  # Adjusted for door height
sensor_matrix = [[0, 0], [0, 0]]  # Matrix to track sensor states [Previous, Current]

# Connect to Wi-Fi
def connect_wifi(SSID, PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    timeout = 20  # 20 seconds timeout
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        print('Connecting to Wi-Fi...')
        print(f'Status: {wlan.status()}')

    if wlan.isconnected():
        print('Connected to Wi-Fi')
        print('Network config:', wlan.ifconfig())
        return wlan.ifconfig()[0]
    else:
        print('Failed to connect to Wi-Fi')
        return None

ip_address = connect_wifi(SSID, PASSWORD)
if ip_address:
    print('ESP32 IP Address:', ip_address)
else:
    print('Failed to connect to Wi-Fi.')
    raise Exception("Failed to connect to Wi-Fi")

# Web server setup
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('Listening on', addr)

def web_page():
    global peopleCount
    response = ujson.dumps({'count': peopleCount})
    return response

def read_sensors():
    global peopleCount, sensor_matrix
    try:
        distance1 = tof1.read()
        distance2 = tof2.read()

        # Debug output for continuous reading
        print(f"Sensor1 Distance: {distance1}, Sensor2 Distance: {distance2}")

        # Update matrix
        sensor_matrix[0][0] = sensor_matrix[0][1]
        sensor_matrix[1][0] = sensor_matrix[1][1]
        
        sensor_matrix[0][1] = distance1 < thresholdDistance
        sensor_matrix[1][1] = distance2 < thresholdDistance

        # Detect people passing through based on sensor order
        if sensor_matrix[0][0] == 0 and sensor_matrix[0][1] == 1:
            if sensor_matrix[1][0] == 1:
                peopleCount += 1
                print("Iemand is de ruimte binnengekomen. Huidige telling:", peopleCount)

        if sensor_matrix[1][0] == 0 and sensor_matrix[1][1] == 1:
            if sensor_matrix[0][0] == 1:
                peopleCount -= 1
                print("Iemand heeft de ruimte verlaten. Huidige telling:", peopleCount)

    except Exception as e:
        print(f"Error reading sensors: {e}")

# Initialize sensor states to avoid initial miscounts
def initialize_sensors():
    try:
        sensor_matrix[0][1] = tof1.read() < thresholdDistance
        sensor_matrix[1][1] = tof2.read() < thresholdDistance
        sensor_matrix[0][0] = sensor_matrix[0][1]
        sensor_matrix[1][0] = sensor_matrix[1][1]
    except Exception as e:
        print(f"Error initializing sensors: {e}")

initialize_sensors()

while True:
    read_sensors()

    try:
        cl, addr = s.accept()
        request = cl.recv(1024)
        request = str(request)

        response = web_page()
        cl.send(
            'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
        cl.send(response)
        cl.close()
    except Exception as e:
        print(f'Error: {e}')
        if cl:
            cl.close()
