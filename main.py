import asyncio
import sys

from app import create_app, App
from view.logic import Logic
from view.ui import UI
from view.ui.actions import Actions

config_path = "/home/daniel/Projects/Python/vak_i_tochka_parser/config.yaml"

app: App


async def main():
    app = await create_app(config_path=config_path)

    ui = UI()
    logic = Logic(app)
    Actions(ui=ui, logic=logic)
    # actions.import_journals()
    # actions.import_passports()
    ui.window.showMaximized()
    sys.exit(ui.application.exec_())


if __name__ == "__main__":
    asyncio.run(main())
