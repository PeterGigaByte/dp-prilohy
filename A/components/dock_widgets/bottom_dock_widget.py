from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QTextEdit, QScrollArea

from utils.dateUtils import get_current_time


class BottomDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(BottomDockWidget, self).__init__("Log", parent)
        self.setAllowedAreas(Qt.BottomDockWidgetArea)

        self.textbox = QTextEdit()
        init_text = get_current_time() + " - Application initialized"
        self.textbox.append(init_text)
        self.textbox.setReadOnly(True)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.textbox)
        scroll_area.setWidgetResizable(True)

        self.setWidget(scroll_area)

    def log(self, text):
        """Append a log message to the textbox."""
        self.textbox.append(get_current_time() + " - " + text)
        print(get_current_time() + " - " + text)
