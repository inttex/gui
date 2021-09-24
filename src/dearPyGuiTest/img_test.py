import numpy as np
from time import sleep, time

from threading import Thread

import dearpygui.dearpygui as dpg

image_id = None
texture_id = dpg.generate_uuid()


def update_pmin_pmax():
    # Was working for 0.80 but now broken.

    config = dpg.get_item_configuration(image_id)
    # print(f"current values: {config['pmin']=} {config['pmax']=}")
    pmin = [200, 200]
    pmax = [500, 500]
    # print(f"Updating pmin/pmax to {pmin=} {pmax=}")
    dpg.configure_item(image_id, pmin=pmin, pmax=pmax)
    config = dpg.get_item_configuration(image_id)
    # print(f"updated values: {config['pmin']=} {config['pmax']=}")


def change_texture():
    image = np.ones([300, 300, 4])
    sin = np.sin(np.linspace(0, 10, 300)) ** 2
    image[:, :, 0] = sin
    image[:, :, 1] = sin
    image[:, :, 2] = sin
    dpg.set_value(texture_id, image.flatten())


do_stop = False
last_time = 0

def image_loop():
    sleep(0.1)
    while not do_stop:
        global last_time
        # sleep(0.02)
        t = time()
        fps = 1/(t-last_time)
        last_time=t
        image = np.ones([300, 300, 4])
        sin = np.sin(np.linspace(0, 10, 300) + t*20) ** 2
        sin2 = np.sin(np.linspace(0, 8, 300) + t * 19) ** 2
        sin3 = np.sin(np.linspace(0, 5, 300) + t * 18) ** 2
        image[:, :, 0] = sin
        image[:, :, 1] = sin2
        image[:, :, 2] = sin3.T
        if not dpg.is_dearpygui_running():
            break
        with dpg.mutex():
            dpg.set_value(texture_id, image.flatten())
            dpg.set_value('text_id',f'fps = {fps:0.1f}fps')
            dpg.draw_image()
    print('stop thread')


with dpg.window(label="Image view test", width=800, height=800) as win_id:
    dpg.add_text("Simple text",id = 'text_id')
    dpg.add_button(label="update image pmin/pmax", callback=update_pmin_pmax)
    with dpg.drawlist(width=500, height=500) as draw_id:
        image = []
        for i in range(0, 300 * 300):
            image.append(255 / 255)
            image.append(0)
            image.append(255 / 255)
            image.append(255 / 255)

        texture_container_id = dpg.add_texture_registry(label="Image Texture Container")
        dpg.add_dynamic_texture(300, 300, image, parent=texture_container_id,
                                id=texture_id)
        image_id = dpg.draw_image(texture_id, [0, 0], [300, 300])
        print(dpg.get_item_configuration(image_id))
    dpg.add_button(label='change texture', callback=change_texture)

thread = Thread(target=image_loop)
thread.start()
dpg_thread = Thread(target=dpg.start_dearpygui)
dpg_thread.start()

dpg_thread.join()
do_stop = True

thread.join()
