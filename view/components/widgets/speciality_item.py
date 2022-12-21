from datetime import datetime
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from view.components.forms.speciality_item import Ui_Form


class SpecialityItem(QWidget):
    def __init__(self, code: str, date: str, title: str, code_is_valid: bool, date_is_valid: bool, title_is_valid: bool,
                 on_delete: Callable):
        super().__init__()
        self.__form = Ui_Form()
        self.__form.setupUi(self)

        self.__form.code.setText(code)
        self.__form.code.setCursorPosition(0)

        self.__form.date.setDate(datetime.fromisoformat(date))

        self.__form.title.setText(title)
        self.__form.title.setCursorPosition(0)

        self.__form.delete_button.clicked.connect(on_delete)

        self.__form.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__form.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__form.date.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if not code_is_valid:
            self.__form.code.setStyleSheet("background-color: rgb(239, 41, 41);")
        if not date_is_valid:
            self.__form.date.setStyleSheet("background-color: rgb(239, 41, 41);")
        if not title_is_valid:
            self.__form.title.setStyleSheet("background-color: rgb(239, 41, 41);")

    @property
    def code(self):
        return self.__form.code.text().strip()

    @property
    def title(self):
        return self.__form.title.text().strip()

    @property
    def date(self):
        return "-".join(self.__form.date.text().split(".")[::-1])

    def change_code_is_valid(self, is_valid):
        if is_valid:
            self.__form.code.setStyleSheet("background-color: rgb(138, 226, 52);")
        else:
            self.__form.code.setStyleSheet("background-color: rgb(239, 41, 41);")

    def change_date_is_valid(self, is_valid):
        if is_valid:
            self.__form.date.setStyleSheet("background-color: rgb(138, 226, 52);")
        else:
            self.__form.date.setStyleSheet("background-color: rgb(239, 41, 41);")

    def change_title_is_valid(self, is_valid):
        if is_valid:
            self.__form.title.setStyleSheet("background-color: rgb(138, 226, 52);")
        else:
            self.__form.title.setStyleSheet("background-color: rgb(239, 41, 41);")
