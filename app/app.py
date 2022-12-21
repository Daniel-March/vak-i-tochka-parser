from typing import Optional
from passports.parser import Parser as PassportsParser
from passports.downloader import Downloader as PassportsDownloader
from passports.store import Store as PassportsStore
from journals.parser import Parser as JournalsParser
from journals.downloader import Downloader as JournalsDownloader
from journals.store import Store as JournalsStore
from app.config import Config


class App:
    config: Optional[Config] = None
    journals_parser: Optional[JournalsParser] = None
    journals_downloader: Optional[JournalsDownloader] = None
    journals_store: Optional[JournalsStore] = None

    passports_parser: Optional[PassportsParser] = None
    passports_downloader: Optional[PassportsDownloader] = None
    passports_store: Optional[PassportsStore] = None

