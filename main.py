import time
from machine import Pin, I2C
from VL53L0X import *

# Initialize the sensors
i2c1 = I2C(scl=Pin(22), sda=Pin(21))
tof1 = VL53L0X(i2c1)
tof1.start()

i2c2 = I2C(scl=Pin(19), sda=Pin(18))
tof2 = VL53L0X(i2c2)
tof2.start()

# Variables
peopleCount = 0
thresholdDistance = 1500  # Adjusted for door height
debounce_time = 0.35  # Debounce time in seconds based on average human walking speed
sensor_matrix = [[0, 0], [0, 0]]  # Matrix to track sensor states [Previous, Current]
last_trigger_time = [0, 0]  # Timestamps of last trigger for each sensor

def read_sensors():
    global peopleCount, sensor_matrix, last_trigger_time
    current_time = time.time()

    try:
        distance1 = tof1.read()
        distance2 = tof2.read()

        # Debug output for continuous reading
        print(f"Sensor1 Distance: {distance1}, Sensor2 Distance: {distance2}")

        # Update matrix with debounce logic
        if distance1 < thresholdDistance:
            if (current_time - last_trigger_time[0]) > debounce_time:
                sensor_matrix[0][0] = sensor_matrix[0][1]  # Previous state
                sensor_matrix[0][1] = 1  # Current state
                last_trigger_time[0] = current_time
        else:
            sensor_matrix[0][1] = 0

        if distance2 < thresholdDistance:
            if (current_time - last_trigger_time[1]) > debounce_time:
                sensor_matrix[1][0] = sensor_matrix[1][1]  # Previous state
                sensor_matrix[1][1] = 1  # Current state
                last_trigger_time[1] = current_time
        else:
            sensor_matrix[1][1] = 0

        if sensor_matrix[0][0] == 0 and sensor_matrix[0][1] == 1:
            if sensor_matrix[1][1] == 1:
                peopleCount += 1
                print("Iemand is de ruimte binnengekomen. Huidige telling:", peopleCount)
                sensor_matrix[0][0] = 0
                sensor_matrix[0][1] = 0
                sensor_matrix[1][0] = 0
                sensor_matrix[1][1] = 0

        elif sensor_matrix[1][0] == 0 and sensor_matrix[1][1] == 1:
            # Sensor 2 triggered
            if sensor_matrix[0][1] == 1:
                peopleCount -= 1
                print("Iemand heeft de ruimte verlaten. Huidige telling:", peopleCount)
                # Reset matrix after counting
                sensor_matrix[0][0] = 0
                sensor_matrix[0][1] = 0
                sensor_matrix[1][0] = 0
                sensor_matrix[1][1] = 0

    except Exception as e:
        print(f"Error reading sensors: {e}")

def initialize_sensors():
    global sensor_matrix, last_trigger_time
    try:
        sensor_matrix[0][1] = tof1.read() < thresholdDistance
        sensor_matrix[1][1] = tof2.read() < thresholdDistance
        sensor_matrix[0][0] = sensor_matrix[0][1]
        sensor_matrix[1][0] = sensor_matrix[1][1]
        last_trigger_time[0] = time.time()
        last_trigger_time[1] = time.time()
    except Exception as e:
        print(f"Error initializing sensors: {e}")

initialize_sensors()

# Main loop
while True:
    read_sensors()
    time.sleep(0.1)  # Small delay to prevent overwhelming the sensor reads
