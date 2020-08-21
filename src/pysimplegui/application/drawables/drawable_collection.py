# Created by hillerj at 20.08.2020
from typing import List, Dict

from application.drawables.drawable import Drawable


class DrawableCollection(Drawable):
    ADDED = 0
    UPDATED = 1

    def __init__(self, name, do_draw=True, drawable_list: List[Drawable] = tuple()):
        super().__init__(name, do_draw)
        self.drawables: Dict[str, Drawable] = {}
        for drw in drawable_list:
            self.add_drawable(drw)

    def add_drawable(self, drawable: Drawable):
        if drawable.name in self.drawables.keys():
            self.drawables[drawable.name].update(drawable.get_data())
            return DrawableCollection.UPDATED
        else:
            self.drawables.update({drawable.name: drawable})
            return DrawableCollection.ADDED

    def draw(self, ax):
        for drw in self.drawables.values():
            if drw.do_draw:
                drw.draw(ax)

    def update(self, data):
        # not applicable
        pass

    def get_data(self):
        pass
