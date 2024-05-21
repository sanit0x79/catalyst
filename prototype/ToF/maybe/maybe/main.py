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

peopleCount = 0
thresholdDistance = 700
sensor1Triggered = False
sensor2Triggered = False
debounceTime = 0.2

# Connect to Wi-Fi

def connect_wifi(SSID, PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    timeout = 25  # 10 seconds timeout
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

# Web server setup
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('Listening on', addr)


def web_page():
    global peopleCount, sensor1Triggered, sensor2Triggered

    distance1 = tof1.read()
    distance2 = tof2.read()

    if distance1 < thresholdDistance:
        if not sensor1Triggered:
            sensor1Triggered = True
            if sensor2Triggered:
                peopleCount -= 1
                sensor2Triggered = False  # Reset sensor 2
                print(f"Someone left the room: {peopleCount}")

    if distance2 < thresholdDistance:
        if not sensor2Triggered:
            sensor2Triggered = True
            if sensor1Triggered:
                peopleCount += 1
                sensor1Triggered = False  # Reset sensor 1
                print(f"Someone Entered the room: {peopleCount}")

    if not (distance1 < thresholdDistance) and sensor1Triggered and not sensor2Triggered:
        sensor1Triggered = False

    if not (distance2 < thresholdDistance) and sensor2Triggered and not sensor1Triggered:
        sensor2Triggered = False

    print(f"People count: {peopleCount}")

    response = ujson.dumps({'count': peopleCount})
    return response


while True:
    try:
        cl, addr = s.accept()
       # print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        #print('Content = %s' % request)

        response = web_page()
        cl.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
        cl.send(response)
        cl.close()
    except Exception as e:
        print('Error:', e)
        cl.close()
