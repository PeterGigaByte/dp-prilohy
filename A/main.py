import sys

from PyQt5.QtWidgets import QApplication

from environment import Environment

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Environment()
    main_window.show()
    sys.exit(app.exec_())
