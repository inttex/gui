# Created by hillerj at 20.08.2020
from threading import Lock
from typing import List

from GuiLib.drawables.drawable import Drawable
from GuiLib.drawables.drawable_collection import DrawableCollection

SHOW_STRING = '☒'
HIDE_STRING = '☐'


class DrawableVisualizer:
    def __init__(self, figure_names: List[str]):
        self.root: DrawableCollection = DrawableCollection(name='root')
        self._vis_updated = True
        self._tree_updated = True
        for fig_name in figure_names:
            self.root.add_drawable(DrawableCollection(name=fig_name))
        self._lock = Lock()
        self._coll_dict = dict()
        self._coll_dict = self._update_collection_dict()

    def _update_collection_dict(self):
        d = dict()

        def recursive_add(node: DrawableCollection):
            for name, drw in node.drawables.items():
                if type(drw) == DrawableCollection:
                    d.update({name: drw})
                    recursive_add(drw)

        d.update({'root': self.root})
        recursive_add(self.root)

        self._coll_dict.update(d)
        return d

    def add_drawable(self, fig_name, drawable):
        with self._lock:
            self._vis_updated = True
            if fig_name not in self._coll_dict:
                print(f'warning: {fig_name} does not exist. existing collections {[v.name for v in self._coll_dict.values()]}')
            added = self._coll_dict[fig_name].add_drawable(drawable)
            self._coll_dict[fig_name].updated_data_since_last_draw = True

            if type(drawable) == DrawableCollection:
                self._update_collection_dict()

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
        for artist in ax.lines + ax.collections + ax.images + ax.artists:
            artist.remove()

        with self._lock:
            drw: Drawable
            for collection in self.root.drawables[fig_name].drawables.values():
                collection.global_draw(ax)

    @classmethod
    def _recursive_tree_creation_add(cls, treedata, this_collection: DrawableCollection, parent):
        string = SHOW_STRING if this_collection.do_draw else HIDE_STRING
        treedata.Insert(parent, this_collection, this_collection.name, [string, ])
        for drawable in this_collection.drawables.values():
            if hasattr(drawable, 'drawables'):
                cls._recursive_tree_creation_add(treedata, drawable, this_collection)
            else:
                string = SHOW_STRING if drawable.do_draw else HIDE_STRING
                treedata.Insert(this_collection, drawable, drawable.name, [string, ])

    def create_treedata(self, treedata):
        with self._lock:
            for coll in self.root.drawables.values():
                self._recursive_tree_creation_add(treedata, coll, parent='')
            return treedata

    def update_tree(self, tree, empty_tree):
        # print('update tree')
        treedata = self.create_treedata(empty_tree)
        tree.update(treedata)
        return treedata

    def set_all_data_obsolete(self):
        def recursive_func(parent: Drawable):
            if hasattr(parent, 'drawables'):
                for drw in parent.drawables.values():
                    recursive_func(drw)
            else:
                parent.updated_data_since_last_draw = False

        for collection in self.root.drawables.values():
            recursive_func(collection)


def handle_tree_event(tree, treedata, values, treename = '-TREE-'):
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

    for key in values[treename]:
        old_value = tree.TreeData.tree_dict[key].values[0]
        new_value = not old_value
        recursive_update(key, new_value)
