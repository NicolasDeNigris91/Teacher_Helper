# main.py
import sys
from PyQt6.QtWidgets import QApplication
from main_window import StudentManagerSystem

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentManagerSystem()
    window.show()
    sys.exit(app.exec())