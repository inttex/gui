# Created by hillerj at 20.08.2020
from threading import Thread
from typing import List

from application.controller_interface import ControllerInterface
from application.drawables.drawable_visualizer import DrawableVisualizer
from application.model import Model
from application.view_interface import ViewInterface


class Controller(ControllerInterface):

    def __init__(self):
        self.model: Model = None
        self.views: List[ViewInterface] = []

    def _run_threaded_algo(self, algo, args):
        print('start algo')
        algo(*args)
        print('end algo')
        self._update_views()

    def apply_algo(self, input_data, dv: DrawableVisualizer):
        thread = Thread(target=self._run_threaded_algo, args=(self.model.topo_algo, (input_data, dv)))
        thread.start()

    def init_with_model_n_view(self, model, views):
        self.model = model
        self.views = views

    def _update_views(self):
        for view in self.views:
            view.update_view()
