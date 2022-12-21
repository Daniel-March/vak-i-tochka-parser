from typing import Optional

from PyQt5.QtWidgets import QProgressBar

from app import App
from app.exceptions import InternetError, FilesError
from view.logic.objects import Journal, Speciality, Passport, Area, Group


class Logic:
    def __init__(self, app: App):
        self.__app = app

    @property
    def app(self):
        return self.__app

    def load_journals(self) -> list[Journal]:
        journals = []
        for journal in self.__app.journals_store.load():
            specialities = [Speciality(date=speciality["date"],
                                       title=speciality["title"],
                                       code=speciality["code"]) for speciality in journal["specialities"]]
            journals.append(Journal(issn=journal["issn"],
                                    title=journal["title"],
                                    specialities=specialities))
        return journals

    def save_journals(self, journals: list[Journal]):
        self.__app.journals_store.save([journal.json for journal in journals])

    def convert_journals(self, journals: list[Journal]):
        for i in range(len(journals) - 1, -1, -1):
            if not journals[i].is_valid:
                del journals[i]
                continue
            journal = {"issn": journals[i].issn,
                       "title": journals[i].title,
                       "specialities": [{"date": speciality.date,
                                         "title": speciality.title,
                                         "area": int(speciality.code.split(".")[0]),
                                         "group": int(speciality.code.split(".")[1]),
                                         "code": int(speciality.code.split(".")[2])} for speciality in
                                        journals[i].specialities]}
            journals[i] = journal
        self.__app.journals_store.save({"data": journals}, temp=False)

    def parse_journals(self, link: Optional[str], progress_bar: QProgressBar, notifier):
        journals = []
        notifier.emit("----- ЗАПУЩЕН ПАРСИНГ ЖУРНАЛОВ -----")
        if link is not None:
            notifier.emit("Начата загрузка pdf с журналами")
            try:
                self.__app.journals_downloader.download(link=link)
            except InternetError as e:
                notifier.emit(e.text)
                return
            except FilesError as e:
                notifier.emit(e.text)
                return
            except Exception as e:
                notifier.emit(f"Что-то при загрузке журналов совсем пошло не так...\n\t\t({e})")
                return
            notifier.emit("Загрузка pdf с журналами завершена")

        journals_generator = self.__app.journals_parser.get_journals()
        start_n_pages = None
        progress_bar.setValue(0)
        notifier.emit("Начат парсинг журналов")
        try:
            for journal in journals_generator:
                if start_n_pages is None:
                    start_n_pages = self.__app.journals_parser.pages
                journals.append(journal)
                progress_bar.setValue(int(100 - (self.__app.journals_parser.pages * 100 / start_n_pages)))
            progress_bar.setValue(100)
        except Exception as e:
            notifier.emit(f"Парсинг журналов совсем пошел не так...\n\t\t({e})")
            progress_bar.setValue(0)
            return
        notifier.emit("Сохранение журналов")
        self.__app.journals_store.save(journals)
        notifier.emit("----- ПАРСИНГ ЖУРНАЛОВ ЗАВЕРШЕН -----")

    def load_passports(self) -> list[Passport]:
        passports = []
        for passport in self.__app.passports_store.load()["passports"]:
            passports.append(Passport(area=passport["area"],
                                      group=passport["group"],
                                      code=passport["code"],
                                      title=passport["title"],
                                      relations=passport["relations"],
                                      search=passport["search"],
                                      specifications=passport["specifications"]))
        for passport in passports:
            passport.validate(passports=passports, areas=self.load_areas(), groups=self.load_groups())
        return passports

    def save_passports(self, passports: list[Passport], areas: list[Area], groups: list[Group]):
        self.__app.passports_store.save({"passports": [passport.json for passport in passports],
                                         "areas": [area.json for area in areas],
                                         "groups": [group.json for group in groups]}, temp=True)

    def convert_passports(self, passports: list[Passport], areas: list[Area], groups: list[Group]):
        passports_json: dict = {}
        relations_json: dict = {}

        for area in areas:
            if not area.is_valid:
                areas.remove(area)
        for group in groups:
            if not group.is_valid:
                groups.remove(group)
        for passport in passports:
            passport.validate(passports=passports, areas=areas, groups=groups)
            if not passport.is_valid:
                passports.remove(passport)
            id = len(passports_json.keys())
            passports_json[id] = passport.json
            del passports_json[id]["relations"]

            relations_json[id] = passport.relations

        self.__app.passports_store.save({"passports": passports_json,
                                         "relations": relations_json,
                                         "areas": [area.json for area in areas],
                                         "groups": [group.json for group in groups]}, temp=False)

    def load_areas(self) -> list[Area]:
        areas = []
        for area in self.__app.passports_store.load()["areas"]:
            areas.append(Area(code=area["code"],
                              title=area["title"]))
        return areas

    def load_groups(self) -> list[Group]:
        groups = []
        for group in self.__app.passports_store.load()["groups"]:
            groups.append(Group(code=group["code"],
                                area=group["area"],
                                title=group["title"]))
        return groups

    def parse_passports(self, link: Optional[str], progress_bar: QProgressBar, notifier):
        result = {"passports": [],
                  "areas": [],
                  "groups": []}
        notifier.emit("----- ЗАПУЩЕН ПАРСИНГ ПАСПОРТОВ -----")
        if link is not None:
            notifier.emit("Начата загрузка pdf паспортов")
            try:
                folder_id = link.split("/")[link.split("/").index("folders") + 1]
                self.__app.passports_downloader.download(folder_id=folder_id, notifier=notifier)
            except InternetError as e:
                notifier.emit(e.text)
                return
            except FilesError as e:
                notifier.emit(e.text)
                return
            except Exception as e:
                notifier.emit(f"Что-то при загрузке паспортов совсем пошло не так...\n\t\t({e})")
                return
            notifier.emit("Загрузка pdf паспортов завершена")

        passports_generator = self.__app.passports_parser.get_passports(notifier)
        start_n_documents = None
        progress_bar.setValue(0)
        notifier.emit("Начат парсинг паспортов")
        try:
            for passport in passports_generator:
                if start_n_documents is None:
                    start_n_documents = self.__app.passports_parser.documents
                result["passports"].append({"code": passport["code"],
                                            "area": passport["area"]["code"],
                                            "group": passport["group"]["code"],
                                            "title": passport["title"].strip(),
                                            "specifications": passport["specifications"],
                                            "relations": passport["relations"],
                                            "search": passport["search"]})
                if passport["area"]["code"] not in [area["code"] for area in result["areas"]]:
                    result["areas"].append({"code": passport["area"]["code"],
                                            "title": passport["area"]["title"]})
                if (passport["area"]["code"], passport["group"]["code"]) not in [(group["area"], group["code"]) for
                                                                                 group in result["groups"]]:
                    result["groups"].append({"code": passport["group"]["code"],
                                             "area": passport["area"]["code"],
                                             "title": passport["group"]["title"]})
                progress_bar.setValue(
                    int((100 - (self.__app.passports_parser.documents * 100 / start_n_documents))))
            progress_bar.setValue(100)
        except Exception as e:
            notifier.emit(f"Парсинг паспортов совсем пошел не так...\n\t\t({e})")
            progress_bar.setValue(0)
            return
        notifier.emit("Сохранение паспортов")
        self.__app.passports_store.save(result)
        notifier.emit("----- ПАРСИНГ ПАСПОРТОВ ЗАВЕРШЕН -----")
