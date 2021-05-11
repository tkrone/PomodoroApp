import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
"""A desktop application that provides all tools necessary to use the pomodoro technique. These tools include a timer
to track you work periods, as well as a timer to track your break periods. The length of these periods are editable.
Once a timer is up, a sound is played to alert the user."""


class MainWindow(QMainWindow):
    """Provides the main timer, options for break and work timers, and the settings button that opens the settings
    window."""
    def __init__(self):
        """Sets the window's size and title. Places and adds functionality for all primary elements that are needed
        in the main window."""
        super().__init__()
        self.setMinimumSize(QSize(750, 500))
        self.setWindowTitle("Pomodoro Timer")

        self.sw = SettingsWindow()

        self.settings_button = QPushButton("Settings", self)
        self.settings_button.move(635, 10)
        self.settings_button.clicked.connect(self.settings_button_clicked)

    def settings_button_clicked(self):
        """Creates the settings window and shows it."""
        self.sw.show()

    def closeEvent(self, event):
        """Closes the settings window if it is open upon closing."""
        self.sw.close()


class SettingsWindow(QWidget):
    """Contains the widgets that allow for editing the timer lengths for break and work periods."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


app = QApplication(sys.argv)
w = MainWindow()
app.MainWindow = w
w.show()
app.exec_()