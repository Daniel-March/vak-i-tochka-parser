import typing

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QCheckBox, QLayout, QProgressBar

from view.logic import Logic
from view.ui import UI

if typing.TYPE_CHECKING:
    from view.ui.actions import Actions


class TabObjects:
    def __init__(self, ui: UI):
        self.__ui = ui

    @property
    def journals_link(self) -> QLineEdit:
        return self.__ui.main_window.journals_link

    @property
    def passports_link(self) -> QLineEdit:
        return self.__ui.main_window.passports_link

    @property
    def parse_journals(self) -> QCheckBox:
        return self.__ui.main_window.parse_journals

    @property
    def parse_passports(self) -> QCheckBox:
        return self.__ui.main_window.parse_passports

    @property
    def start_parsing(self) -> QPushButton:
        return self.__ui.main_window.start_parsing

    @property
    def parsing_notifier(self) -> QLayout:
        return self.__ui.main_window.parsing_notifier

    @property
    def journals_progress(self) -> QProgressBar:
        return self.__ui.main_window.journals_progress

    @property
    def passports_progress(self) -> QProgressBar:
        return self.__ui.main_window.passports_progress


class ParsingPageActions(QObject):
    __notifier = pyqtSignal(str)

    def __init__(self, actions: "Actions", ui: UI, logic: Logic):
        super().__init__()
        self.__thread_pool = QtCore.QThreadPool()
        self.__ui = ui
        self.__logic = logic
        self.__actions = actions

        self.__objects = TabObjects(ui)

        self.__objects.start_parsing.clicked.connect(self.parse)
        self.__notifier.connect(self.create_notification)

    @property
    def journals_link(self) -> str:
        return self.__objects.journals_link.text()

    @property
    def passports_link(self) -> str:
        return self.__objects.passports_link.text()

    @property
    def parse_journals(self) -> bool:
        return self.__objects.parse_journals.checkState() == 2

    @property
    def parse_passports(self) -> bool:
        return self.__objects.parse_passports.checkState() == 2

    @property
    def journals_progress(self) -> QProgressBar:
        return self.__objects.journals_progress

    @property
    def passports_progress(self) -> QProgressBar:
        return self.__objects.passports_progress

    def parse(self) -> None:
        self.__actions.parse(self.__notifier)

    def create_notification(self, text: str) -> None:
        self.__objects.parsing_notifier.addWidget(QLabel(text))
