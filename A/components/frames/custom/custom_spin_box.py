from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QSpinBox


class CustomLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(CustomLineEdit, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        super(CustomLineEdit, self).mousePressEvent(event)
        self.clicked.emit()


class CustomSpinBox(QSpinBox):
    editingStarted = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(CustomSpinBox, self).__init__(*args, **kwargs)
        self.setLineEdit(CustomLineEdit())  # Set the custom QLineEdit
        self.lineEdit().clicked.connect(self.editingStarted.emit)  # Connect the clicked signal_object

    def focusInEvent(self, event):
        super(CustomSpinBox, self).focusInEvent(event)
