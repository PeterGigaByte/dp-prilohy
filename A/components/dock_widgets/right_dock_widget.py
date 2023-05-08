from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QDockWidget


class RightDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(RightDockWidget, self).__init__("Chart", parent)
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        list_widget = QListWidget()
        list_widget.addItems(['Chart 1', 'Chart 2', 'Chart 3'])
        self.setWidget(list_widget)