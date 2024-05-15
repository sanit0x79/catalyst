import time
import VL53L0X

# Initialiseer de sensoren
sensor1 = VL53L0X(address=0x29)
sensor2 = VL53L0X(address=0x30)

sensor1.open()
sensor2.open()

sensor1.start_ranging()
sensor2.start_ranging()

# Stel de drempelwaarde in voor detectie
threshold = 400  # in millimeters

# Variabele voor het bijhouden van het aantal personen
person_count = 0

# Status van de sensoren
sensor1_triggered = False
sensor2_triggered = False

try:
    while True:
        # Lees de afstand van de sensoren
        distance1 = sensor1.get_distance()
        distance2 = sensor2.get_distance()

        # Controleer of sensor 1 wordt getriggerd
        if distance1 < threshold:
            sensor1_triggered = True
        elif sensor1_triggered and distance1 > threshold:
            # Sensor 1 is niet langer getriggerd
            sensor1_triggered = False

            # Controleer of sensor 2 kort daarna wordt getriggerd
            if sensor2_triggered:
                person_count += 1
                sensor2_triggered = False
                print("Iemand ging naar binnen, totaal aantal personen:", person_count)

        # Controleer of sensor 2 wordt getriggerd
        if distance2 < threshold:
            sensor2_triggered = True
        elif sensor2_triggered and distance2 > threshold:
            # Sensor 2 is niet langer getriggerd
            sensor2_triggered = False

            # Controleer of sensor 1 kort daarna wordt getriggerd
            if sensor1_triggered:
                person_count -= 1
                sensor1_triggered = False
                print("Iemand ging naar buiten, totaal aantal personen:", person_count)

        # Wacht even voordat je opnieuw meet
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programma gestopt door gebruiker")

finally:
    sensor1.stop_ranging()
    sensor2.stop_ranging()
    sensor1.close()
    sensor2.close()