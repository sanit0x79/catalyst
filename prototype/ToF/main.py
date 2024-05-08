import time
from machine import I2C, Pin
import VL53L0X

SCL_PIN = 22
SDA_PIN = 21

i2c = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))

tof = VL53L0X.VL53L0X(i2c)

tof.start()

previousDistance = tof.read()
peopleCount = 0
personInRoom = False

try:
    while True:
        distance = tof.read()
        
        if distance < 500:
            peopleCount += 1
            personInRoom = True
            print("Person entered. Count:", peopleCount)
        
        #if distance > 100 and person_in_room:
        #    personInRoom = False
        #    print("Person left. Count:", people_count)
        
        time.sleep(0.3) 

finally:
    tof.stop()