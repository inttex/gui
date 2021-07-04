import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()

imgs = np.random.random((100, 100, 100))
fig = plt.figure(0)
plt.imshow(imgs[0])

ax = plt.gca()
ch = ax.get_children()

plt.cla()
plt.show()

# slow method
tstart = time.time()
for i in np.arange(10):
    print("iteration {}".format(i))
    plt.cla()
    plt.imshow(imgs[i])
    plt.draw()
    time.sleep(0.1)
    plt.pause(.0001)
tend = time.time()
totslow = tend - tstart

plt.cla()

# fast method
tstart = time.time()
for i in np.arange(100):
    print("iteration {}".format(i))
    ch[9].set_data(imgs[i])  # ch[2] is the member of axes that stores the image, AxesImage object
    ax.draw_artist(ch[2])
    fig.canvas.blit()
    fig.canvas.flush_events()
    fig.show()
tend = time.time()
totfast = tend - tstart

print("Slow method timing: {} seconds".format(totslow))
print("Fast method timing: {} seconds".format(totfast))