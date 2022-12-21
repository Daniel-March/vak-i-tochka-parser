from typing import Callable

from PyQt5.QtWidgets import QWidget

from view.components.forms.area_item import Ui_Form


class AreaItem(QWidget):
    def __init__(self, code: int, title: str, on_delete: Callable, title_is_valid: bool, code_is_valid: bool,
                 on_change: Callable):
        super().__init__()
        self.__form = Ui_Form()
        self.__form.setupUi(self)
        self.__form.code.setValue(code)
        self.__form.title.setText(title)
        self.__form.title.setCursorPosition(0)

        self.__form.delete_area.clicked.connect(on_delete)
        self.__form.title.textChanged.connect(on_change)
        self.__form.code.valueChanged.connect(on_change)

        if title_is_valid:
            self.__form.title.setStyleSheet("")
        else:
            self.__form.title.setStyleSheet("background-color: rgb(239, 41, 41);")
        if code_is_valid:
            self.__form.code.setStyleSheet("")
        else:
            self.__form.code.setStyleSheet("background-color: rgb(239, 41, 41);")

    @property
    def code(self):
        return int(self.__form.code.text())

    @property
    def title(self):
        return self.__form.title.text()

    def change_title_is_valid(self, is_valid: bool):
        if is_valid:
            self.__form.title.setStyleSheet("")
        else:
            self.__form.title.setStyleSheet("background-color: rgb(239, 41, 41);")

    def change_code_is_valid(self, is_valid: bool):
        if is_valid:
            self.__form.code.setStyleSheet("")
        else:
            self.__form.code.setStyleSheet("background-color: rgb(239, 41, 41);")

    def change_code(self, code: int):
        self.__form.code.setValue(code)

    def change_title(self, title: str):
        self.__form.title.setText(title)
