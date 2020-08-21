# Created by hillerj at 20.08.2020

from abc import ABC, abstractmethod
import numpy as np


class Drawable(ABC):
    def __init__(self, name='drawable_name', do_draw=True):
        self.name: str = name
        self.do_draw: bool = do_draw

    def __repr__(self):
        return f'drawable: name = {self.name}, do_draw = {self.do_draw}'

    @abstractmethod
    def draw(self, ax):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def get_data(self):
        pass


class DrawablePts(Drawable):
    def __init__(self, name, do_draw=True, pts=[], args=(), **kwargs):
        super().__init__(name, do_draw)
        self.pts = self.update(pts)
        self.args = args
        self.kwargs = kwargs

    def draw(self, ax):
        ax.plot(self.pts[:, 0], self.pts[:, 1], *self.args, **self.kwargs)

    def update(self, pts):
        self.pts = np.array(pts)
        return self.pts

    def get_data(self):
        return self.pts


class DrawableImg(Drawable):
    def __init__(self, name, do_draw=True, img=np.zeros(shape=(10, 10)),
                 args=(), **kwargs):
        super().__init__(name, do_draw)
        self.img = self.update(img)
        self.args = args
        self.kwargs = kwargs

    def draw(self, ax):
        ax.imshow(self.img, *self.args, **self.kwargs)

    def update(self, data):
        self.img = np.array(data)
        return self.img

    def get_data(self):
        return self.img
