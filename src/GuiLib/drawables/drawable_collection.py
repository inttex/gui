# Created by hillerj at 20.08.2020
from typing import List, Dict

from GuiLib.drawables.drawable import Drawable


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
            self.drawables[drawable.name].update_transform(drawable.transf_to_vis)
            self.drawables[drawable.name].updated_data_since_last_draw = True
            # TODO: very ugly in order to update kwargs
            self.drawables[drawable.name].kwargs = drawable.kwargs
            return DrawableCollection.UPDATED
        else:
            self.drawables.update({drawable.name: drawable})
            self.drawables[drawable.name].updated_data_since_last_draw = True
            return DrawableCollection.ADDED

    def _draw(self, ax):
        for drw in self.drawables.values():
            drw.global_draw(ax)
        return []

    def update(self, data):
        # not applicable
        pass

    def get_data(self):
        pass
