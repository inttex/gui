from matplotlib.pyplot import figure, show
import numpy as np

import matplotlib as mpl

mpl.rcParams['toolbar'] = 'None'


class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def zoom_factory(self, fig, base_scale=2.):
        def zoom(event):
            # this_ax = ax
            if not hasattr(event.inaxes, 'axes'):
                return
            else:
                ax = event.inaxes.axes
                cur_xlim = ax.get_xlim()
                cur_ylim = ax.get_ylim()

                xdata = event.xdata  # get event x location
                ydata = event.ydata  # get event y location

                if event.button == 'up':
                    # deal with zoom in
                    scale_factor = 1 / base_scale
                elif event.button == 'down':
                    # deal with zoom out
                    scale_factor = base_scale
                else:
                    # deal with something that should never happen
                    scale_factor = 1
                    print(event.button)

                new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

                relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
                rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

                ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
                ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
                ax.figure.canvas.draw()
                # ax.canvas.draw()

        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, fig):
        def onPress(event):
            if not hasattr(event.inaxes, 'axes'):
                return
            else:
                ax = event.inaxes.axes
                if event.inaxes != ax: return
                self.cur_xlim = ax.get_xlim()
                self.cur_ylim = ax.get_ylim()
                self.press = self.x0, self.y0, event.xdata, event.ydata
                self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            if not hasattr(event.inaxes, 'axes'):
                return
            else:
                ax = event.inaxes.axes
                self.press = None
                ax.figure.canvas.draw()

        def onMotion(event):
            if not hasattr(event.inaxes, 'axes'):
                return
            else:
                ax = event.inaxes.axes
                if self.press is None: return
                if event.inaxes != ax: return
                dx = event.xdata - self.xpress
                dy = event.ydata - self.ypress
                self.cur_xlim -= dx
                self.cur_ylim -= dy
                ax.set_xlim(self.cur_xlim)
                ax.set_ylim(self.cur_ylim)
                ax.figure.canvas.draw()

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)

        # return the function
        return onMotion


def main():
    fig = figure()

    ax1 = fig.add_subplot(121, xlim=(0, 1), ylim=(0, 1), autoscale_on=False)
    ax2 = fig.add_subplot(122)  # , autoscale_on=False)

    ax1.set_title('Click to zoom')
    x, y, s, c = np.random.rand(4, 200)
    s *= 200

    ax1.scatter(x, y, s, c)
    ax2.imshow(np.random.rand(20, 20))

    scale = 1.2
    zp = ZoomPan()
    figZoom = zp.zoom_factory(fig, base_scale=scale)
    figPan = zp.pan_factory(fig)
    show()


if __name__ == '__main__':
    main()
