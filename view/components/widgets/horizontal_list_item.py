from typing import Callable

from PyQt5.QtWidgets import QWidget

from view.components.forms.horizontal_list_item import Ui_Form


class HorizontalListItem(QWidget):
    def __init__(self, text: str, on_delete: Callable, is_long: bool = False):
        super().__init__()
        self.__form = Ui_Form()
        self.__form.setupUi(self)
        self.__form.title.setText(text)
        self.__form.title.setCursorPosition(0)
        self.__form.delete_button.clicked.connect(on_delete)
        if is_long:
            self.__form.title.setMinimumSize(250, 0)

    @property
    def title(self):
        return self.__form.title.text().strip()

    def change_text(self, text):
        self.__form.title.setText(text)
        self.__form.title.setCursorPosition(0)
