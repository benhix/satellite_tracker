import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow


if __name__ == "__main__":
    app = QApplication((sys.argv))
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())