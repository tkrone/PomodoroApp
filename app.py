import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QVBoxLayout, QSlider, QGridLayout
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, pyqtSignal, pyqtSlot

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

        layout = QGridLayout()

        # Timer
        self.timer = QTimer(self)
        self.time_label = QLabel(self)
        self.time_label.setFont(QFont('Times', 35))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("background-color: Bisque; "
                                   "border: 1px solid black;")
        self.timer.timeout.connect(self.show_time)

        # Default time settings
        self.break_seconds = 300
        self.work_seconds = 900

        # Sets label's default value to the default work time
        m, s = divmod(self.work_seconds, 60)
        self.time_label.setText(f'{m:02d}:{s:02d}')
        self.current_countdown = self.work_seconds

        # "work" represents we or on the work time counter, "break" represents we're on the break time counter
        self.mode = "work"

        # Settings Button
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.settings_button_clicked)

        # Work Toggle Button
        self.work_button = QPushButton("Work", self)
        self.work_button.clicked.connect(self.work_button_clicked)

        # Break Toggle Button
        self.break_button = QPushButton("Break", self)
        self.break_button.clicked.connect(self.break_button_clicked)

        # Start Button
        self.start_stop_button = QPushButton("Start", self)
        self.start_stop_button.clicked.connect(self.start_stop_button_clicked)

        layout.addWidget(self.settings_button, 0, 0, 1, 2)
        layout.addWidget(self.work_button, 1, 0)

        layout.addWidget(self.break_button, 1, 1)
        layout.addWidget(self.time_label, 2, 0, 1, 2)
        layout.addWidget(self.start_stop_button, 3, 0, 1, 2)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_stop_button_clicked(self):
        """Toggles between start and stop. Stops timer if it's running, starts it if it's not."""
        if self.start_stop_button.text() == "Start":
            self.timer.start(1000)
            self.start_stop_button.setText("Stop")
        else:
            self.timer.stop()
            self.start_stop_button.setText("Start")

    def show_time(self):
        """Every second that is passed, decrements current_countdown and updates the time label"""
        self.update_time_label()
        self.current_countdown -= 1

    def update_time_label(self):
        """changes the amount of seconds left on the timer to minutes:seconds format and updates the time
        label."""
        m, s = divmod(self.current_countdown, 60)
        self.time_label.setText(f'{m:02d}:{s:02d}')

    def settings_button_clicked(self):
        """Creates the settings window and shows it."""
        self.sw = SettingsWindow()
        self.sw.time_change.connect(self.update_time)
        self.sw.show()

    def work_button_clicked(self):
        """Sets/Resets the second count to the amount of work seconds specified by the settings. Updates the time
        label. Stops the timer if it was running"""
        if self.timer.isActive():
            self.timer.stop()
            self.start_stop_button.setText("Start")
        self.current_countdown = self.work_seconds
        self.update_time_label()
        mode = "work"

    def break_button_clicked(self):
        """Sets/Resets the second count to the amount of break seconds specified by the settings. Updates the time
        label. Stops the timer if it was running"""
        if self.timer.isActive():
            self.timer.stop()
            self.start_stop_button.setText("Start")
        self.current_countdown = self.break_seconds
        self.update_time_label()
        self.mode = "break"

    def closeEvent(self, event):
        """Closes the settings window if it is open upon closing."""
        self.sw.close()

    def update_time(self, work_time, break_time):
        self.work_seconds = int(work_time) * 60
        self.break_seconds = int(break_time) * 60

        if self.mode == "work":
            self.current_countdown = self.work_seconds
        else:
            self.current_countdown = self.break_seconds
        print(self.current_countdown)

        self.update_time_label()


class SettingsWindow(QWidget):
    """Contains the widgets that allow for editing the timer lengths for break and work periods."""

    time_change = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setMinimumSize(QSize(600, 150))
        self.setWindowTitle("Pomodoro Timer")
        self.setWindowIcon(QtGui.QIcon('timer_icon.png'))

        self.work_slider = QSlider(Qt.Horizontal)
        self.work_slider.setMaximum(60)
        self.work_slider.setValue(15)
        self.work_slider.setTickPosition(QSlider.TicksBelow)
        self.work_slider.setTickInterval(5)
        self.work_slider.valueChanged.connect(self.work_value_change)

        self.work_label = QLabel("Work")
        self.work_label.setAlignment(Qt.AlignCenter)
        self.work_label.setStyleSheet("font-weight: bold;")
        self.work_time_label = QLabel(str(self.work_slider.value()))

        self.break_slider = QSlider(Qt.Horizontal)
        self.break_slider.setMaximum(60)
        self.break_slider.setValue(5)
        self.break_slider.setTickPosition(QSlider.TicksBelow)
        self.break_slider.setTickInterval(5)
        self.break_slider.valueChanged.connect(self.break_value_change)

        self.break_label = QLabel("Break")
        self.break_label.setAlignment(Qt.AlignCenter)
        self.break_label.setStyleSheet("font-weight: bold;")
        self.break_time_label = QLabel(str(self.break_slider.value()))

        self.apply_button = QPushButton("Apply", self)
        self.apply_button.clicked.connect(self.apply_button_clicked)

        layout.addStretch()
        layout.addWidget(self.work_label)
        layout.addWidget(self.work_time_label)
        layout.addWidget(self.work_slider)
        layout.addWidget(self.break_label)
        layout.addWidget(self.break_time_label)
        layout.addWidget(self.break_slider)
        layout.addWidget(self.apply_button)
        layout.setSpacing(5)
        self.setLayout(layout)

    def work_value_change(self):
        self.work_time_label.setText(str(self.work_slider.value()))

    def break_value_change(self):
        self.break_time_label.setText(str(self.break_slider.value()))

    def apply_button_clicked(self):
        self.time_change.emit(self.work_time_label.text(), self.break_time_label.text())

app = QApplication(sys.argv)
w = MainWindow()
app.MainWindow = w
w.show()
app.exec_()