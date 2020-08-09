#!/usr/bin/env python
import sys
import os
import PySimpleGUI as sg

"""
    A PySimpleGUI or PySimpleGUIQt demo program that will display a folder heirarchy with icons for the folders and files.
    Note that if you are scanning a large folder then tkinter will eventually complain abouit too many bitmaps and crash
    Getting events back from clicks on the entries works for PySimpleGUI, but appears to not be implemented in PySimpleGUIQt
    If you need tree events using PySimpleGUIQt then post an Issue on the GitHub http://www.PySimpleGUI.com
"""

# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

starting_path = sg.popup_get_folder('Folder to display', default_path='/home/jonas/PycharmProjects/guis/src/')

if not starting_path:
    sys.exit(0)

treedata = sg.TreeData()


def add_files_in_folder(parent, dirname):
    files = os.listdir(dirname)
    for f in files:
        fullname = os.path.join(dirname, f)
        if os.path.isdir(fullname):  # if it's a folder, add folder and recurse
            treedata.Insert(parent, fullname, f, values=[], icon=folder_icon)
            add_files_in_folder(fullname, fullname)
        else:

            treedata.Insert(parent, fullname, f, values=[
                os.stat(fullname).st_size], icon=file_icon)


add_files_in_folder('', starting_path)

tree = sg.Tree(data=treedata,
               headings=['Size', ],
               auto_size_columns=True,
               num_rows=20,
               col0_width=40,
               key='-TREE-',
               show_expanded=False,
               enable_events=True)

layout = [[sg.Text('File and folder browser Test')],
          [tree,
           ],
          [sg.Button('Ok'), sg.Button('Cancel')]]

window = sg.Window('Tree Element Test', layout)

while True:  # Event Loop
    event, values = window.read()
    # key = '/home/jonas/PycharmProjects/guis/src/flask_test.py'
    if event == '-TREE-':
        for key in values['-TREE-']:
            old_value = tree.TreeData.tree_dict[key].values  # treedata.tree_dict[key].values
            new_value = ['0' if 'X' in old_value else 'X']
            treedata.tree_dict[key].values = new_value
            tree.update(key=key, value=new_value)
            # recursive update
            if treedata.tree_dict[key]:
                for child in  treedata.tree_dict[key].children:
                    child_key = child.key
                    treedata.tree_dict[child_key].values = new_value
                    tree.update(key=child_key, value=new_value)
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    print(event, values)
window.close()
