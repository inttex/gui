# Created by hillerj at 20.08.2020
import logging
import sys

# in order to exclude debug logs from matplotlib
# for key in logging.Logger.manager.loggerDict:
#     print(key)
from GuiLib.test.controller import Controller
from GuiLib.test.model import Model

logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('getters.file_getter_glob').setLevel(logging.WARNING)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    # MVC pattern according to "O'REILLY, Entwurfsmuster von Kopf bis Fuss, 2.Auflage", ab Seite. 235
    try:
        model = Model()
        controller = Controller(model)

    finally:
        model.exit()
        logging.debug('end main')


if __name__ == '__main__':
    main()
