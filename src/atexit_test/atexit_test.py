from time import sleep

from threading import Thread

import atexit

a = 3


class MyThread(Thread):
    def __init__(self, check_end_condition):
        super(MyThread, self).__init__()
        self.check_end_condition = check_end_condition
        self.n=0

    def run(self):
        self.n = 0
        while not self.check_end_condition():
            sleep(1)
            self.n += 1
        print('stopping thread')


do_stop = False
th = MyThread(check_end_condition=lambda: do_stop)
th.start()


def atexit_func():
    print('inside atexit')
    global do_stop
    do_stop = True
    th.join()
    print('thread stopped')


atexit.register(atexit_func)

print('end of script')
