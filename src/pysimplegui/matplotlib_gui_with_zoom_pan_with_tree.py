#!/usr/bin/env python
from random import randint, random
from time import time

import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Yet another usage of MatPlotLib with animations.
from matplotlib_folder.zoom_pan import ZoomPan
from pysimplegui.drawable import DrawablePts, DrawableImage


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def main():
    NUM_DATAPOINTS = 10000
    # define the form layout

    treedata = sg.TreeData()

    treedata.Insert("", '_A_', 'A', [1, 2, 3])
    treedata.Insert("", '_B_', 'B', [4, 5, 6])
    treedata.Insert("_A_", '_A1_', 'A1', ['can', 'be', 'anything'])

    layout = [[sg.Text('Animated Matplotlib', size=(40, 1),
                       justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(34, 28), key='-CANVAS-'),
               sg.Tree(data=treedata,
                       headings=['Size', 'bla', 'ena'],
                       auto_size_columns=True,
                       num_rows=5,
                       col0_width=40,
                       key='-TREE-',
                       show_expanded=False,
                       enable_events=True),
               ],
              [sg.Canvas(size=(340, 280), key='-CANVAS2-'),
               ],
              [sg.Text('Progress through the data')],
              [sg.Slider(range=(0, NUM_DATAPOINTS), size=(60, 10),
                         orientation='h', key='-SLIDER-')],
              [sg.Text('Number of data points to display on screen')],
              [sg.Slider(range=(10, 500), default_value=40, size=(40, 10),
                         orientation='h', key='-SLIDER-DATAPOINTS-')],
              [sg.Button('Exit', size=(10, 1), pad=((280, 0), 3), font='Helvetica 14')],
              [sg.Button('New'), sg.Button('Shift'), sg.Button('UpdatePts')],
              ]

    # create the form and show it without the plot
    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
                       layout, finalize=True)


    slider_elem = window['-SLIDER-']
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas

    canvas_elem2 = window['-CANVAS2-']
    canvas2 = canvas_elem2.TKCanvas

    # draw the initial plot in the window
    fig1 = Figure(figsize = (5,3))
    fig2 = Figure(figsize = (5,3))

    ax1 = fig1.add_subplot(111)

    ax2 = fig2.add_subplot(111)

    ax1.set_xlabel("X axis")
    ax1.set_ylabel("Y axis")
    ax1.grid()

    fig_agg = draw_figure(canvas, fig1)
    fig_agg2 = draw_figure(canvas2, fig2)
    # make a bunch of random data points

    # see https://stackoverflow.com/questions/60145965/zoom-capable-matplotlib-window-embedded-in-a-pysimplegui-window-tab
    zp1 = ZoomPan()
    figZoom = zp1.zoom_factory(ax1, base_scale=1.2)
    figPan = zp1.pan_factory(ax1)

    zp2 = ZoomPan()
    figZoom2 = zp2.zoom_factory(ax2, base_scale=1.2)
    figPan2 = zp2.pan_factory(ax2)

    dpts = [randint(0, 10) for x in range(NUM_DATAPOINTS)]

    line, = ax1.plot(range(40), [randint(0, 10) for x in range(40)], color='purple')
    pt_line_x = 10
    pt_line, = ax1.plot([pt_line_x, ], [4, ], 'ro')

    drw_pts = []
    drw_pts = np.array([[2, 5],
                        [3, 6]])
    drawable_pts = DrawablePts(name='drawable pts', ax=1, pts=drw_pts)
    drawable_pts.draw(ax1)

    N=20
    drawable_img = DrawableImage(name='drawable_img', ax=2, image=np.random.random((N,N)))
    drawable_img.draw(ax2)

    pts = []
    time_0 = time()

    for i in range(len(dpts)):
        now = time()
        d_time = now - time_0
        # print(f'd_time = {d_time:0.3f} sec')
        time_0 = now

        event, values = window.read(timeout=10)
        if event in ('Exit', None):
            exit(69)
        slider_elem.update(i)  # slider shows "progress" through the data points
        # ax1.cla()  # clear the subplot
        # ax1.grid()  # draw the grid
        data_points = int(values['-SLIDER-DATAPOINTS-'])  # draw this many data points (on next line)
        # ax1.plot(range(data_points), dpts[i:i + data_points], color='purple')
        # ax1.plot(range(5), [1, 4, 3, 4, 4], color='purple')

        line.set_data(range(data_points), dpts[i:i + data_points])

        if event == 'New':
            print(f'new')
            ax1.plot(pt_line_x, randint(0, 10), 'bx')

        if event == 'Shift':
            pt_line_x += 1
            pt_line.set_data(pt_line_x, 4)
            print(f'Shift')

        if event == 'UpdatePts':
            drw_pts = np.vstack([drw_pts, np.array([[6, 4]])])
            drawable_pts.draw(ax1, drw_pts)

        fig_agg.draw()

    window.close()


if __name__ == '__main__':
    main()
