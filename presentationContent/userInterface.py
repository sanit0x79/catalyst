
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PeopleCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MensenTelling")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #ffffff;")

        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()

        self.countLabel = QLabel("Geen mensen in zicht")
        self.countLabel.setFont(QFont("Arial", 20))
        self.countLabel.setStyleSheet("color: #ff0000;")
        self.layout.addWidget(self.countLabel, alignment=Qt.AlignCenter)

        self.incrementButton = QPushButton("Voeg persoon aan teller toe")
        self.incrementButton.setStyleSheet("background-color: #ff0000; color: white; font-size: 16px; border-radius: 5px;")
        self.incrementButton.clicked.connect(self.incrementCount)
        self.layout.addWidget(self.incrementButton)

        self.decrementButton = QPushButton("Haal persoon weg")
        self.decrementButton.setStyleSheet("background-color: #ff0000; color: white; font-size: 16px; border-radius: 5px;")
        self.decrementButton.clicked.connect(self.decrementCount)
        self.layout.addWidget(self.decrementButton)

        self.centralWidget.setLayout(self.layout)

    def incrementCount(self):
        currentCount = int(self.countLabel.text().split(": ")[-1]) if ":" in self.countLabel.text() else 0
        newCount = currentCount + 1
        if newCount == 0:
            self.countLabel.setText("Geen mensen in zicht")
        else:
            self.countLabel.setText(f"Totale mensen in zicht: {newCount}")

    def decrementCount(self):
        currentCount = int(self.countLabel.text().split(": ")[-1]) if ":" in self.countLabel.text() else 0
        newCount = currentCount - 1
        if newCount == 0:
            self.countLabel.setText("Geen mensen in zicht")
        elif newCount > 0:
            self.countLabel.setText(f"Totale mensen in zicht: {newCount}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PeopleCounterApp()
    window.show()
    sys.exit(app.exec_())
