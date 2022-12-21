from typing import TYPE_CHECKING

from journals.downloader import Downloader
from journals.parser import Parser
from journals.store import Store

if TYPE_CHECKING:
    from app import App


async def setup_parser(app: "App"):
    app.journals_parser = Parser(app)


async def setup_downloader(app: "App"):
    app.journals_downloader = Downloader(app)


async def setup_store(app: "App"):
    app.journals_store = Store(app)
