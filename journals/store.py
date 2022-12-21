import json
import os.path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.app import App


class Store:
    def __init__(self, app: "App"):
        self.__app: App = app

    def load(self) -> list[dict]:
        path = os.path.join(self.__app.config.paths.temporary, self.__app.config.names.temp_journals_json)
        if os.path.exists(path):
            with open(path, "r") as file:
                return json.loads(file.read())
        return []

    def save(self, data: list[dict] | dict, temp: bool = True):
        if temp:
            path = os.path.join(self.__app.config.paths.temporary, self.__app.config.names.temp_journals_json)
        else:
            path = os.path.join(self.__app.config.paths.output, self.__app.config.names.output_journals_json)

        with open(path, "w") as file:
            file.write(json.dumps(data, ensure_ascii=False))
