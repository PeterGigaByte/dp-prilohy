from PyQt5.QtWidgets import QMessageBox


def show_tutorial():
    """Show tutorial for application."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Generate files via scripts using NS-3\n" +
                "1. Select XML/JSON file to be visualised.\n" +
                "2. Start simulation with play button or pause it.")
    msg.setWindowTitle("Tutorial")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()