# Created by hillerj at 20.08.2020
from GuiLib.drawables.drawable_collector import MatplotlibDrawableCollector
from GuiLib.test.controller_interface import ControllerInterface
from GuiLib.test.model import Model
from GuiLib.test.views.pysimplegui_view import ViewWithTree


class Controller(ControllerInterface):

    def __init__(self, model):
        self.model: Model = model
        self.view = ViewWithTree(self)
        # pysguiview will stay in loop and only quit at the end of the program
        # cannot be run in a separate thread, due to some tkinter limitations (tkinter has to run in main thread)

        self._dc = MatplotlibDrawableCollector()

        self.view.run_view() # this call is run until the GUI stops
        # NO CODE AFTER THIS


    def init_files_input(self, input, callback):
        self.model.init_files_input(input, callback)


    def exit(self):
        print('stopping controller')
        self.model.exit()

    def run_algo(self, algo_input, visual_result_callback):
        self.model.apply_algo(algo_input, self._dc, visual_result_callback)
