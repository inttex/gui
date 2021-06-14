# Created by hillerj at 20.08.2020

import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from GuiLib.drawables.drawable_visualizer import DrawableVisualizer, handle_tree_event
from GuiLib.test.controller_interface import ControllerInterface
from GuiLib.test.model_tuples import AlgoResult, AlgoInput
from GuiLib.test.views.view_interface import AbstractView
from GuiLib.vis.zoom_pan import ZoomPan

sg.theme('SandyBeach')


class ViewWithTree(AbstractView):

    def __init__(self, controller: ControllerInterface):
        self.controller = controller
        self.window = None

        self._dv = DrawableVisualizer(figure_names=['ax1', 'ax21', 'ax22', 'ax23'])
        self._window = None
        self._do_update_view = True
        self._fig_agg1, self._ax1 = None, None
        self._fig_agg2, self._ax21, self._ax22, self._ax23 = None, None, None, None

    def _create_frame(self):
        self._canvas1 = sg.Canvas(size=(15, 15), key='-CANVASV1-')
        self._canvas2 = sg.Canvas(size=(15, 15), key='-CANVASV2-')

        self.treedata = self._dv.create_treedata(sg.TreeData())
        self.tree = sg.Tree(data=self.treedata,
                            headings=['show'],
                            auto_size_columns=False,
                            num_rows=20,
                            col0_width=20,
                            col_widths=[4],
                            key='-VIS_TREE-',
                            show_expanded=True,
                            enable_events=True, font='Helvetica 9')

        self._sliders = [sg.Slider((3, 10), 5, 1, 1, key='-SLIDER1-', enable_events=True),
                         sg.Slider((10, 100), 20, 2, 10, key='-SLIDER2-', enable_events=True),
                         sg.Slider((0, 2 * np.pi), 0, 0.33, 1, key='-SLIDER3-', enable_events=True),
                         ]
        self._algo_button = sg.Button('Run Algo', key='-RUN_ALGO-')
        self._algo_success = sg.Text('run first', size=(8, 1), justification='center')
        self._txt_output = sg.Multiline('This is what a Multi-line Text Element looks like', size=(80, 2), autoscroll=True)
        self._button1 = sg.Button('test callback', key='-BUTTON1-')
        self._txt_callback = sg.Text('bla', size=(30, 0), justification='center', text_color='red', key='-CALLBACK_OUT-')

        self._output_layout = [[self._canvas1, self._canvas2, self.tree],
                               [*self._sliders, self._algo_button, self._txt_output, self._algo_success],
                               [self._button1, self._txt_callback]]

        window = sg.Window('Topo_GUI', self._output_layout, finalize=True,
                           element_justification='center',
                           font='Helvetica 10',
                           location=(0, 0),  # (3840, 0),
                           return_keyboard_events=True,
                           )
        # before preparing these figures, the sg.Window has to be created!
        self._fig_agg1, self._ax1 = prepare_figure1(self._canvas1)
        self._fig_agg2, self._ax21, self._ax22, self._ax23 = prepare_figure2(self._canvas2)

        self.window = window

    def grabber_callback(self, res: str):
        self.window['-CALLBACK_OUT-'].update(res)

    def visual_result_callback(self, algo_result: AlgoResult):
        self._dv.set_all_data_obsolete()
        for drawable_tuple in algo_result.drawable_tuples:
            self._dv.add_drawable(*drawable_tuple)
        if algo_result.success:
            self._algo_success.update('Success', background_color='green')
        else:
            self._algo_success.update('Failed', background_color='red')
        self._txt_output.update('')
        self._txt_output.print(algo_result.txt)
        self._do_update_view = True

    def handle_evts(self, event, values, window, controller):
        if event == '-BUTTON1-':
            self.controller.init_files_input('input', self.grabber_callback)
        if event == '-RUN_ALGO-' or '-SLIDER' in event:
            algo_input = AlgoInput(values['-SLIDER1-'],
                                   values['-SLIDER2-'],
                                   values['-SLIDER3-'])
            self.controller.run_algo(algo_input, self.visual_result_callback)
        if self._dv.is_tree_updated():
            self.treedata = self._dv.update_tree(self.tree, empty_tree=sg.TreeData())
        if event == '-VIS_TREE-':
            handle_tree_event(self.tree, self.treedata, values, treename='-VIS_TREE-')
            self._do_update_view = True
        if self._dv.is_vis_updated() or self._do_update_view:
            # print('update view')
            self._do_update_view = False
            self._dv.draw_fig('ax1', self._ax1)
            self._dv.draw_fig('ax21', self._ax21)
            self._dv.draw_fig('ax22', self._ax22)
            self._dv.draw_fig('ax23', self._ax23)
            self._fig_agg1.draw()
            self._fig_agg2.draw()

    def run_view(self):
        self._create_frame()
        self.initialize_drawing_elements()

        # according to a strict model view control pattern, some of the below code should be externalized to the controller
        print('start gui mainloop')
        window = self.window

        event, values = window.read(timeout=0)

        while True:
            event, values = window.read(timeout=100)
            self.handle_evts(event, values, window, self.controller)

            if event is None:
                break
            if '__TIMEOUT__' not in str(event):
                # print(event, values)
                pass
            if event == sg.WIN_CLOSED:
                break

        print(f'closing pysimplegui window, terminating thread')
        self.controller.exit()
        window.close()

    def initialize_drawing_elements(self):
        algo_input = AlgoInput(5, 10, 0)
        self.controller.run_algo(algo_input, self.visual_result_callback)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def prepare_figure1(canvas):
    fig = Figure(figsize=(7, 6))
    ax1 = fig.add_subplot(111)
    ax1.grid(alpha=0.5)

    ax1.set_xlim(-10, 110)
    ax1.set_ylim(-11, 11)
    ax1.invert_yaxis()
    # ax1.set_aspect(1.0, anchor='C')
    # ax1.axis('equal')
    ax1.autoscale(False)
    fig.set_tight_layout(True)

    fig_agg1 = draw_figure(canvas.TKCanvas, fig)
    zp1 = ZoomPan()
    _ = zp1.zoom_factory(fig, base_scale=1.2)
    _ = zp1.pan_factory(fig)
    return fig_agg1, ax1


def prepare_figure2(canvas):
    fig = Figure(figsize=(7, 6))
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)
    for ax in [ax1, ax2, ax3]:
        ax.set_ylim(-2, 2)
        ax.get_xaxis().set_visible(False)
        ax.grid(alpha=0.5)

    fig.set_tight_layout(True)

    fig_agg1 = draw_figure(canvas.TKCanvas, fig)
    zp1 = ZoomPan()
    _ = zp1.zoom_factory(fig, base_scale=1.2, only_y=True)
    _ = zp1.pan_factory(fig)
    return fig_agg1, ax1, ax2, ax3
