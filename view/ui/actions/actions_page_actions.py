import os
import threading
import typing

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QLayout

from view.logic import Logic
from view.ui import UI

if typing.TYPE_CHECKING:
    from view.ui.actions import Actions


class TabObjects:
    def __init__(self, ui: UI):
        self.__ui = ui

    @property
    def journals_temp_path(self) -> QLabel:
        return self.__ui.main_window.journals_temp_path

    @property
    def passports_temp_path(self) -> QLabel:
        return self.__ui.main_window.passports_temp_path

    @property
    def journals_final_path(self) -> QLabel:
        return self.__ui.main_window.journals_final_path

    @property
    def passports_final_path(self) -> QLabel:
        return self.__ui.main_window.passports_final_path

    @property
    def secret_key(self) -> QLineEdit:
        return self.__ui.main_window.secret_key

    @property
    def journals_uploading_link(self) -> QLineEdit:
        return self.__ui.main_window.journals_uploading_link

    @property
    def passports_uploading_link(self) -> QLineEdit:
        return self.__ui.main_window.passports_uploading_link

    @property
    def save_journals(self) -> QPushButton:
        return self.__ui.main_window.save_journals

    @property
    def save_passports(self) -> QPushButton:
        return self.__ui.main_window.save_passports

    @property
    def convert_journals(self) -> QPushButton:
        return self.__ui.main_window.convert_journals

    @property
    def convert_passports(self) -> QPushButton:
        return self.__ui.main_window.convert_passports

    @property
    def import_data(self) -> QPushButton:
        return self.__ui.main_window.import_data

    @property
    def upload_journals(self) -> QPushButton:
        return self.__ui.main_window.upload_journals

    @property
    def upload_passports(self) -> QPushButton:
        return self.__ui.main_window.upload_passports

    @property
    def actions_notifier(self) -> QLayout:
        return self.__ui.main_window.actions_notifier


class ActionsPageActions(QObject):
    __notifier = pyqtSignal(str)

    def __init__(self, actions: "Actions", ui: UI, logic: Logic):
        super().__init__()
        self.__ui = ui
        self.__logic = logic
        self.__actions = actions

        self.__objects = TabObjects(ui)

        self.__objects.save_journals.clicked.connect(self.save_journals)
        self.__objects.save_passports.clicked.connect(self.save_passports)

        self.__objects.convert_journals.clicked.connect(self.convert_journals)
        self.__objects.convert_passports.clicked.connect(self.convert_passports)

        self.__objects.import_data.clicked.connect(self.import_data)

        self.__objects.upload_journals.clicked.connect(self.upload_journals)
        self.__objects.upload_passports.clicked.connect(self.upload_passports)

        self.__notifier.connect(self.create_notification)

        self.__objects.passports_temp_path.setText(str(os.path.join(self.__logic.app.config.paths.output,
                                                                    self.__logic.app.config.names.temp_passports_json)))
        self.__objects.passports_final_path.setText(str(os.path.join(self.__logic.app.config.paths.output,
                                                                     self.__logic.app.config.names.output_passports_json)))

        self.__objects.journals_temp_path.setText(str(os.path.join(self.__logic.app.config.paths.output,
                                                                   self.__logic.app.config.names.temp_journals_json)))
        self.__objects.journals_final_path.setText(str(os.path.join(self.__logic.app.config.paths.output,
                                                                    self.__logic.app.config.names.output_journals_json)))

    @property
    def secret_key(self):
        return self.__objects.secret_key.text()

    @property
    def journals_uploading_link(self):
        return self.__objects.journals_uploading_link.text()

    @property
    def passports_uploading_link(self):
        return self.__objects.passports_uploading_link.text()

    def save_journals(self):
        self.__actions.save_journals(notifier=self.__notifier)

    def save_passports(self):
        self.__actions.save_passports(notifier=self.__notifier)

    def convert_journals(self):
        self.__actions.convert_journals(notifier=self.__notifier)

    def convert_passports(self):
        self.__actions.convert_passports(notifier=self.__notifier)

    def import_data(self):
        self.__actions.import_journals()
        self.__actions.import_passports()

    def create_notification(self, text: str):
        self.__objects.actions_notifier.addWidget(QLabel(text))

    def upload_journals(self):
        threading.Thread(target=self.__actions.upload_journals,
                         args=[self.__notifier]).start()

    def upload_passports(self):
        threading.Thread(target=self.__actions.upload_passports,
                         args=[self.__notifier]).start()
