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


def initialize_sensor(i2c, retries=3):
    sensor = None
    for attempt in range(retries):
        try:
            sensor = VL53L0X(i2c)
            sensor.start()
            print(f"Sensor initialized successfully on attempt {attempt + 1}")
            break
        except Exception as e:
            print(f"Failed to initialize sensor on attempt {attempt + 1}: {e}")
            sensor = None
            time.sleep(1)
    return sensor


i2c1 = I2C(scl=Pin(22), sda=Pin(21))
tof1 = initialize_sensor(i2c1)

i2c2 = I2C(scl=Pin(19), sda=Pin(18))
tof2 = initialize_sensor(i2c2)

peopleCount = 0  # Define the peopleCount variable
thresholdDistance = 800
sensor1Triggered = False
sensor2Triggered = False
debounceTime = 1

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
        print(f'Status: {wlan.status()}')  # Print the status

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

# Server setup to send data to the laptop
server_ip = '192.168.241.39'
server_port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((server_ip, server_port))
    print(f"Connected to laptop server at {server_ip}:{server_port}")
except Exception as e:
    print(f"Failed to connect to laptop server: {e}")
    raise


def read_sensors():
    global peopleCount, sensor1Triggered, sensor2Triggered
    try:
        if tof1 is None or tof2 is None:
            raise Exception("Sensors not initialized")

        distance1 = tof1.read()
        distance2 = tof2.read()

        if distance1 is None or distance2 is None:
            raise ValueError("Sensor reading is None")

        print(f"Sensor1 Distance: {distance1}, Sensor2 Distance: {
              distance2}, {peopleCount}")

        current_time = time.time()

        if distance1 < thresholdDistance and not sensor1Triggered:
            sensor1Triggered = True
            if sensor2Triggered:
                peopleCount -= 1
                sensor2Triggered = False  # Reset sensor 2
                print(f"Someone left the room: {peopleCount}")
            time.sleep(debounceTime)  # Debounce delay

        if distance2 < thresholdDistance and not sensor2Triggered:
            sensor2Triggered = True
            if sensor1Triggered:
                peopleCount += 1
                sensor1Triggered = False  # Reset sensor 1
                print(f"Someone entered the room: {peopleCount}")
            time.sleep(debounceTime)  # Debounce delay

        if not (distance1 < thresholdDistance) and sensor1Triggered and not sensor2Triggered:
            sensor1Triggered = False

        if not (distance2 < thresholdDistance) and sensor2Triggered and not sensor1Triggered:
            sensor2Triggered = False

        data = {'distance1': distance1,
                'distance2': distance2, 'count': peopleCount}
        # Add a newline character as a delimiter
        return ujson.dumps(data) + '\n'
    except Exception as e:
        print(f"Error reading sensors: {e}")
        return ujson.dumps({'error': str(e)}) + '\n'


last_sensor_read_time = time.time()
sensor_read_interval = 0.1  # Read sensors every 0.1 seconds

while True:
    current_time = time.time()

    if current_time - last_sensor_read_time >= sensor_read_interval:
        sensor_data = read_sensors()
        try:
            sock.send(sensor_data.encode())
        except Exception as e:
            print(f"Error sending data: {e}")
            sock.close()
            break
        last_sensor_read_time = current_time

    time.sleep(0.1)
