import json
import os.path
import threading
from uuid import uuid4

import requests

from view.logic import Logic
from view.ui import UI
from view.ui.actions.actions_page_actions import ActionsPageActions
from view.ui.actions.journals_page_actions import JournalsPageActions
from view.ui.actions.parsing_page_actions import ParsingPageActions
from view.ui.actions.passports_page_actions import PassportsPageActions


class Actions:
    def __init__(self, ui: UI, logic: Logic):
        self.__ui = ui
        self.__logic = logic

        self.__journals = JournalsPageActions(ui=ui,
                                              actions=self,
                                              logic=logic)
        self.__passports = PassportsPageActions(ui=ui,
                                                actions=self,
                                                logic=logic)
        self.__actions = ActionsPageActions(ui=ui,
                                            actions=self,
                                            logic=logic)
        self.__parsing = ParsingPageActions(actions=self,
                                            ui=ui,
                                            logic=logic)

    def import_journals(self):
        self.__journals.set_journals(self.__logic.load_journals())

    def save_journals(self, notifier):
        self.__logic.save_journals(self.__journals.journals)
        notifier.emit("Журналы сохранены успешно")

    def save_passports(self, notifier):
        self.__logic.save_passports(areas=self.__passports.areas,
                                    groups=self.__passports.groups,
                                    passports=self.__passports.passports)
        notifier.emit("Паспорта сохранены успешно")

    def convert_journals(self, notifier):
        self.__logic.convert_journals(self.__journals.journals)
        notifier.emit("Журналы конвертированы успешно")

    def convert_passports(self, notifier):
        self.__logic.convert_passports(areas=self.__passports.areas,
                                       groups=self.__passports.groups,
                                       passports=self.__passports.passports)
        notifier.emit("Паспорта конвертированы успешно")

    def import_passports(self):
        self.__passports.set_areas(sorted(self.__logic.load_areas(), key=lambda x: x.code))
        self.__passports.set_groups(sorted(self.__logic.load_groups(), key=lambda x: x.area * 1000 + x.code))
        self.__passports.set_passports(
            sorted(self.__logic.load_passports(), key=lambda x: x.area * 1000000 + x.group * 1000 + x.code))

    def parse(self, notifier):
        journals_link = self.__parsing.journals_link
        passports_link = self.__parsing.passports_link

        if self.__parsing.parse_journals:
            threading.Thread(target=self.__logic.parse_journals,
                             kwargs={"link": journals_link if journals_link != "" else None,
                                     "progress_bar": self.__parsing.journals_progress,
                                     "notifier": notifier}).start()
        if self.__parsing.parse_passports:
            threading.Thread(target=self.__logic.parse_passports,
                             kwargs={"link": passports_link if passports_link != "" else None,
                                     "progress_bar": self.__parsing.passports_progress,
                                     "notifier": notifier}).start()

    def upload_journals(self, notifier):
        notifier.emit("Начата отправка журналов")
        if not os.path.exists(os.path.join(self.__logic.app.config.paths.output,
                                           self.__logic.app.config.names.output_journals_json)):
            notifier.emit("Начата конвертация журналов")
            self.convert_journals(notifier)
        with open(os.path.join(self.__logic.app.config.paths.output,
                               self.__logic.app.config.names.output_journals_json), "r") as file:
            data_json = json.loads(file.read())["data"]
        operation_uuid = uuid4().hex
        while len(data_json) > 0:
            r = requests.post(self.__actions.journals_uploading_link,
                              data={"json": json.dumps({"data": data_json[:200]}).encode(),
                                    "operation_uuid": operation_uuid},
                              cookies={"session_key": self.__actions.secret_key})
            data_json = data_json[200:]
            notifier.emit(f"Часть журналов отправлена. Осталось {len(data_json)}. Ответ сервера: {str(r.text)}")
        notifier.emit("Отправка журналов завершена")

    def upload_passports(self, notifier):
        notifier.emit("Начата отправка паспортов")
        if not os.path.exists(os.path.join(self.__logic.app.config.paths.output,
                                           self.__logic.app.config.names.output_passports_json)):
            notifier.emit("Начата конвертация паспортов")
            self.convert_passports(notifier)
        r = requests.post(self.__actions.passports_uploading_link,
                          data={"json": open(os.path.join(self.__logic.app.config.paths.output,
                                                          self.__logic.app.config.names.output_passports_json), "rb")},
                          cookies={"session_key": self.__actions.secret_key})
        notifier.emit(f"Ответ сервера: {str(r.text)}")
        notifier.emit("Отправка паспортов завершена")
