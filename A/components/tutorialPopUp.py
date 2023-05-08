from PyQt5.QtWidgets import QMessageBox


def show_tutorial():
    """Show tutorial for application."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Generate files via scripts using NS-3\n" +
                "If some error appears try to delete local database file and try again and check if everything is "
                "correctly setup in settings (it is very important and allows you to avoid crashing of "
                "application). Do not forget to check 'use database' when using ElementTree parser and uncheck when "
                "not using database. Do not use any"
                "buttons while parsing or processing to avoid application from crashing.\n\n" +
                "1. Make sure everything is set up correctly in settings.\n" +
                "2. Select XML/JSON file to be visualised.\n" +
                "3. Click parse file from main menu.\n" +
                "4. Click process data from main menu.\n" +
                "5. Start simulation with play button or pause it.")
    msg.setWindowTitle("Tutorial")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()