import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget
from PyQt5.QtCore import Qt


def window():
    app = QApplication(sys.argv)
    widget = QWidget()
    button1 = QPushButton(widget)
    button1.setText("Button1")
    button1.move(64, 32)
    button1.clicked.connect(button1_clicked)

    widget.setGeometry(50, 50, 320, 200)
    widget.setWindowTitle("PyQt5 Button Click Example")
    widget.show()
    sys.exit(app.exec_())


def button1_clicked():
    print("Button 1 clicked")


if __name__ == '__main__':
    window()