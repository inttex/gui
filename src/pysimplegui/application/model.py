# Created by hillerj at 20.08.2020
from time import sleep

import numpy as np

from application.drawables.drawable import DrawablePts
from application.drawables.drawable_visualizer import DrawableVisualizer


class Model:

    def apply_algo(self, input, dv: DrawableVisualizer):
        print(f'running algo with input: {input}')
        sleep(3)
        x = 2 * np.linspace(0, 10, 100, endpoint=False)
        y = 3 * np.sin(x * input) + 8
        dv.add_drawable('ax1', DrawablePts('algo_pts', pts=np.array([x, y]).T, args=('b-',)))
