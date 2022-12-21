from PyQt5.QtWidgets import QMainWindow

from view.components.forms.main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__form = Ui_MainWindow()
        self.__form.setupUi(self)
