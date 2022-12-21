from typing import Callable

from PyQt5.QtWidgets import QWidget

from view.components.forms.search_item import Ui_Form


class SearchItem(QWidget):
    def __init__(self, title: str, on_delete: Callable):
        super().__init__()
        self.__form = Ui_Form()
        self.__form.setupUi(self)
        self.__form.title.setText(title)
        self.__form.title.setCursorPosition(0)
        self.__form.delete_button.clicked.connect(on_delete)

    @property
    def title(self):
        return self.__form.title.text().strip()
    def change_text(self, text):
        self.__form.title.setText(text)
        self.__form.title.setCursorPosition(0)
