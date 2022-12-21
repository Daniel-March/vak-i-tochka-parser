import typing
from enum import Enum
from functools import partial
from uuid import uuid4

from PyQt5.QtWidgets import QComboBox, QPushButton, QLineEdit, QLabel

from app.utils import through
from view.components.widgets import AreaItem, GroupItem, ListButton, SearchItem, HorizontalListItem
from view.logic import Logic, Area, Group, Passport
from view.ui import UI

if typing.TYPE_CHECKING:
    from view.ui.actions import Actions


class FilterTypes(Enum):
    values_type = int
    CODE = 0
    TITLE = 1
    DOUBLED = 2


class TabObjects:  # ToDo Add typing
    def __init__(self, ui: UI):
        self.__ui = ui

    @property
    def areas_list(self):
        return self.__ui.main_window.areas_list

    @property
    def new_area(self):
        return self.__ui.main_window.add_area

    @property
    def groups_is_valid_filter(self) -> QComboBox:
        return self.__ui.main_window.groups_combo_box

    @property
    def groups_list(self):
        return self.__ui.main_window.groups_list

    @property
    def new_group(self):
        return self.__ui.main_window.add_group

    @property
    def passports_is_valid_filter(self) -> QComboBox:
        return self.__ui.main_window.passports_combo_box

    @property
    def filter(self) -> QPushButton:
        return self.__ui.main_window.passports_filter_button

    @property
    def filter_statement(self) -> QLineEdit:
        return self.__ui.main_window.passport_filter_statement

    @property
    def filter_type(self) -> QComboBox:
        return self.__ui.main_window.passport_filter_combo_box

    @property
    def amount(self) -> QLabel:
        return self.__ui.main_window.amount_of_passports

    @property
    def passports_list(self):
        return self.__ui.main_window.passports_list

    @property
    def new_passport(self):
        return self.__ui.main_window.add_passport

    @property
    def passport_title(self):
        return self.__ui.main_window.passport_title

    @property
    def passport_code(self):
        return self.__ui.main_window.passport_code

    @property
    def specifications(self):
        return self.__ui.main_window.specifications_list

    @property
    def new_specification(self):
        return self.__ui.main_window.add_specification

    @property
    def relations(self):
        return self.__ui.main_window.relations_list

    @property
    def new_relation(self):
        return self.__ui.main_window.add_relation

    @property
    def search(self):
        return self.__ui.main_window.search_list

    @property
    def new_search(self):
        return self.__ui.main_window.add_search

    @property
    def save_passport(self):
        return self.__ui.main_window.save_passport

    @property
    def delete_passport(self):
        return self.__ui.main_window.delete_passport


class AreasList:
    def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
        self.__objects: TabObjects = objects
        self.__page: PassportsPageActions = page

        self.__items: dict[str, AreaItem] = {}

        self.__objects.new_area.clicked.connect(self.__page.new_area)

    def new(self) -> None:
        self.__page.add_area(Area(title="",
                                  code=0))

    def add(self, uuid: str, area: Area) -> None:
        if uuid in self.__items.keys():
            self.change(uuid=uuid, area=area)
            return
        exists = len([1 for a in self.__items.values() if a.code == area.code]) > 1
        self.__items[uuid] = AreaItem(code=area.code,
                                      title=area.title,
                                      on_delete=partial(self.delete, uuid=uuid),
                                      title_is_valid=area.title_is_valid,
                                      code_is_valid=area.code_is_valid and not exists,
                                      on_change=partial(self.on_change, uuid=uuid))
        self.__objects.areas_list.addWidget(self.__items[uuid])

    def on_change(self, uuid: str):
        area = Area(code=self.__items[uuid].code,
                    title=self.__items[uuid].title)
        self.change(uuid=uuid, area=area)
        self.__page.change_area(uuid=uuid, area=area, reload=False)

    def change(self, uuid: str, area: Area) -> None:
        exists = len([1 for a in self.__items.values() if a.code == area.code]) > 1
        self.__items[uuid].change_title(area.title)
        self.__items[uuid].change_code(area.code)
        self.__items[uuid].change_title_is_valid(area.title_is_valid)
        self.__items[uuid].change_code_is_valid(area.code_is_valid and not exists)

    def delete(self, uuid: str) -> None:
        if uuid in self.__items.keys():
            self.__items[uuid].setParent(None)
            self.__objects.areas_list.removeWidget(self.__items[uuid])
            del self.__items[uuid]
        self.__page.remove_area(uuid, reload=False)

    def clear(self) -> None:
        for uuid in list(self.__items.keys()):
            self.delete(uuid)


class GroupsList:
    def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
        self.__objects: TabObjects = objects
        self.__page: PassportsPageActions = page

        self.__items: dict[str, GroupItem] = {}

        self.__objects.new_group.clicked.connect(self.__page.new_group)

    def new(self) -> None:
        self.__page.add_group(Group(title="",
                                    area=0,
                                    code=0))

    def add(self, uuid: str, group: Group) -> None:
        if uuid in self.__items.keys():
            self.change(uuid=uuid, group=group)
            return
        exists = len([1 for g in self.__items.values() if g.code == group.code and g.area == group.area]) > 1
        self.__items[uuid] = GroupItem(code=group.code,
                                       area=group.area,
                                       title=group.title,
                                       on_delete=partial(self.delete, uuid=uuid),
                                       title_is_valid=group.title_is_valid,
                                       code_is_valid=group.code_is_valid and not exists,
                                       area_is_valid=group.area_is_valid and self.__page.area_exists(group.area),
                                       on_change=partial(self.on_change, uuid=uuid))
        self.__objects.groups_list.addWidget(self.__items[uuid])

    def on_change(self, uuid: str):
        group = Group(code=self.__items[uuid].code,
                      area=self.__items[uuid].area,
                      title=self.__items[uuid].title)
        self.change(uuid=uuid, group=group)
        self.__page.change_group(uuid=uuid, group=group, reload=False)

    def change(self, uuid: str, group: Group) -> None:
        exists = len([1 for g in self.__items.values() if g.code == group.code and g.area == group.area]) > 1
        self.__items[uuid].change_title(group.title)
        self.__items[uuid].change_code(group.code)
        self.__items[uuid].change_area(group.area)
        self.__items[uuid].change_area_is_valid(group.area_is_valid and self.__page.area_exists(group.area))
        self.__items[uuid].change_title_is_valid(group.title_is_valid)
        self.__items[uuid].change_code_is_valid(group.code_is_valid and not exists)

    def delete(self, uuid: str) -> None:
        if uuid in self.__items.keys():
            self.__items[uuid].setParent(None)
            self.__objects.groups_list.removeWidget(self.__items[uuid])
            del self.__items[uuid]
        self.__page.remove_group(uuid, reload=False)

    def clear(self) -> None:
        for uuid in list(self.__items.keys()):
            self.delete(uuid)


class PassportsList:
    def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
        self.__objects: TabObjects = objects
        self.__page: PassportsPageActions = page
        self.__filter = self.Filter(objects=objects, page=page)
        self.__items: dict[str, ListButton] = {}

        self.__objects.new_passport.clicked.connect(self.__page.new_passport)

    def add(self, uuid: str, passport: Passport) -> None:
        if uuid in self.__items.keys():
            self.change(uuid=uuid, passport=passport)
            return
        self.__items[uuid] = ListButton(text=str(passport),
                                        on_click=partial(self.__page.open_passport, uuid=uuid),
                                        is_valid=passport.is_valid)
        self.__objects.passports_list.addWidget(self.__items[uuid])
        self.__objects.amount.setText(str(len(self.__items)))

    def change(self, uuid: str, passport: Passport) -> None:
        self.__items[uuid].change_text(str(passport))
        self.__items[uuid].change_is_valid(passport.is_valid)
        self.__page.change_passport(uuid=uuid, passport=passport, reload=False)

    def delete(self, uuid: str) -> None:
        if uuid in self.__items.keys():
            self.__items[uuid].setParent(None)
            self.__objects.passports_list.removeWidget(self.__items[uuid])
            del self.__items[uuid]
        self.__objects.amount.setText(str(len(self.__items)))

    def clear(self) -> None:
        for uuid in list(self.__items.keys()):
            self.delete(uuid)
        self.__objects.amount.setText(str(len(self.__items)))

    class Filter:
        def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
            self.__objects: TabObjects = objects
            self.__page: PassportsPageActions = page

            self.__objects.filter.clicked.connect(self.filter)

        def filter(self):
            match self.__objects.passports_is_valid_filter.currentIndex():
                case 1:
                    is_valid = True
                case 2:
                    is_valid = False
                case _:
                    is_valid = None
            filter_type = FilterTypes(self.__objects.filter_type.currentIndex())
            filter_statement = self.__objects.filter_statement.text()
            self.__page.filter_passports(is_valid=is_valid,
                                         filter_type=filter_type,
                                         filter_statement=filter_statement)


class PassportInfo:
    def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
        self.__objects: TabObjects = objects
        self.__page: PassportsPageActions = page
        self.__specifications = self.SpecificationsList(objects=self.__objects,
                                                        page=self.__page)
        self.__relations = self.RelationsList(objects=self.__objects,
                                              page=self.__page)
        self.__search = self.SearchList(objects=self.__objects,
                                        page=self.__page)
        self.disable()

    def save(self, uuid: str):
        passport = Passport(title=self.__objects.passport_title.text().strip(),  # ToDo
                            area=int(self.__objects.passport_code.text().split(".")[0]),
                            group=int(self.__objects.passport_code.text().split(".")[1]),
                            code=int(self.__objects.passport_code.text().split(".")[2]),
                            relations=self.__relations.relations,
                            search=self.__search.search,
                            specifications=self.__specifications.specifications)
        passport.validate(self.__page.passports, areas=self.__page.areas, groups=self.__page.groups)
        self.__page.change_passport(uuid=uuid,
                                    passport=passport)

    def set(self, uuid: str, passport: Passport) -> None:
        self.enable()
        self.__objects.passport_title.setText(passport.title)
        self.__objects.passport_title.setCursorPosition(0)
        self.__objects.passport_code.setText(f"{passport.area}.{passport.group}.{passport.code}")
        self.__specifications.clear()
        self.__relations.clear()
        self.__search.clear()

        for specification in passport.specifications:
            self.__specifications.add(specification)
        for relation in passport.relations:
            self.__relations.add(relation)
        for search in passport.search:
            self.__search.add(search)

        through(func=self.__objects.save_passport.clicked.disconnect)
        self.__objects.save_passport.clicked.connect(partial(self.save, uuid=uuid))

        through(func=self.__objects.delete_passport.clicked.disconnect)
        self.__objects.delete_passport.clicked.connect(partial(self.__page.remove_passport, uuid=uuid))

        if passport.title_is_valid:
            self.__objects.passport_title.setStyleSheet("")
        else:
            self.__objects.passport_title.setStyleSheet("background-color: rgb(239, 41, 41);")

        if passport.area_is_valid and passport.group_is_valid and passport.code_is_valid:
            self.__objects.passport_code.setStyleSheet("")
        else:
            self.__objects.passport_code.setStyleSheet("background-color: rgb(239, 41, 41);")

    def new(self) -> None:
        def inner():
            passport = Passport(title=self.__objects.passport_title.text().strip(),  # ToDo
                                area=int(self.__objects.passport_code.text().split(".")[0]),
                                group=int(self.__objects.passport_code.text().split(".")[1]),
                                code=int(self.__objects.passport_code.text().split(".")[2]),
                                relations=self.__relations.relations,
                                search=self.__search.search,
                                specifications=self.__specifications.specifications)
            passport.validate(self.__page.passports, areas=self.__page.areas, groups=self.__page.groups)
            uuid = self.__page.add_passport(passport)
            self.__page.open_passport(uuid)

        self.clear()
        through(func=self.__objects.save_passport.clicked.disconnect)
        self.__objects.save_passport.clicked.connect(partial(inner))

        through(func=self.__objects.delete_passport.clicked.disconnect)
        self.enable()

    def clear(self) -> None:
        self.__objects.passport_title.setText("")
        self.__objects.passport_code.setText("")
        self.__specifications.clear()
        self.__relations.clear()
        self.__search.clear()

        self.__objects.passport_title.setStyleSheet("")
        self.__objects.passport_code.setStyleSheet("")

    def disable(self) -> None:
        self.__objects.passport_title.setEnabled(False)
        self.__objects.passport_code.setEnabled(False)
        self.__objects.new_search.setEnabled(False)
        self.__objects.new_specification.setEnabled(False)
        self.__objects.new_relation.setEnabled(False)
        self.__objects.save_passport.setEnabled(False)
        self.__objects.delete_passport.setEnabled(False)

    def enable(self) -> None:
        self.__objects.passport_title.setEnabled(True)
        self.__objects.passport_code.setEnabled(True)
        self.__objects.new_search.setEnabled(True)
        self.__objects.new_specification.setEnabled(True)
        self.__objects.new_relation.setEnabled(True)
        self.__objects.save_passport.setEnabled(True)
        self.__objects.delete_passport.setEnabled(True)

    class SpecificationsList:
        def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
            self.__objects: TabObjects = objects
            self.__page: PassportsPageActions = page
            self.__items: dict[str, HorizontalListItem] = {}

            self.__objects.new_specification.clicked.connect(self.new)

        @property
        def specifications(self) -> list[str]:
            return [item.title for item in self.__items.values()]

        def add(self, specification: str) -> None:
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = HorizontalListItem(text=specification,
                                                    on_delete=partial(self.delete, uuid=uuid),
                                                    is_long=True)
            self.__objects.specifications.addWidget(self.__items[uuid])

        def new(self):
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = HorizontalListItem(text="",
                                                    on_delete=partial(self.delete, uuid=uuid),
                                                    is_long=True)
            self.__objects.specifications.addWidget(self.__items[uuid])

        def change(self, uuid: str, specification: str) -> None:
            self.__items[uuid].change_text(specification)
            # self.__items[uuid].change_is_valid(journal.is_valid)

        def delete(self, uuid: str) -> None:
            if uuid in self.__items.keys():
                self.__items[uuid].setParent(None)
                self.__objects.specifications.removeWidget(self.__items[uuid])
                del self.__items[uuid]

        def clear(self) -> None:
            for uuid in list(self.__items.keys()):
                self.delete(uuid)

    class RelationsList:
        def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
            self.__objects: TabObjects = objects
            self.__page: PassportsPageActions = page
            self.__items: dict[str, HorizontalListItem] = {}

            self.__objects.new_relation.clicked.connect(self.new)

        @property
        def relations(self) -> list[str]:
            return [item.title for item in self.__items.values()]

        def add(self, relation: str) -> None:
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = HorizontalListItem(text=relation,
                                                    on_delete=partial(self.delete, uuid=uuid))
            self.__objects.relations.addWidget(self.__items[uuid])

        def new(self):
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = HorizontalListItem(text="",
                                                    on_delete=partial(self.delete, uuid=uuid))
            self.__objects.relations.addWidget(self.__items[uuid])

        def change(self, uuid: str, relation: str) -> None:
            self.__items[uuid].change_text(relation)
            # self.__items[uuid].change_is_valid(journal.is_valid)

        def delete(self, uuid: str) -> None:
            if uuid in self.__items.keys():
                self.__items[uuid].setParent(None)
                self.__objects.relations.removeWidget(self.__items[uuid])
                del self.__items[uuid]

        def clear(self) -> None:
            for uuid in list(self.__items.keys()):
                self.delete(uuid)

    class SearchList:
        def __init__(self, objects: TabObjects, page: "PassportsPageActions"):
            self.__objects: TabObjects = objects
            self.__page: PassportsPageActions = page

            self.__items: dict[str, SearchItem] = {}

            self.__objects.new_search.clicked.connect(self.new)

        @property
        def search(self) -> list[str]:
            return [item.title for item in self.__items.values()]

        def add(self, search: str) -> None:
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = SearchItem(title=search,
                                            on_delete=partial(self.delete, uuid=uuid))
            self.__objects.search.addWidget(self.__items[uuid])

        def new(self):
            uuid = uuid4().hex
            while uuid in self.__items.keys():
                uuid = uuid4().hex
            self.__items[uuid] = SearchItem(title="",
                                            on_delete=partial(self.delete, uuid=uuid))
            self.__objects.search.addWidget(self.__items[uuid])

        def change(self, uuid: str, search: str) -> None:
            self.__items[uuid].change_text(search)
            # self.__items[uuid].change_is_valid(journal.is_valid)

        def delete(self, uuid: str) -> None:
            if uuid in self.__items.keys():
                self.__items[uuid].setParent(None)
                self.__objects.search.removeWidget(self.__items[uuid])
                del self.__items[uuid]

        def clear(self) -> None:
            for uuid in list(self.__items.keys()):
                self.delete(uuid)


class PassportsPageActions:
    def __init__(self, actions: "Actions", ui: UI, logic: Logic):
        self.__ui = ui
        self.__logic = logic
        self.__actions = actions

        self.__objects = TabObjects(ui)

        self.__areas: dict[str, Area] = {}
        self.__groups: dict[str, Group] = {}
        self.__passports: dict[str, Passport] = {}

        self.__areas_list = AreasList(objects=self.__objects, page=self)
        self.__groups_list = GroupsList(objects=self.__objects, page=self)
        self.__passports_list = PassportsList(objects=self.__objects, page=self)
        self.__passport_info = PassportInfo(objects=self.__objects, page=self)

    @property
    def passports(self):
        return list(self.__passports.values())

    @property
    def areas(self):
        return list(self.__areas.values())

    @property
    def groups(self):
        return list(self.__groups.values())

    def set_areas(self, areas: list[Area], reload: bool = True) -> None:
        self.__areas_list.clear()
        for area in areas:
            self.add_area(area, reload=reload)

    def area_exists(self, code: int):
        for area in self.__areas.values():
            if area.code == code:
                return True
        return False

    def add_area(self, area: Area, reload: bool = True):
        uuid = uuid4().hex
        while uuid in self.__areas.keys():
            uuid = uuid4().hex
        self.__areas[uuid] = area
        if reload:
            self.__areas_list.add(uuid=uuid, area=area)
        return uuid

    def new_area(self):
        self.__areas_list.new()

    def change_area(self, uuid: str, area: Area, reload: bool = True):
        if uuid in self.__areas.keys():
            self.__areas[uuid] = area
        if reload:
            self.__areas_list.change(uuid=uuid, area=area)

    def remove_area(self, uuid: str, reload: bool = True):
        if uuid in self.__areas.keys():
            del self.__areas[uuid]
        if reload:
            self.__areas_list.delete(uuid)

    def set_groups(self, groups: list[Group], reload: bool = True) -> None:
        self.__groups_list.clear()
        for group in groups:
            self.add_group(group, reload=reload)

    def add_group(self, group: Group, reload: bool = True):
        uuid = uuid4().hex
        while uuid in self.__groups.keys():
            uuid = uuid4().hex
        self.__groups[uuid] = group
        if reload:
            self.__groups_list.add(uuid=uuid, group=group)
        return uuid

    def new_group(self):
        self.__groups_list.new()

    def change_group(self, uuid: str, group: Group, reload: bool = True):
        if uuid in self.__groups.keys():
            self.__groups[uuid] = group
        if reload:
            self.__groups_list.change(uuid=uuid, group=group)

    def remove_group(self, uuid: str, reload: bool = True):
        if uuid in self.__groups.keys():
            del self.__groups[uuid]
        if reload:
            self.__groups_list.delete(uuid)

    def set_passports(self, passports: list[Passport], reload: bool = True) -> None:
        self.__passports_list.clear()
        for passport in passports:
            self.add_passport(passport, reload=reload)

    def open_passport(self, uuid: str):
        self.__passport_info.set(uuid=uuid, passport=self.__passports[uuid])

    def filter_passports(self, is_valid: bool, filter_type: FilterTypes.values_type, filter_statement: str):
        self.__passports_list.clear()
        self.__passport_info.clear()
        self.__passport_info.disable()

        for uuid, passport in self.__passports.items():
            if passport.is_valid != is_valid and is_valid is not None:
                continue
            if len(filter_statement.strip()) != 0 or filter_type == FilterTypes.DOUBLED:
                if filter_type == FilterTypes.CODE:
                    if list(map(int, filter_statement.split("."))) != [passport.area, passport.group, passport.code]:
                        continue
                elif filter_type == FilterTypes.TITLE:
                    if filter_statement.lower() not in passport.title.lower():
                        continue
                elif filter_type == FilterTypes.DOUBLED:
                    if len([1 for p in self.__passports.values() if passport == p]) < 2:
                        continue
            self.__passports_list.add(uuid=uuid, passport=passport)

    def add_passport(self, passport: Passport, reload: bool = True):
        uuid = uuid4().hex
        while uuid in self.__passports.keys():
            uuid = uuid4().hex
        self.__passports[uuid] = passport
        if reload:
            self.__passports_list.add(uuid=uuid, passport=passport)
        return uuid

    def new_passport(self):
        self.__passport_info.new()

    def change_passport(self, uuid: str, passport: Passport, reload: bool = True):
        if uuid in self.__passports.keys():
            self.__passports[uuid] = passport
        if reload:
            for u, p in self.__passports.items():
                if p == passport:
                    p.validate(passports=self.passports,
                               areas=self.areas,
                               groups=self.groups)
                    self.__passports_list.change(uuid=u, passport=p)
            self.open_passport(uuid=uuid)

    def remove_passport(self, uuid: str, reload: bool = True):
        if uuid in self.__passports.keys():
            del self.__passports[uuid]
        if reload:
            self.__passports_list.delete(uuid)
