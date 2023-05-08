from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSlider


class CustomSlider(QSlider):
    sliderPressed = pyqtSignal()
    sliderReleased = pyqtSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.sliderPressed.emit()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.sliderReleased.emit()
