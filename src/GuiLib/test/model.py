# Created by hillerj at 20.08.2020
import logging
from threading import Thread, Lock
from time import sleep

import numpy as np
from matplotlib.transforms import Affine2D

from GuiLib.drawables.drawable_collector import DrawableCollectorInterface, DrawableType
from GuiLib.test.model_tuples import AlgoInput, AlgoResult


class Model:
    def __init__(self):
        self.algo_settings_lock = Lock()
        self.current_algo_thread = None

    @staticmethod
    def _thread_target_with_callback(target_method, args, callback):
        logging.debug(f'start threaded execution {target_method}')
        result_for_callback = target_method(*args)
        logging.debug('end threaded execution')
        callback(result_for_callback)

    @classmethod
    def _run_threaded_with_callback(cls, target_method, algo_args, callback_method):
        thread = Thread(target=cls._thread_target_with_callback,
                        args=(target_method, algo_args, callback_method))
        thread.start()

    def init_files_input(self, input, callback):
        self._run_threaded_with_callback(target_method=self._init_files_input_threaded,
                                         algo_args=(input,),
                                         callback_method=callback)

    def _init_files_input_threaded(self, input):
        return f'callback of input {input}'

    def apply_algo(self, algo_input: AlgoInput, dc: DrawableCollectorInterface, callback):
        self._run_threaded_with_callback(target_method=self._apply_algo,
                                         algo_args=(algo_input, dc, callback),
                                         callback_method=callback)

    def _apply_algo(self, algo_input: AlgoInput, dc: DrawableCollectorInterface, callback):
        print(f'running algo with input: {input}')
        # sleep(1)
        x = 2 * np.linspace(0, algo_input.slider2, 1000, endpoint=False)
        y = algo_input.slider1 * np.sin(x + algo_input.slider3)
        dc.create_drawable('ax1', DrawableType.PTS, name='algo_pts', data=np.array([x, y]).T, color='b', linestyle='-')
        dc.create_drawable('ax1', DrawableType.PTS, name='algo_pts_transformed', data=np.array([x, y]).T,
                           color='r', linestyle=':', linewidth=10, alpha = 0.3,
                           transf_to_vis=Affine2D().translate(0.5,0.5).rotate_deg(10))
        return AlgoResult('result_string', dc.get_new_drawable_tuples(), success=True)

    def exit(self):
        print('stopping model')
