import threading
from time import sleep
from flask import Flask

app = Flask(__name__)

import PySimpleGUIWeb as sg

layout = [[sg.Text('Filename', text_color='red', key='_TEXT_')],
          [sg.Input(key='_INPUT_'), sg.FileBrowse()],
          [sg.OK(key='_OK BUTTON_'), sg.Cancel()]]

window = sg.Window('Get filename example').Layout(layout)


@app.route('/')
def hello():
    msg = 'hello route /'
    print(msg)
    return msg


@app.route('/asdf/')
def asdf():
    msg = 'route /asdf7'
    print(msg)
    return msg


def threadfun():
    print('start1')
    sleep(2)
    print('end sleep 1')

    app.run(host='0.0.0.0', port=5001)
    print('end1')


def pysimpleguithred():
    print('start2')
    sleep(2)
    print('end sleep 2')

    while True:
        event, values = window.Read()
        if event in (None, 'Quit'):
            break
        if event == '_OK BUTTON_':
            asdf()
            window.Element('_TEXT_').Update(values['_INPUT_'])
    window.close()
    print('end2')


def main():
    th1 = threading.Thread(target=threadfun)
    th2 = threading.Thread(target=pysimpleguithred)
    print('thread is starting.....')
    th1.start()
    th2.start()
    # The Event Loop
    print('thread is running.....')


if __name__ == '__main__':
    main()
