import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo
from math import sin

dpg.show_documentation()

show_demo()

dpg.show_metrics()


def update_plot_data(sender, app_data, plot_data):
    mouse_y = app_data[1]
    if len(plot_data) > 100:
        plot_data.pop(0)
    plot_data.append(sin(mouse_y/30))
    dpg.set_value("plot", plot_data)

data=[]
with dpg.window(label="Tutorial", width=500, height=500):
    myplot = dpg.add_simple_plot(label="Simple Plot", min_scale=-1.0, max_scale=1.0, height=300, id="plot")

    dpg.add_3d_slider(label="abasdf")

with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=update_plot_data, user_data=data)

dpg.start_dearpygui()