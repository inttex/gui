from time import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()


def f(x, y):
    return np.sin(x) + np.cos(y)


x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)

im = plt.imshow(f(x, y), animated=True)
redDot, = plt.plot([0], [np.sin(0)], 'ro')

time0 = time()


def updatefig(*args):
    global x, y, time0
    now = time()
    print(f'delta t = {now - time0:0.3f}')
    time0 = now
    x += np.pi / 15.
    y += np.pi / 20.
    new_array = f(x, y)

    x0, y0 = np.unravel_index(np.argmax(new_array, axis=None), new_array.shape)
    redDot.set_data(y0, x0)

    im.set_array(new_array)

    return im, redDot


ani = animation.FuncAnimation(fig, updatefig, interval=10, blit=True)
plt.show()
