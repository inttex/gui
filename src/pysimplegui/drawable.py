from abc import ABC, abstractmethod
import matplotlib.pylab as plt


class Drawable(ABC):

    def __init__(self, name, ax):
        self.name = name
        self.ax = ax
        self.do_draw = True
        self.updated = True

    @abstractmethod
    def draw(self, ax):
        raise NotImplemented


class DrawableImage(Drawable):
    def __init__(self, name, ax, image):
        super().__init__(name, ax)
        self.image = image
        self.artist = None

    def draw(self, ax):
        if not self.artist:
            self.initial_draw(ax)
        else:
            self.update()

    def initial_draw(self,ax):
        self.artist = ax.imshow(self.image)

    def update(self, image):
        self.artist.set_data(image)


class DrawablePts(Drawable):
    def __init__(self, name, ax, pts):
        super().__init__(name, ax)
        self.pts = pts
        self.artist = None

    def draw(self, ax, data=None):
        if data is not None:
            self.pts = data
        if self.artist is None:
            self.initial_draw(ax)
        else:
            self.update()

    def initial_draw(self, ax):
        print('initial_draw')
        self.artist, = ax.plot(self.pts[:, 0], self.pts[:, 1], 'rx-')

    def update(self):
        self.artist.set_data(self.pts[:, 0], self.pts[:, 1])
