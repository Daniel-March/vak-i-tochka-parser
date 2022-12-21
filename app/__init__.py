import os.path

from app.app import App
from app.config import setup_config
from app.exceptions import ConfigPathError
from journals import setup_downloader as setup_journals_downloader
from journals import setup_parser as setup_journals_parser
from journals import setup_store as setup_journals_store
from passports import setup_downloader as setup_passports_parser
from passports import setup_parser as setup_passports_downloader
from passports import setup_store as setup_passports_store


async def check_directories(app: App):
    if not os.path.exists(app.config.paths.journals):
        raise ConfigPathError(text="path to save journals doesn't exists")
    if not os.path.exists(app.config.paths.passports):
        raise ConfigPathError(text="path to save passports doesn't exists")
    if not os.path.exists(app.config.paths.output):
        raise ConfigPathError(text="path to save output files doesn't exists")
    if not os.path.exists(app.config.paths.temporary):
        raise ConfigPathError(text="path to save temporary files doesn't exists")


async def create_app(config_path: str):
    app = App()
    await setup_config(app=app,
                       config_path=config_path)
    await check_directories(app)
    await setup_journals_parser(app)
    await setup_journals_downloader(app)
    await setup_journals_store(app)
    await setup_passports_parser(app)
    await setup_passports_downloader(app)
    await setup_passports_store(app)
    return app
