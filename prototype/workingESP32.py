import machine
import time

# Initialiseren van de pins op de ESP32
pirPlusPin = 23
pirMinPin = 24

# Initialiseren van de input die wij de sensoren geven
pirPlus = machine.Pin(pirPlusPin, machine.Pin.IN)
pirMin = machine.Pin(pirMinPin, machine.Pin.IN)

# Initialiseren van de tellers
binnenkomstTal = 0
verlaatTal = 0
mensenTal = 0
binnenkomstStatus = 0
verlaatStatus = 0

print("PiR sensor telt nu voor mensen, druk op Ctrl+C om het programma te verlaten")

try:
    while True:
        # Leest huidige status van binnenkomst en verlaat sensoren
        binnenkomstStatus = pirPlus.value()
        verlaatStatus = pirMin.value()
        
        # Update het aantal mensen door het bekijken van de voltages van de sensoren
        if binnenkomstStatus == 1:
            binnenkomstTal += 1
            time.sleep(0.5) # Er is hier een delay toegevoegd om miscalculatie te voorkomen
        elif verlaatStatus == 1:
            if binnenkomstTal > 0:
                binnenkomstTal -= 1
            verlaatTal += 1
            time.sleep(0.5) # Delay toegevoegd om miscalculatie te voorkomen

        mensenTal = binnenkomstTal - verlaatTal

        print(f"Totale mensen in zicht: {mensenTal}")
        
        # Software wacht hier zeer kort om verkeerde detecties te voorkomen
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programma wordt afgesloten")
