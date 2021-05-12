import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime
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
        self.setWindowIcon(QtGui.QIcon('timer_icon.png'))

        self.sw = SettingsWindow()

        # Timer
        self.timer = QTimer(self)
        self.time_label = QLabel(self)
        self.time_label.move(300, 150)
        self.timer.timeout.connect(self.show_time)

        # Default time settings
        self.break_seconds = 300
        self.work_seconds = 900
        self.current_countdown = 0

        # Sets label's default value to the default work time
        m, s = divmod(self.work_seconds, 60)
        self.time_label.setText(f'{m:02d}:{s:02d}')
        self.current_countdown = self.work_seconds

        # Settings Button
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.move(635, 10)
        self.settings_button.clicked.connect(self.settings_button_clicked)

        # Work Toggle Button
        self.work_button = QPushButton("Work", self)
        self.work_button.move(250, 50)
        self.work_button.clicked.connect(self.work_button_clicked)

        # Break Toggle Button
        self.break_button = QPushButton("Break", self)
        self.break_button.move(400, 50)
        self.break_button.clicked.connect(self.break_button_clicked)

        # Start Button
        self.start_stop_button = QPushButton("Start", self)
        self.start_stop_button.move(350, 450)
        self.start_stop_button.clicked.connect(self.start_stop_button_clicked)

    def start_stop_button_clicked(self):
        if self.start_stop_button.text() == "Start":
            self.timer.start(1000)
            self.start_stop_button.setText("Stop")
        else:
            self.timer.stop()
            self.start_stop_button.setText("Start")

    def show_time(self):
        self.update_time_label()
        self.current_countdown -= 1

    def update_time_label(self):
        m, s = divmod(self.current_countdown, 60)
        self.time_label.setText(f'{m:02d}:{s:02d}')

    def settings_button_clicked(self):
        """Creates the settings window and shows it."""
        self.sw.show()

    def work_button_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_stop_button.setText("Start")
        self.current_countdown = self.work_seconds
        self.update_time_label()

    def break_button_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_stop_button.setText("Start")
        self.current_countdown = self.break_seconds
        self.update_time_label()

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