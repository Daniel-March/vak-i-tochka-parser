import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

import yaml

from app.exceptions import ConfigPathError

if TYPE_CHECKING:
    from app.app import App


@dataclass
class Paths:
    journals: str
    passports: str
    output: str
    temporary: str


@dataclass
class Names:
    journals: str
    temp_journals_json: str
    output_journals_json: str
    temp_passports_json: str
    output_passports_json: str


@dataclass
class Config:
    paths: Paths
    names: Names


async def setup_config(app: "App", config_path: str):
    if not os.path.exists(config_path):
        raise ConfigPathError(text="path doesn't exists")

    with open(config_path, "r") as file:
        raw_config = yaml.safe_load(file)

    app.config = Config(paths=Paths(journals=raw_config["directory_to_save_journals_pdf_file"],
                                    passports=raw_config["directory_to_save_passports_pdf_files"],
                                    output=raw_config["directory_to_save_output_files"],
                                    temporary=raw_config["directory_to_save_temporary_files"],),
                        names=Names(journals=raw_config["filename_to_save_journals_pdf"],
                                    temp_journals_json=raw_config["filename_to_save_temporary_journals_json"],
                                    output_journals_json=raw_config["filename_to_save_output_journals_json"],
                                    temp_passports_json=raw_config["filename_to_save_temporary_passports_json"],
                                    output_passports_json=raw_config["filename_to_save_output_passports_json"],))
