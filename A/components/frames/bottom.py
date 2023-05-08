from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel


class BottomFrame(QFrame):
    def __init__(self, parent=None):
        super(BottomFrame, self).__init__(parent)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        self.time_label = QLabel()
        layout.addWidget(self.time_label)
        self.setLayout(layout)

        # Initialize the timer and connect it to update_time_label method
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(1000)

    def update_time_label(self):
        """Update the time label with the current time."""
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(f"Current Time: {current_time}")
