# from https://github.com/PySimpleGUI/PySimpleGUI/issues/2710

import PySimpleGUIQt as sg
import numpy as np
import pyqtgraph as pg
from PySide2.QtWidgets import QLabel, QLineEdit

"""
    HIGHLY experimental way for users to add their own widgets to a layout.
    Place a Colummn in the window's layout where you want your Widget to go.
"""

layout = [[sg.Text('My Window')],
          [sg.T('Before Col'), sg.Column([[]], key='-COL-'), sg.T('End of column')],
          [sg.Button('Go'), sg.Button('Exit'),
           sg.Slider(range=(0, 3.14*10), default_value=0, resolution=0.1*10,
                     key='-SLIDER-', orientation='h',
                     enable_events=True)]]

# You must finalize the window before trying to add new widgets, elements to it
window = sg.Window('Window Title', layout, finalize=True, size=(800, 600))

# Get some QT Widgets to add
qlabel = QLabel('Extended element asdfasf asf asdf ')
qedit = QLineEdit()

pg.setConfigOption('background', 'w')
pg.setConfigOption('antialias', True)
plotWidget = pg.plot(title="Three plot curves")
x = np.linspace(0, 1000, 1000)
y = np.random.normal(size=(3, 1000))
plots = []
for i in range(3):
    plots.append(plotWidget.plot(x, np.sin(x * 2 * 3.14 / 100 + i * 2 * 3.14 / 3), pen=(i, 3)))

# Add the widgets to the Column
window['-COL-'].vbox_layout.addWidget(qlabel)
window['-COL-'].vbox_layout.addWidget(qedit)
window['-COL-'].vbox_layout.addWidget(plotWidget)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if 'Go' in event:
        plots[2].setData(np.random.random(100))
    if '-SLIDER-' in event:
        value = values['-SLIDER-']/10
        print(value)
        plots[2].setData(x, np.sin(x * 2 * 3.14 / 100 + value * 2 * 3.14 / 3))
window.close()
