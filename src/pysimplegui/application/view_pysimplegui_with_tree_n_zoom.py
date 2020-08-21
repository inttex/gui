# Created by hillerj at 20.08.2020
from threading import Thread

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from application.controller import Controller
from application.drawables.drawable import DrawablePts, DrawableImg
from application.drawables.drawable_collection import DrawableCollection
from application.drawables.drawable_visualizer import DrawableVisualizer, handle_tree_event
from application.view_interface import ViewInterface
from application.zoom_pan import ZoomPan

# sg.theme('LightBrown8')
sg.theme('Default1')
# sg.theme('DarkBrown')
sg.theme('SandyBeach')


# theme_name_list = sg.theme_list()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def prepare_figure(canvas):
    fig = Figure(figsize=(5, 4))
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel("X axis")
    ax1.set_ylabel("Y axis")
    ax1.grid()
    ax1.set_xlim(0, 20)
    ax1.set_ylim(-10, 10)
    fig_agg = draw_figure(canvas.TKCanvas, fig)
    zp1 = ZoomPan()
    _ = zp1.zoom_factory(fig, base_scale=1.2)
    _ = zp1.pan_factory(fig)
    return fig_agg, ax1


def prepare_figure2(canvas):
    fig = Figure(figsize=(2, 2))
    ax1 = fig.add_subplot(111)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    fig_agg = draw_figure(canvas.TKCanvas, fig)
    zp1 = ZoomPan()
    _ = zp1.zoom_factory(fig, base_scale=1.2)
    _ = zp1.pan_factory(fig)
    return fig_agg, ax1


class ViewWithTree(ViewInterface):

    def __init__(self, controller: Controller):
        self.controller = controller

        self.dv = DrawableVisualizer(['ax1', 'ax2'])
        x = np.linspace(0, 10, 100, endpoint=False)
        self.dv.add_drawable('ax1', DrawablePts('pts', pts=np.array([x, np.sin(x)]).T, args=('r--',), marker=','))

        collection = DrawableCollection('collection1')
        self.dv.add_drawable('ax1', collection)
        collection.add_drawable(DrawablePts('pts2', pts=np.array([2 * x, 2 * np.sin(2 * x)]).T, args=('g-',)))
        collection.add_drawable(DrawablePts('pts3', pts=np.array([2 * x, 3 + 2 * np.sin(2 * x)]).T, args=('g-',)))
        self.do_update_view = True
        self.thread = Thread(target=self._loop)
        self.thread.setDaemon(True)
        self.thread.start()

    def add_drawable(self, fig_name, drawable):
        self.dv.add_drawable(fig_name, drawable)

    def is_running(self):
        return self.thread.is_alive()

    def _loop(self):
        self.button = sg.Button(button_text='T0', key='-T0-')
        self.sec_text = sg.InputText(default_text='1', key='-IN-')
        self.text = sg.Text('blabla', key='-TEXT-')
        self.canvas = sg.Canvas(size=(35, 21), key='-CANVAS-')
        self.canvas2 = sg.Canvas(size=(10, 10), key='-CANVAS2-')

        treedata = self.dv.create_treedata(sg.TreeData())
        tree = sg.Tree(data=treedata,
                       headings=['show'],
                       auto_size_columns=False,
                       num_rows=10,
                       col0_width=15,
                       col_widths=[4],
                       key='-TREE-',
                       show_expanded=True,
                       enable_events=True, font='Helvetica 9')

        layout = [[self.button],
                  [self.canvas, tree],
                  [self.canvas2, sg.Button('add img', key='-T1-')],
                  [sg.Slider(range=(0.5, 3), default_value=1.0, size=(40, 10),
                             orientation='h', key='-SLIDER-', enable_events=True, resolution=0.1)],
                  [self.text],
                  ]

        window = sg.Window('LED_Driver_GUI', layout, finalize=True,
                           element_justification='center',
                           font='Helvetica 18', location=(100, 0))

        fig_agg, ax1 = prepare_figure(self.canvas)
        fig_agg2, ax2 = prepare_figure2(self.canvas2)

        while True:
            # read the form
            event, values = window.read(timeout=100)
            if event is None:
                break
            if '__TIMEOUT__' not in event:
                print(event, values)

            # perform button and keyboard operations
            if event == sg.WIN_CLOSED:
                break
            if event == '-SLIDER-':
                slider_value = values['-SLIDER-']
                self.text.update(slider_value)
                self.controller.apply_algo(input_data=slider_value, dv=self.dv)
            if event == '-T0-':
                y = 2 * np.linspace(0, 3, 100, endpoint=False) - 8
                x = 10 * np.sin(y * 1.2) + 10
                self.dv.add_drawable('ax1', DrawablePts('vert_sin', pts=np.array([x, y]).T, args=('m--',)))
            if event == '-T1-':
                fig = np.random.random(size=(10, 10))
                self.dv.add_drawable('ax2', DrawableImg('rand_img', img=fig, cmap='plasma_r'))
            if self.dv.is_tree_updated():
                treedata = self.dv.update_tree(tree, empty_tree=sg.TreeData())
            if event == '-TREE-':
                handle_tree_event(tree, treedata, values)
                self.do_update_view = True
            if self.dv.is_vis_updated() or self.do_update_view:
                print('update view')
                self.do_update_view = False
                self.dv.draw_fig('ax1', ax1)
                self.dv.draw_fig('ax2', ax2)

            fig_agg.draw()
            fig_agg2.draw()

        print(f'closing pysimplegui window, terminating thread')
        window.close()

    def update_view(self):
        self.do_update_view = True
