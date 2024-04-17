import machine
import time

pirSensorPin = 23

pirSensor = machine.Pin(pirSensorPin, machine.Pin.IN)

# Initialiseren van variabelen
mensenTal = 0
vorigeStatus = 0

print("PiR sensor telt nu voor mensen, druk op Ctrl+C om het programma te stoppen.")

try:
    while True:
        huidigeStatus = pirSensor.value()

        # Bekijk of de status van de sensor is veranderd van laag naar hoog met voltage van de sensor
        if huidigeStatus == 1 and vorigeStatus == 0:
            mensenTal += 1
            print(f"Persoon gedetecteerd. Totale personen: {mensenTal}")

        vorigeStatus = huidigeStatus

        time.sleep(0.1)
except KeyboardInterrupt:
    print("Programma wordt afgesloten")

