import os
import re
from typing import TYPE_CHECKING

import pdfplumber
from PyQt5.QtWidgets import QHBoxLayout

if TYPE_CHECKING:
    from app import App


class Parser:
    def __init__(self, app: "App"):
        self.__app: App = app
        self.__n_documents = 0

    @property
    def documents(self):
        return self.__n_documents

    def get_passports(self, notifier: QHBoxLayout):
        files = [file for file in os.listdir(self.__app.config.paths.passports) if file[-4:] == ".pdf"]
        for index, filename in enumerate(files):
            self.__n_documents = len(files) - index
            cur_path = os.path.join(self.__app.config.paths.passports, filename)
            with pdfplumber.open(cur_path) as pdf:
                document = ""
                for page in pdf.pages:
                    document += page.extract_text().strip() + "\n"

                while "  " in document:
                    document = document.replace("  ", " ")

                try:
                    area_span = re.search(r"(Область|Отрасль) наук[и]*", document).start()
                    group_span = document.index("Группа научных")
                    specification_span = re.search("Наименовани[ея] отрасл[ией]*", document).start()
                    title_span = re.search(r"Шифр.*специальност[ией]*:", document).start()
                    search_span = re.search(r"(Направлени[ея]|Наименовани[ея]) исследован[ияй]*", document).start()
                    relations_span = re.search(r"Смежн[ыея]* специальност[иь]", document).start()
                except:
                    notifier.emit(f"----1 Ошибка при парсинге журнала. Журнал создан как пустой ({filename})")
                    yield {"code": 0,
                           "area": {"code": 0,
                                    "title": ""},
                           "group": {"code": 0,
                                     "title": ""},
                           "title": filename,
                           "specifications": [],
                           "relations": [],
                           "search": []}
                    continue

                try:
                    area_span = document[area_span: group_span].strip()
                    group_span = document[group_span:specification_span].strip()
                    specification_span = document[specification_span:title_span].strip()
                    title_span = document[title_span:search_span].strip().replace("\n", " ")
                    search_span = document[search_span:relations_span].strip()
                    relations_span = document[relations_span:].strip()
                except:
                    notifier.emit(f"----2 Ошибка при парсинге журнала ({filename})")
                    yield {"code": 0,
                           "area": {"code": 0,
                                    "title": ""},
                           "group": {"code": 0,
                                     "title": ""},
                           "title": filename,
                           "specifications": [],
                           "relations": [],
                           "search": []}
                    continue

                while "  " in title_span:
                    title_span = title_span.replace("  ", " ")

                while (index := re.search(r".\n\D", search_span)) is not None:
                    search_span = search_span[:index.start() + 1] + search_span[index.end() - 1:]

                while (index := re.search(r".\n\D", relations_span)) is not None:
                    relations_span = relations_span[:index.start() + 1] + relations_span[index.end() - 1:]

                while "  " in search_span:
                    search_span = search_span.replace("  ", " ")
                try:
                    search_span = "\n".join([s for s in search_span.split("\n")[1:] if len(s) > 4])
                except:
                    notifier.emit(f"----3 Ошибка при парсинге журнала ({filename})")
                    yield {"code": 0,
                           "area": {"code": 0,
                                    "title": ""},
                           "group": {"code": 0,
                                     "title": ""},
                           "title": title,
                           "specifications": [],
                           "relations": [],
                           "search": []}
                    continue

                try:
                    area = re.search(r"\d\d*.*$", area_span).group()
                    group = re.search(r"\d\d*\.\d\d*.*", group_span).group()
                    specifications = re.findall(r".*", specification_span[specification_span.index(":") + 1:].strip())
                    specifications = [specification.strip() for specification in specifications if specification != ""]
                    title = re.search(r"\d\d*\.\d\d*\.\d\d*.*", title_span).group()
                    search = [(re.search(r"[a-zA-Zа-яА-Я].*", s).group() if s[0].isdigit() else s).strip()
                              for s in search_span.split("\n")]
                    relations = re.findall(r"\d\d*\.\d\d*\.\d\d*", relations_span)
                except:
                    notifier.emit(f"----4 Ошибка при парсинге журнала ({filename})")
                    yield {"code": 0,
                           "area": {"code": 0,
                                    "title": ""},
                           "group": {"code": 0,
                                     "title": ""},
                           "title": title,
                           "specifications": [],
                           "relations": [],
                           "search": []}
                    continue

                try:
                    area_code = area[:re.search(r"\d\d*", area).end()].replace(".", "")
                    area_title = area[re.search(r"\D\D*", area).start():].strip()
                except:
                    notifier.emit(f"----5 Ошибка при парсинге журнала ({filename})")
                    yield {"code": 0,
                           "area": {"code": 0,
                                    "title": ""},
                           "group": {"code": 0,
                                     "title": ""},
                           "title": title,
                           "specifications": [],
                           "relations": [],
                           "search": []}
                    continue

                if area_title[0] == ".":
                    area_title = area_title[1:].strip()

                try:
                    group_code = group[group.index("."):re.search(r"[^0-9.]", group).start()].replace(".", "")
                    group_title = group[re.search(r"[^0-9.]", group).start():].strip()
                    if group_title[0] == ".":
                        group_title = group_title[1:].strip()
                except:
                    notifier.emit(f"----6 Ошибка при парсинге журнала ({filename})")
                    yield {"code": 0,
                           "area": {"code": 0,
                                    "title": ""},
                           "group": {"code": 0,
                                     "title": ""},
                           "title": title,
                           "specifications": [],
                           "relations": [],
                           "search": []}
                    continue

                try:
                    title_code = title[re.search(r"\d\d*\.\d\d*\.", title).end():
                                       re.search(r"[^0-9.]", title).start()].replace(".", "").strip()
                    title_title = title[re.search(r"[^0-9.]", title).start():].strip()
                    if title_title[0] == ".":
                        title_title = title_title[1:].strip()
                except:
                    notifier.emit(f"----7 Ошибка при парсинге журнала ({filename})")
                    yield {"code": 0,
                           "area": {"code": 0,
                                    "title": ""},
                           "group": {"code": 0,
                                     "title": ""},
                           "title": title,
                           "specifications": [],
                           "relations": [],
                           "search": []}
                    continue

                yield {"code": int(title_code),
                       "area": {"code": int(area_code),
                                "title": area_title},
                       "group": {"code": int(group_code),
                                 "title": group_title},
                       "title": title_title,
                       "specifications": specifications,
                       "relations": relations,
                       "search": search}
