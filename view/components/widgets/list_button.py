from typing import Callable

from PyQt5.QtWidgets import QWidget

from view.components.forms.list_button import Ui_Form


class ListButton(QWidget):
    def __init__(self, text: str, on_click: Callable, is_valid: bool):
        super().__init__()
        self.__form = Ui_Form()
        self.__form.setupUi(self)

        self.__form.button.setText(text)

        if is_valid:
            self.__form.button.setStyleSheet("text-align:left; background-color: rgb(138, 226, 52);")
        else:
            self.__form.button.setStyleSheet("text-align:left; background-color: rgb(239, 41, 41);")
        self.__form.button.clicked.connect(on_click)

    def change_text(self, text: str):
        self.__form.button.setText(text)

    def change_is_valid(self, is_valid: bool):
        if is_valid:
            self.__form.button.setStyleSheet("text-align:left; background-color: rgb(138, 226, 52);")
        else:
            self.__form.button.setStyleSheet("text-align:left; background-color: rgb(239, 41, 41);")
