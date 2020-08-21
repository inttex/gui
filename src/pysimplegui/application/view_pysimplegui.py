# Created by hillerj at 20.08.2020
from threading import Thread
from time import sleep

from application.controller import Controller
from application.view_interface import ViewInterface
import PySimpleGUI as sg


class View(ViewInterface):
    def __init__(self, controller: Controller):
        self.controller = controller
        self.thread = Thread(target=self._loop)
        self.thread.setDaemon(True)
        self.thread.start()

    def is_running(self):
        return self.thread.is_alive()

    def _loop(self):
        self.button = sg.Button(button_text='T0', key='-T0-')
        self.sec_text = sg.InputText(default_text='1', key='-IN-')
        layout = [[self.button],
                  [sg.Text('blabla')],
                  ]

        window = sg.Window('LED_Driver_GUI', layout, finalize=True,
                           element_justification='center',
                           font='Helvetica 18')

        while True:
            # read the form
            event, values = window.read()
            print(event, values)
            # perform button and keyboard operations
            if event == sg.WIN_CLOSED:
                break
            if event == '-T0-':
                self.controller.apply_algo(input_data=1)
            sleep(0.05)

        print(f'closing pysimplegui window, terminating thread')
        window.close()

    def update_view(self):
        pass
