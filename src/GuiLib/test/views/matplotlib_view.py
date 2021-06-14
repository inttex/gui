# Created by hillerj at 14.09.2020
from pathlib import Path
from threading import Thread
from time import sleep
from typing import Type
import numpy as np

from AlgoLib.algos.algo_interface import ApplicationAlgo
from AlgoLib.application.algo_views.post_kerat_view import POST_KERAT_SETTINGS_FILE
from AlgoLib.application.controller_interface import ControllerInterface
from AlgoLib.application.model_tuples import AlgoResultStruct
from GuiLib.drawables.drawable_collector import DrawableTuple
from AlgoLib.application.views.pysimplegui_view import INPUT_DEFAULT_SUB_FOLDER, INPUT_FILENAME, INPUT_DEFAULT_FOLDER
from AlgoLib.application.views.view_interface import AbstractView
from SettingsLib.json_named_tuple import SettingHandler

import matplotlib

matplotlib.use('TkAgg')
import matplotlib as mpl

mpl.rcParams['toolbar'] = 'toolbar2'


class SimpleMatplotLibView(AbstractView):
    def __init__(self, controller: ControllerInterface, algo_cls: Type[ApplicationAlgo]):
        self.algo_cls = algo_cls
        self.controller = controller

        self._init_callback_print = lambda x: print(f'init callback print: {x}')
        self._grab_callback_print = lambda x: print(f'grab callback print: {x}')
        self._algo_callback_print = lambda x: print(f'algo callback print: {x}')

        self.drawables = None

    def _run_view_threaded(self):
        path = Path(INPUT_DEFAULT_FOLDER).joinpath(INPUT_DEFAULT_SUB_FOLDER).joinpath(INPUT_FILENAME)
        self.controller.set_input('files')
        self.controller.init_files_input(path=path, callback=self._init_callback_print)

        sh = SettingHandler(self.algo_cls.get_algo_settings_cls())

        filename = Path(POST_KERAT_SETTINGS_FILE)
        settings_name = self.algo_cls.get_algo_settings_cls().__name__
        out = []
        for i, letter in enumerate(settings_name):
            if letter.isupper():
                if i == 0:
                    letter = letter.lower()
                else:
                    letter = '_' + letter.lower()
            out.append(letter)
        out = ''.join(out) + '.json'
        filename = filename.parent.joinpath(out)
        settings = sh.load_from_file(filename.resolve())
        sh.update_n_write_named_tuple_to_file(settings, filename)

        self.controller.link_algo(self.algo_cls, algo_settings=settings,
                                  algo_link_callback=self._algo_callback_print,
                                  update_view_callback=self._update_view_callback)

        sleep(0.5)  # sleep for files input initialization thread to finish
        self.controller.single_grab(callback=self._grab_callback_print, step=1)

        # visualization
        while self.drawables is None:
            sleep(0.1)
        axes_set = set([a[0] for a in self.drawables])
        import matplotlib.pylab as plt
        nb_rows = 2
        fig, axes = plt.subplots(nb_rows, int(np.ceil(len(axes_set) / nb_rows)), figsize=(12, 7), squeeze=False)
        axes = np.ravel(axes)
        ax_dict = dict()
        for i, ax in enumerate(axes_set):
            ax_dict.update({ax: axes[i]})

        for drawable_tuple in self.drawables:
            drawable_tuple: DrawableTuple
            drawable = drawable_tuple.drawable
            if drawable.do_draw and drawable.updated_data_since_last_draw:
                ax = ax_dict[drawable_tuple.ax_name]
                drawable.global_draw(ax)
        plt.show(block=True)

    def run_view(self):
        Thread(target=self._run_view_threaded, args=()).start()

    def _update_view_callback(self, algo_result: AlgoResultStruct):
        self.drawables = algo_result.drawables
