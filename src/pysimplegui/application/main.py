# Created by hillerj at 20.08.2020
from time import sleep

from application.controller import Controller
from application.model import Model
from application.view_pysimplegui_with_tree_n_zoom import ViewWithTree


def main():
    controller = Controller()

    model = Model()
    pysimplegui_tree_view = ViewWithTree(controller)
    print('init controller')
    controller.init_with_model_n_view(model, [pysimplegui_tree_view])

    # while pysimplegui_tree_view.is_running():
    #     sleep(0.01)

    pysimplegui_tree_view.loop()


if __name__ == '__main__':
    main()
