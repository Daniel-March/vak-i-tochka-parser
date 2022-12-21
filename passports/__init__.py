from typing import TYPE_CHECKING

from passports.downloader import Downloader
from passports.parser import Parser
from passports.store import Store

if TYPE_CHECKING:
    from app import App


async def setup_parser(app: "App"):
    app.passports_parser = Parser(app)


async def setup_downloader(app: "App"):
    app.passports_downloader = Downloader(app)


async def setup_store(app: "App"):
    app.passports_store = Store(app)
