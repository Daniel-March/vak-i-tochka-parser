import os.path
from typing import TYPE_CHECKING

import requests

from app.exceptions import InternetError, FilesError

if TYPE_CHECKING:
    from app.app import App


class Downloader:
    def __init__(self, app: "App"):
        self.__app: App = app

    def download(self, link: str) -> None:
        try:
            pdf_response = requests.get(link, verify=False)
        except:
            raise InternetError(text="journals downloading failed")

        try:
            with open(os.path.join(self.__app.config.paths.journals, self.__app.config.names.journals), "wb") as file:
                file.write(pdf_response.content)
        except:
            raise FilesError(text="journals saving failed")
