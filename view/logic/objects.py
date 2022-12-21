import re
from dataclasses import dataclass


@dataclass
class Speciality:
    title: str
    code: str
    date: str

    @property
    def title_is_valid(self):
        return len(self.title) > 2

    @property
    def code_is_valid(self):
        return re.match(r"^\d+.\d+.\d+$", self.code) is not None

    @property
    def date_is_valid(self):
        return self.date > "1800-12-12"

    @property
    def is_valid(self):
        if not self.title_is_valid:
            return False
        elif not self.code_is_valid:
            return False
        elif not self.date_is_valid:
            return False
        return True

    @property
    def json(self) -> dict:
        return {"title": self.title,
                "code": self.code,
                "date": self.date}


@dataclass
class Journal:
    issn: str
    title: str
    specialities: list[Speciality]

    @property
    def title_is_valid(self):
        return len(self.title) > 2

    @property
    def issn_is_valid(self):
        return re.match(r"^(\d\d\d\d-\d\d\d[A-Z0-9] )*(\d\d\d\d-\d\d\d[A-Z0-9])$", self.issn) is not None

    @property
    def specialities_is_valid(self):
        if len(self.specialities) == 0:
            return False
        for speciality in self.specialities:
            if not speciality.is_valid:
                return False
        return True

    @property
    def is_valid(self):
        if not self.title_is_valid:
            return False
        elif not self.issn_is_valid:
            return False
        elif not self.specialities_is_valid:
            return False
        return True

    def __str__(self):
        return f"{self.issn} - {self.title}"

    @property
    def json(self) -> dict:
        return {"issn": self.issn,
                "title": self.title,
                "specialities": [speciality.json for speciality in self.specialities]}


@dataclass
class Area:
    title: str
    code: int

    @property
    def title_is_valid(self):
        return len(self.title) > 2

    @property
    def code_is_valid(self):
        return self.code > 0

    @property
    def is_valid(self) -> bool:
        if not self.title_is_valid:
            return False
        if not self.code_is_valid:
            return False
        return True

    @property
    def json(self) -> dict:
        return {"title": self.title,
                "code": self.code}


@dataclass
class Group:
    title: str
    code: int
    area: int

    @property
    def title_is_valid(self):
        return len(self.title) > 2

    @property
    def code_is_valid(self):
        return self.code > 0

    @property
    def area_is_valid(self):
        return self.area > 0

    @property
    def is_valid(self) -> bool:
        if not self.title_is_valid:
            return False
        if not self.code_is_valid:
            return False
        if not self.area_is_valid:
            return False
        return True

    @property
    def json(self) -> dict:
        return {"title": self.title,
                "code": self.code,
                "area": self.area}


@dataclass
class Passport:
    title: str
    area: int
    group: int
    code: int
    relations: list[str]
    search: list[str]
    specifications: list[str]
    title_is_valid: bool = True
    code_is_valid: bool = True
    area_is_valid: bool = True
    group_is_valid: bool = True
    relations_is_valid: bool = True
    search_is_valid: bool = True
    specifications_is_valid: bool = True

    def validate(self, passports: list["Passport"], areas: list[Area], groups: list[Group]) -> bool:
        self.title_is_valid = len(self.title) > 2
        self.area_is_valid = self.area > 0
        self.group_is_valid = self.group > 0
        self.code_is_valid = self.code > 0
        self.relations_is_valid = len(self.relations) > 0
        self.search_is_valid = len(self.search) > 0
        self.specifications_is_valid = len(self.specifications) > 0

        if self.area not in [a.code for a in areas]:
            self.area_is_valid = False

        if (self.area, self.group) not in [(a.area, a.code) for a in groups]:
            self.group_is_valid = False

        if len([1 for passport in passports if passport.title == self.title]) > 1:
            self.title_is_valid = False
            self.area_is_valid = False
            self.group_is_valid = False
            self.code_is_valid = False

        for relation in self.relations:
            if len(relation) <= 2:
                self.relations_is_valid = False
                break
            area, group, code = list(map(int, relation.split(".")))

            if f"{area}.{group}" not in [f"{g.area}.{g.code}" for g in groups]:
                self.relations_is_valid = False
                break
            if code not in [p.code for p in passports]:
                self.relations_is_valid = False
                break

        for search in self.search:
            if len(search) <= 2:
                self.search_is_valid = False
                break
        for specification in self.specifications:
            if len(specification) <= 2:
                self.specifications_is_valid = False
                break
        return True

    @property
    def is_valid(self):
        return self.title_is_valid and \
               self.code_is_valid and \
               self.area_is_valid and \
               self.group_is_valid and \
               self.relations_is_valid and \
               self.search_is_valid and \
               self.specifications_is_valid

    @property
    def json(self) -> dict:
        return {"title": self.title,
                "area": self.area,
                "group": self.group,
                "code": self.code,
                "relations": self.relations,
                "search": self.search,
                "specifications": self.specifications}

    def __eq__(self, other: "Passport"):
        return [other.area, other.group, other.code] == [self.area, self.group, self.code]

    def __str__(self):
        return f"{self.area}.{self.group}.{self.code} - {self.title}"
