import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class PeopleCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MensenTelling")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #ffffff;")

        # Laad de connectie met de ESP32
        self.ser = serial.Serial('COM5', 115200, timeout=1)

        # Variabele voor de tellerwaarde
        self.countValue = 0

        # Timer voor het periodiek lezen van de ESP32
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.readFromESP32)
        self.timer.start(1000)  # Lees elke 1 seconde

        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()

        self.countLabel = QLabel("Geen mensen in zicht")
        self.countLabel.setFont(QFont("Arial", 20))
        self.countLabel.setStyleSheet("color: #ff0000;")
        self.layout.addWidget(self.countLabel, alignment=Qt.AlignCenter)

        self.countValueLabel = QLabel("0")
        self.countValueLabel.setFont(QFont("Arial", 20))
        self.countValueLabel.setStyleSheet("color: #0000ff;")
        self.layout.addWidget(self.countValueLabel, alignment=Qt.AlignCenter)

        self.centralWidget.setLayout(self.layout)

    def readFromESP32(self):
        while self.ser.in_waiting:
            response = self.ser.readline().decode('utf-8').strip()
            if response.startswith("+"):
                self.incrementCount()
            elif response.startswith("-"):
                self.decrementCount()
            else:
                self.updateCount(response)

    def incrementCount(self):
        self.countLabel.setText("Iemand is binnen gekomen")
        self.countValue += 1
        self.updateCountLabel()

    def decrementCount(self):
        self.countLabel.setText("Iemand is vertrokken")
        if self.countValue > 0:
            self.countValue -= 1
        self.updateCountLabel()

    def updateCount(self, response):
        self.countLabel.setText(f"Totale mensen in zicht: {response}")
        try:
            self.countValue = int(response.strip())
        except ValueError:
            print(f"Ongeldige waarde ontvangen van ESP32: {response}")
            self.countValue = 0
        self.updateCountLabel()


    def updateCountLabel(self):
        self.countValueLabel.setText(str(self.countValue))

    def closeEvent(self, event):
        self.timer.stop()
        self.ser.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PeopleCounterApp()
    window.show()
    sys.exit(app.exec_())
