import PySimpleGUIQt as sg
import numpy as np
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QComboBox, QFormLayout, QVBoxLayout, \
    QHBoxLayout, QListWidget, QDial, QTableWidget
import pyqtgraph as pg

# from https://github.com/PySimpleGUI/PySimpleGUI/issues/2710

"""
    HIGHLY experimental way for users to add their own widgets to a layout.
    Place a Colummn in the window's layout where you want your Widget to go.
"""

layout = [[sg.Text('My Window')],
          [sg.T('Before Col'), sg.Column([[]], key='-COL-'), sg.T('End of column')],
          [sg.Button('Go'), sg.Button('Exit')]]

# You must finalize the window before trying to add new widgets, elements to it
window = sg.Window('Window Title', layout, finalize=True)

# Get some QT Widgets to add
qlabel = QLabel('Extended element')
qlabel3 = QLabel('Extended element3')
qlabel4 = QLabel('Extended element4')
qedit = QLineEdit()
# Add the widgets to the Column
window['-COL-'].vbox_layout.addWidget(qlabel)
window['-COL-'].vbox_layout.addWidget(qlabel3)
window['-COL-'].vbox_layout.addWidget(qlabel4)
window['-COL-'].vbox_layout.addWidget(qedit)

plt = pg.plot()
plt.setGeometry(100, 100, 600, 500)
plt.setMinimumSize(400, 300)
plt.setWindowTitle('pyqtgraph example: Legend')
plt.addLegend()
l = pg.LegendItem((100, 60), offset=(70, 30))  # args are (size, offset)
l.setParentItem(plt.graphicsItem())  # Note we do NOT call plt.addItem in this case

x = np.linspace(1, 3 * np.pi, 100)
y = np.sin(x)
c1 = plt.plot(x, y, pen='r', symbol='o', symbolPen='r', symbolBrush=0.5, name='red plot')
c2 = plt.plot([2, 1, 4, 3], pen='g', fillLevel=0, fillBrush=(255, 255, 255, 30), name='green plot')
# l.addItem(c1, 'red plot')
# l.addItem(c2, 'green plot')
window['-COL-'].vbox_layout.addWidget(plt)

t = 0
while True:  # Event Loop
    event, values = window.read(timeout=10)
    t += 1
    y = np.sin(x + t/10)
    c1.setData(x,y)
    if not 'TIMEOUT' in event:
        print(event, values)
    if event in (None, 'Exit'):
        break
window.close()
