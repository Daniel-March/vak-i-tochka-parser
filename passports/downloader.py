import os
import shutil
import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.app import App
from google_api import GoogleAPI


class Counter:
    def __init__(self, count: int, notifier):
        self.__count = count
        self.__current = 0
        self.__notifier = notifier
        self.__in_process = []

    @property
    def in_process(self):
        return len(self.__in_process)

    def started(self, file_id: str):
        self.__in_process.append(file_id)

    def finished(self, file_id):
        self.__in_process.remove(file_id)
        self.__current += 1
        self.__notifier.emit(f"Скачано паспортов: {self.__current}/{self.__count}")


class Downloader:
    def __init__(self, app: "App"):
        self.__app: App = app

    def download(self, folder_id: str, notifier):
        if os.path.isdir(self.__app.config.paths.passports):
            shutil.rmtree(self.__app.config.paths.passports, ignore_errors=True)
        os.mkdir(self.__app.config.paths.passports)
        passports = GoogleAPI.get_folder_files(folder_id)
        counter = Counter(len(passports), notifier)
        for i, passport in enumerate(passports):
            while counter.in_process > 150:
                time.sleep(0.2)
            counter.started(passport)
            threading.Thread(target=self.__download,
                             args=[passport, self.__app.config.paths.passports, counter]).start()

        while counter.in_process > 0:
            time.sleep(1)

    @staticmethod
    def __download(file_id: str, path: str, counter: Counter):
        GoogleAPI.download_file(file_id, path)
        counter.finished(file_id)
