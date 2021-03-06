import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pylab as plt
import numpy as np
import time

# fig, ax = plt.subplots()
# line, = ax.plot(np.random.randn(100))
# plt.show(block=False)
#
# tstart = time.time()
# num_plots = 0
# while time.time()-tstart < 1:
#     line.set_ydata(np.random.randn(100))
#     fig.canvas.draw()
#     fig.canvas.flush_events()
#     num_plots += 1
# print(num_plots)

fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100))
plt.show(block=False)

tstart = time.time()
num_plots = 0
while time.time() - tstart < 5:
    line.set_ydata(np.random.randn(100))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.update()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots / 5)
