import os.path
import re
from datetime import datetime
from typing import TYPE_CHECKING

import pdfplumber

from app.exceptions import FilesError

if TYPE_CHECKING:
    from app import App


class Parser:
    def __init__(self, app: "App"):
        self.__app: App = app
        self.__n_pages = 0

    def __get_journals_row(self):
        flag = True
        first = True
        with pdfplumber.open(os.path.join(self.__app.config.paths.journals, self.__app.config.names.journals)) as pdf:
            pages = pdf.pages
            self.__n_pages = len(pages)
            while self.__n_pages > 0:
                for row in pages[0].extract_table():
                    if flag and "1." != str(row[0]):
                        continue
                    flag = False
                    if first:
                        row = row[::3]
                    if "" in row:
                        for i in range(len(row)):
                            if row[i] == "":
                                row[i] = None
                    yield row
                first = False
                del pages[0]
                self.__n_pages -= 1

    @property
    def pages(self):
        return self.__n_pages

    def get_journals(self) -> dict:
        if not os.path.exists(os.path.join(self.__app.config.paths.journals, self.__app.config.names.journals)):
            raise FilesError(text="pdf file to parse journals doesn't exists")

        journal = {}
        last_date = None
        for row in self.__get_journals_row():
            if row[0] is not None:
                if journal != {}:
                    yield journal
                if row[2] is not None:
                    row[2] = row[2].strip().replace("\n", " ").replace(",", " ").replace("Х", "X")
                    while "  " in row[2]:
                        row[2] = row[2].replace("  ", " ")
                journal = {
                    "title": row[1].replace("\n", "") if row[1] is not None else "",
                    "issn": row[2],
                    "specialities": []
                }
            if row[1] is not None and row[0] is None:
                journal["title"] += " " + row[1].replace("\n", "").strip()
            journal["title"] = journal["title"].strip()
            if row[4] is not None:
                last_date = row[4].strip()
                if (match := re.search(r"\d\d\.\d\d\.\d\d\d\d", last_date)) is not None:
                    last_date = str(datetime.strptime(match.group(), "%d.%m.%Y").strftime("%Y-%m-%d"))
                    last_date = f"0{last_date}"[-10:]
                else:
                    last_date = "1800-12-12"
            if row[3] is not None:
                codes = re.findall(r"\d+\.\d+\.\d+", row[3])
                titles = re.split(r"\d+\.\d+\.\d+", row[3])[1:]
                for index in range(len(titles)):
                    title = titles[index]
                    title = title.replace("\n", "").replace("  ", " ").strip()
                    title = title[re.search(r"[a-zA-ZА-Яа-я]", title).start():]
                    if title[-1] == ",":
                        title = title[:-1].strip()
                    titles[index] = title
                    journal["specialities"].append({
                        "code": codes[index],
                        "title": titles[index],
                        "date": last_date
                    })
        if journal != {}:
            yield journal
