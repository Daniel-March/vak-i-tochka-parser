from PyQt5.QtWidgets import QMainWindow, QApplication

from view.components.forms.main_window import Ui_MainWindow


class UI:
    def __init__(self):
        self.__application = QApplication([])
        self.__window = QMainWindow()
        self.__main_window = Ui_MainWindow()
        self.__main_window.setupUi(self.__window)

    @property
    def window(self):
        return self.__window

    @property
    def main_window(self):
        return self.__main_window

    @property
    def application(self):
        return self.__application
