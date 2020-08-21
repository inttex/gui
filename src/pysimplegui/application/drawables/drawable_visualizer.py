# Created by hillerj at 20.08.2020
from threading import Lock
from typing import List
import numpy as np
import matplotlib.pylab as plt

from application.drawables.drawable import DrawablePts, Drawable
from application.drawables.drawable_collection import DrawableCollection

SHOW_STRING = '☒'
HIDE_STRING = '☐'


class DrawableVisualizer:
    def __init__(self, figure_names: List[str]):
        self.root: dict[str, DrawableCollection] = {}
        self._vis_updated = True
        self._tree_updated = True
        for fig_name in figure_names:
            self.root.update({fig_name: DrawableCollection(name=fig_name)})
        self._lock = Lock()

    def add_drawable(self, fig_name, drawable):
        with self._lock:
            self._vis_updated = True
            added = self.root[fig_name].add_drawable(drawable)
            if added == DrawableCollection.ADDED:
                self._tree_updated = True

    def is_vis_updated(self):
        res = self._vis_updated
        self._vis_updated = False
        return res

    def is_tree_updated(self):
        res = self._tree_updated
        self._tree_updated = False
        return res

    def draw_fig(self, fig_name, ax):
        ax.autoscale(False)
        for artist in ax.lines + ax.collections + ax.images:
            artist.remove()

        with self._lock:
            drw: Drawable
            for drw in self.root[fig_name].drawables.values():
                if drw.do_draw:
                    drw.draw(ax)

    @classmethod
    def _recursive_add(cls, treedata, this_collection: DrawableCollection, parent):
        string = SHOW_STRING if this_collection.do_draw else HIDE_STRING
        treedata.Insert(parent, this_collection, this_collection.name, [string, ])
        for drawable in this_collection.drawables.values():
            if hasattr(drawable, 'drawables'):
                cls._recursive_add(treedata, drawable, this_collection)
            else:
                string = SHOW_STRING if drawable.do_draw else HIDE_STRING
                treedata.Insert(this_collection, drawable, drawable.name, [string, ])

    def create_treedata(self, treedata):
        with self._lock:
            for coll in self.root.values():
                self._recursive_add(treedata, coll, parent='')
            return treedata

    def update_tree(self, tree, empty_tree):
        print('update tree')
        treedata = self.create_treedata(empty_tree)
        tree.update(treedata)
        return treedata


def handle_tree_event(tree, treedata, values):
    def update_value_of_key(key_, new_value_):
        treedata.tree_dict[key_].values[0] = new_value_
        treedata.tree_dict[key_].key.do_draw = new_value_
        string = SHOW_STRING if new_value_ else HIDE_STRING
        tree.update(key=key_, value=string)

    def recursive_update(this_key, new_value_):
        update_value_of_key(this_key, new_value_)
        if hasattr(treedata.tree_dict[this_key], 'children'):
            for child in treedata.tree_dict[this_key].children:
                child_key = child.key
                recursive_update(child_key, new_value)

    for key in values['-TREE-']:
        old_value = tree.TreeData.tree_dict[key].values[0]
        new_value = not old_value
        recursive_update(key, new_value)


def main():
    dv = DrawableVisualizer(['ax1', 'ax2'])
    x = np.linspace(0, 10, 100, endpoint=False)

    dv.add_drawable('ax1', DrawablePts('pts', pts=np.array([x, np.sin(x)]).T, args=('r--',), marker='o'))

    dv.add_drawable('ax2', DrawablePts('pts2', pts=np.array([x, np.sin(2 * x)]).T))

    drw_pts2 = DrawablePts('pts3', pts=np.array([x, np.sin(1.1 * x)]).T, args=('b.-',))
    dv.add_drawable('ax2', drw_pts2)
    # overwrite data, not possible for args and kwargs
    dv.add_drawable('ax2', DrawablePts('pts3', pts=np.array([x, np.sin(3 * x)]).T, args=('r.-',)))

    fig, [ax1, ax2] = plt.subplots(1, 2)

    dv.draw_fig('ax1', ax1)
    dv.draw_fig('ax2', ax2)
    plt.show(block=True)


if __name__ == '__main__':
    main()
