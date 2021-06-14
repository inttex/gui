# Created by hillerj at 20.08.2020
import logging
from abc import ABC, abstractmethod

import numpy as np
from matplotlib import patches
from matplotlib.transforms import Affine2D

from ell_fit import Ellipse


def plot_line(spt, ept, ax, color='-', linewidth=0.5, markersize=2):
    ax.plot([spt[0], ept[0]], [spt[1], ept[1]], color, linewidth=linewidth, markersize=markersize)


def plot_vect(spt, vect, ax, color='-', linewidth=0.5, markersize=2):
    plot_line(spt, spt + vect, ax, color, linewidth=linewidth, markersize=markersize)


def get_rot_mat(angleRad):
    s = np.sin(angleRad)
    c = np.cos(angleRad)
    return np.array([[c, -s],
                     [s, c], ])


class Drawable(ABC):
    def __init__(self, name='drawable_name', do_draw=True, transf_to_vis=Affine2D()):
        self.name: str = name
        self.do_draw: bool = do_draw
        self.transf_to_vis = transf_to_vis
        self.updated_data_since_last_draw = True

    def __repr__(self):
        type_string = str(type(self)).split("'")[1].split('.')[-1]
        return f'{type_string:<30}\t: name = {self.name:<50}, do_draw = {self.do_draw:<8}\t, updated = {self.updated_data_since_last_draw}'

    @abstractmethod
    def _draw(self, ax):
        pass

    def global_draw(self, ax):
        # print(f'draw {self}')
        try:
            if self.do_draw and self.updated_data_since_last_draw:
                artists = self._draw(ax)
                for artist in artists:
                    trans_data = self.transf_to_vis + ax.transData
                    artist.set_transform(trans_data)
        except Exception as e:
            logging.error(f'exception while drawing {self.name}', exc_info=True)

    @abstractmethod
    def update(self, data):
        pass

    def update_transform(self, transf_to_vis):
        self.transf_to_vis = transf_to_vis

    @abstractmethod
    def get_data(self):
        pass


class DrawablePts(Drawable):
    def __init__(self, name,
                 data=[],
                 do_draw=True,
                 transform_to_vis=Affine2D(),
                 args=(), **kwargs):
        super().__init__(name, do_draw, transform_to_vis)
        self.pts = self.update(data)
        self.args = args
        self.kwargs = kwargs

    def _draw(self, ax):
        artist, = ax.plot(self.pts[:, 0], self.pts[:, 1], *self.args, **self.kwargs)
        return [artist, ]

    def update(self, pts):
        self.pts = np.array(pts)
        return self.pts

    def get_data(self):
        return self.pts


class DrawableImg(Drawable):
    def __init__(self, name,
                 data=np.zeros(shape=(10, 10)),
                 do_draw=True,
                 transform_to_vis=Affine2D(),
                 args=(), **kwargs):
        super().__init__(name, do_draw, transform_to_vis)
        self.img = self.update(data)
        self.args = args
        self.kwargs = kwargs

    def _draw(self, ax):
        artist = ax.imshow(self.img, *self.args, **self.kwargs)
        return [artist, ]

    def update(self, data):
        self.img = np.array(data)
        return self.img

    def get_data(self):
        return self.img


class DrawableCirc(Drawable):
    def __init__(self, name,
                 data=(0, 0, 10),
                 do_draw=True,
                 transform_to_vis=Affine2D(),
                 args=(), **kwargs):
        super().__init__(name, do_draw, transform_to_vis)
        self.x, self.y, self.radius = self.update(data)
        self.args = args
        self.kwargs = kwargs

    def _draw(self, ax):
        artist = patches.Circle((self.x, self.y),
                                radius=self.radius,
                                fill=False, *self.args, **self.kwargs)
        ax.add_artist(artist)
        return [artist, ]

    def update(self, data):
        self.x, self.y, self.radius = data
        return data

    def get_data(self):
        return self.x, self.y, self.radius


class DrawableEllipse(Drawable):
    def __init__(self, name,
                 data=(0, 0, 10),
                 do_draw=True,
                 transform_to_vis=Affine2D(),
                 args=(), **kwargs):
        super().__init__(name, do_draw, transform_to_vis)
        self.ell: Ellipse = self.update(data)
        self.args = args
        self.kwargs = kwargs

    def _draw(self, ax):
        ell = self.ell
        ellipse_patch = patches.Ellipse(ell.center, ell.r_major * 2, ell.r_minor * 2, np.degrees(ell.angle_rad_major),
                                        fill=False, *self.args, **self.kwargs)
        keys = self.kwargs.keys()
        keys = [k for k in keys if k not in ['alpha', 'transparency']]
        kwargs = {key: self.kwargs[key] for key in keys}
        plot_vect(ell.center, ell.r_major * get_rot_mat(ell.angle_rad_major).dot(np.array([1, 0])), ax=ax, *self.args, **kwargs)
        plot_vect(ell.center, 0.5 * ell.r_minor * get_rot_mat(ell.angle_rad_major).dot(np.array([0, 1])), ax=ax, *self.args, **kwargs)
        ax.add_artist(ellipse_patch)
        return [ellipse_patch, ]

    def update(self, data):
        self.ell = data
        return data

    def get_data(self):
        return self.ell


class DrawableSegments(Drawable):
    def __init__(self, name,
                 data=(0, 0, 10),
                 do_draw=True,
                 transform_to_vis=Affine2D(),
                 args=(), **kwargs):
        super().__init__(name, do_draw, transform_to_vis)
        self.data = self.update(data)
        self.args = args
        self.kwargs = kwargs

    def _draw(self, ax):
        artists = []
        for pts in self.data:
            x = pts[0::2]
            y = pts[1::2]
            artist, = ax.plot(x, y, *self.args, **self.kwargs)
            artists.append(artist)
        return artists

    def update(self, data):
        self.data = data
        return data

    def get_data(self):
        return self.data


class DrawableQuiver(Drawable):
    def __init__(self, name,
                 data=(0, 0, 0, 0),
                 do_draw=True,
                 transform_to_vis=Affine2D(),
                 args=(), **kwargs):
        super().__init__(name, do_draw, transform_to_vis)
        self.x, self.y, self.vx, self.vy = self.update(data)
        self.args = args
        self.kwargs = kwargs

    def _draw(self, ax):
        artist = ax.quiver(self.x, self.y, self.vx, self.vy,
                           *self.args, **self.kwargs)
        return [artist, ]

    def update(self, data):
        self.x, self.y, self.vx, self.vy = data
        return data

    def get_data(self):
        return self.x, self.y, self.vx, self.vy
