"""
Основной модуль.
Создаёт объект класса Окна и запускает его.
"""
from app import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())

if __name__ == "__main__":
    main()