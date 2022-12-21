import typing
from enum import Enum
from functools import partial
from uuid import uuid4

from PyQt5.QtWidgets import QLineEdit, QLabel

from app.utils import through
from view.components.widgets import ListButton, SpecialityItem
from view.logic import Logic, Journal, Speciality
from view.ui import UI

if typing.TYPE_CHECKING:
    from view.ui.actions import Actions


class FilterTypes(Enum):
    values_type = int
    ISSN = 0
    TITLE = 1


class TabObjects:  # ToDo Add typing
    def __init__(self, ui: UI):
        self.__ui = ui

    @property
    def list(self):
        return self.__ui.main_window.journals_list

    @property
    def amount(self) -> QLabel:
        return self.__ui.main_window.amount_of_journals

    @property
    def title(self) -> QLineEdit:
        return self.__ui.main_window.journal_title

    @property
    def issn(self) -> QLineEdit:
        return self.__ui.main_window.journal_issn

    @property
    def is_valid_filter(self):
        return self.__ui.main_window.journals_type_combo_box

    @property
    def filter_type(self):
        return self.__ui.main_window.filter_combo_box

    @property
    def filter_statement(self) -> QLineEdit:
        return self.__ui.main_window.filter_statement

    @property
    def filter(self):
        return self.__ui.main_window.filter_button

    @property
    def specialities(self):
        return self.__ui.main_window.journal_specialities_list

    @property
    def add_speciality(self):
        return self.__ui.main_window.add_journal_speciality

    @property
    def new_journal(self):
        return self.__ui.main_window.add_journal

    @property
    def save_journal(self):
        return self.__ui.main_window.save_journal

    @property
    def delete_journal(self):
        return self.__ui.main_window.delete_journal


class JournalsList:
    def __init__(self, objects: TabObjects, page: "JournalsPageActions"):
        self.__objects: TabObjects = objects
        self.__page: JournalsPageActions = page
        self.__filter = self.Filter(objects=objects, page=page)
        self.__items: dict[str, ListButton] = {}

        self.__objects.new_journal.clicked.connect(self.__page.new_journal)

    def add(self, uuid: str, journal: Journal) -> None:
        if uuid in self.__items.keys():
            self.change(uuid=uuid, journal=journal)
            return
        self.__items[uuid] = ListButton(text=str(journal),
                                        on_click=partial(self.__page.open_journal, uuid=uuid),
                                        is_valid=journal.is_valid)
        self.__objects.list.addWidget(self.__items[uuid])
        self.__objects.amount.setText(str(len(self.__items)))

    def change(self, uuid: str, journal: Journal) -> None:
        self.__items[uuid].change_text(str(journal))
        self.__items[uuid].change_is_valid(journal.is_valid)

    def delete(self, uuid: str) -> None:
        if uuid in self.__items.keys():
            self.__items[uuid].setParent(None)
            self.__objects.list.removeWidget(self.__items[uuid])
            del self.__items[uuid]
        self.__objects.amount.setText(str(len(self.__items)))

    def clear(self) -> None:
        for uuid in list(self.__items.keys()):
            self.delete(uuid)
        self.__objects.amount.setText(str(len(self.__items)))

    class Filter:
        def __init__(self, objects: TabObjects, page: "JournalsPageActions"):
            self.__objects: TabObjects = objects
            self.__page: JournalsPageActions = page

            self.__objects.filter.clicked.connect(self.filter)

        def filter(self):
            match self.__objects.is_valid_filter.currentIndex():
                case 1:
                    is_valid = True
                case 2:
                    is_valid = False
                case _:
                    is_valid = None
            filter_type = FilterTypes(self.__objects.filter_type.currentIndex())
            filter_statement = self.__objects.filter_statement.text()
            self.__page.filter(is_valid=is_valid,
                               filter_type=filter_type,
                               filter_statement=filter_statement)


class JournalInfo:
    def __init__(self, objects: TabObjects, page: "JournalsPageActions"):
        self.__objects: TabObjects = objects
        self.__page: JournalsPageActions = page
        self.__specialities = self.SpecialitiesList(objects=self.__objects,
                                                    page=self.__page)
        self.disable()

    def save(self, uuid: str):
        self.__page.change_journal(uuid=uuid,
                                   journal=Journal(issn=self.__objects.issn.text(),
                                                   title=self.__objects.title.text(),
                                                   specialities=self.__specialities.specialities))

    def set(self, uuid: str, journal: Journal) -> None:
        self.enable()
        self.__objects.title.setText(journal.title)
        self.__objects.title.setCursorPosition(0)
        self.__objects.issn.setText(journal.issn)
        self.__specialities.clear()

        for speciality in journal.specialities:
            self.__specialities.add(speciality)

        through(func=self.__objects.save_journal.clicked.disconnect)
        self.__objects.save_journal.clicked.connect(partial(self.save, uuid=uuid))

        through(func=self.__objects.delete_journal.clicked.disconnect)
        self.__objects.delete_journal.clicked.connect(partial(self.__page.remove_journal, uuid=uuid))

        if journal.title_is_valid:
            self.__objects.title.setStyleSheet("")
        else:
            self.__objects.title.setStyleSheet("background-color: rgb(239, 41, 41);")

        if journal.issn_is_valid:
            self.__objects.issn.setStyleSheet("")
        else:
            self.__objects.issn.setStyleSheet("background-color: rgb(239, 41, 41);")

    def new(self) -> None:
        def inner():
            uuid = self.__page.add_journal(Journal(issn=self.__objects.issn.text(),
                                                   title=self.__objects.title.text(),
                                                   specialities=self.__specialities.specialities))
            self.__page.open_journal(uuid)

        self.clear()
        through(func=self.__objects.save_journal.clicked.disconnect)
        self.__objects.save_journal.clicked.connect(partial(inner))

        through(func=self.__objects.delete_journal.clicked.disconnect)
        self.enable()

    def clear(self) -> None:
        self.__objects.title.setText("")
        self.__objects.issn.setText("")
        self.__specialities.clear()

        self.__objects.title.setStyleSheet("")
        self.__objects.issn.setStyleSheet("")

    def disable(self) -> None:
        self.__objects.title.setEnabled(False)
        self.__objects.issn.setEnabled(False)
        self.__objects.add_speciality.setEnabled(False)
        self.__objects.save_journal.setEnabled(False)
        self.__objects.delete_journal.setEnabled(False)

    def enable(self) -> None:
        self.__objects.title.setEnabled(True)
        self.__objects.issn.setEnabled(True)
        self.__objects.add_speciality.setEnabled(True)
        self.__objects.save_journal.setEnabled(True)
        self.__objects.delete_journal.setEnabled(True)

    class SpecialitiesList:
        def __init__(self, objects: TabObjects, page: "JournalsPageActions"):
            self.__objects: TabObjects = objects
            self.__page: JournalsPageActions = page

            self.__items: dict[str, SpecialityItem] = {}

            self.__objects.add_speciality.clicked.connect(self.new)

        @property
        def specialities(self) -> list[Speciality]:
            return [Speciality(title=speciality.title,
                               code=speciality.code,
                               date=speciality.date) for speciality in self.__items.values()]

        def add(self, speciality: Speciality) -> None:
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = SpecialityItem(code=speciality.code,
                                                date=speciality.date,
                                                title=speciality.title,
                                                code_is_valid=speciality.code_is_valid,
                                                date_is_valid=speciality.date_is_valid,
                                                title_is_valid=speciality.title_is_valid,
                                                on_delete=partial(self.delete, uuid=uuid))
            self.__objects.specialities.addWidget(self.__items[uuid])

        def new(self):
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = SpecialityItem(code="",
                                                date="1800-12-12",
                                                title="",
                                                code_is_valid=True,
                                                date_is_valid=True,
                                                title_is_valid=True,
                                                on_delete=partial(self.delete, uuid=uuid))
            self.__objects.specialities.addWidget(self.__items[uuid])

        def delete(self, uuid: str) -> None:
            if uuid in self.__items.keys():
                self.__items[uuid].setParent(None)
                self.__objects.specialities.removeWidget(self.__items[uuid])
                del self.__items[uuid]

        def clear(self) -> None:
            for uuid in list(self.__items.keys()):
                self.delete(uuid)


class JournalsPageActions:
    def __init__(self, actions: "Actions", ui: UI, logic: Logic):
        self.__ui = ui
        self.__logic = logic
        self.__actions = actions

        self.__journals: dict[str, Journal] = {}
        self.__objects = TabObjects(ui)

        self.__list = JournalsList(objects=self.__objects, page=self)
        self.__info = JournalInfo(objects=self.__objects, page=self)

    @property
    def journals(self) -> list[Journal]:
        return list(self.__journals.values())

    def set_journals(self, journals: list[Journal], reload: bool = True) -> None:
        self.__list.clear()
        for journal in journals:
            self.add_journal(journal, reload)

    def add_journal(self, journal: Journal, reload: bool = True) -> str:
        uuid = uuid4().hex
        while uuid in self.__journals.keys():
            uuid = uuid4().hex
        self.__journals[uuid] = journal
        if reload:
            self.__list.add(uuid=uuid, journal=journal)
        return uuid

    def new_journal(self):
        self.__info.new()

    def open_journal(self, uuid: str):
        self.__info.set(uuid=uuid, journal=self.__journals[uuid])

    def filter(self, is_valid: typing.Optional[bool], filter_type: FilterTypes.values_type, filter_statement: str):
        self.__list.clear()
        self.__info.clear()
        self.__info.disable()

        for uuid, journal in self.__journals.items():
            if journal.is_valid != is_valid and is_valid is not None:
                continue
            if len(filter_statement.strip()) != 0:
                if filter_type == FilterTypes.ISSN:
                    if filter_statement.lower() != journal.issn.lower():
                        continue
                elif filter_type == FilterTypes.TITLE:
                    if filter_statement.lower() not in journal.title.lower():
                        continue
            self.__list.add(uuid=uuid, journal=journal)

    def change_journal(self, uuid: str, journal: Journal, reload: bool = True):
        self.__journals[uuid] = journal
        if reload:
            self.__list.change(uuid=uuid, journal=journal)
        self.open_journal(uuid)

    def remove_journal(self, uuid: str, reload: bool = True):
        if uuid in self.__journals.keys():
            del self.__journals[uuid]
        if reload:
            self.__list.delete(uuid)
        self.__info.clear()
        self.__info.disable()
