import time
from machine import I2C, Pin
import VL53L0X

sclPin1 = 22
sdaPin1 = 21
sclPin2 = 19
sdaPin2 = 18

i2c1 = I2C(0, scl=Pin(sclPin1), sda=Pin(sdaPin1))
tof1 = VL53L0X.VL53L0X(i2c1)
tof1.start()
i2c2 = I2C(1, scl=Pin(sclPin2), sda=Pin(sdaPin2))
tof2 = VL53L0X.VL53L0X(i2c2)
tof2.start()

peopleCount = 0
thresholdDistance = 350
sensor1Triggered = False
sensor2Triggered = False
debounceTime = 0.4

try:
    while True:
        distance1 = tof1.read()
        distance2 = tof2.read()

        if distance1 < thresholdDistance:
            if not sensor1Triggered:
                sensor1Triggered = True
                if sensor2Triggered:
                    peopleCount -= 1
                    print("Person exited. Count:", peopleCount)
                    sensor2Triggered = False  # Reset sensor 2

        if distance2 < thresholdDistance:
            if not sensor2Triggered:
                sensor2Triggered = True
                if sensor1Triggered:
                    peopleCount += 1
                    print("Person entered. Count:", peopleCount)
                    sensor1Triggered = False  # Reset sensor 1

        if not (distance1 < thresholdDistance) and sensor1Triggered and not sensor2Triggered:
            sensor1Triggered = False

        if not (distance2 < thresholdDistance) and sensor2Triggered and not sensor1Triggered:
            sensor2Triggered = False

        time.sleep(debounceTime)

finally:
    tof1.stop()
    tof2.stop()