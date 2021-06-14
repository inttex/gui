# Created by hillerj at 21.08.2020
from abc import abstractmethod, ABC
from enum import Enum, auto
from typing import List, NamedTuple

from matplotlib.transforms import Affine2D

from GuiLib.drawables.drawable import DrawableImg, DrawablePts, DrawableCirc, DrawableQuiver, DrawableEllipse, DrawableSegments, Drawable
from AlgoLib.application.drawables.drawables_topo import TopoEllipse

class DrawableTuple(NamedTuple):
    ax_name: str
    drawable: Drawable

class DrawableType(Enum):
    PTS = auto()
    SEGMENTS = auto()
    IMG = auto()
    ELL = auto()
    CIRC = auto()
    QUIV = auto()
    TOPO_ELL = auto()


class DrawableCollectorInterface(ABC):
    @abstractmethod
    def create_drawable(self, fig_name: str,
                        drw_type: DrawableType,
                        name: str,
                        data,
                        do_draw: bool = True,
                        transf_to_vis=Affine2D(),
                        *args, **kwargs):
        pass

    @abstractmethod
    def get_new_drawable_tuples(self) -> List[DrawableTuple]:
        pass


class MatplotlibDrawableCollector(DrawableCollectorInterface):

    def __init__(self):
        self.lookup = dict({DrawableType.PTS: DrawablePts,
                            DrawableType.IMG: DrawableImg,
                            DrawableType.ELL: DrawableEllipse,
                            DrawableType.CIRC: DrawableCirc,
                            DrawableType.QUIV: DrawableQuiver,
                            DrawableType.TOPO_ELL: TopoEllipse,
                            DrawableType.SEGMENTS: DrawableSegments,
                            })
        self._new_drawables = []

    def create_drawable(self, fig_name: str,
                        drw_type: DrawableType,
                        name: str,
                        data,
                        do_draw: bool = True,
                        transf_to_vis=Affine2D(),
                        *args, **kwargs):
        drawable_cls = self.lookup[drw_type]
        drawable = drawable_cls(name, data=data,
                                do_draw=do_draw,
                                transform_to_vis=transf_to_vis,
                                args=args,
                                **kwargs)
        self._new_drawables.append(DrawableTuple(fig_name, drawable))

    def get_new_drawable_tuples(self) -> List[DrawableTuple]:
        drawables = self._new_drawables
        self._new_drawables = []
        return drawables

    def clear(self):
        self._new_drawables = []
