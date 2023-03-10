import multiprocessing
from multiprocessing import Queue
from multiprocessing.connection import Connection
from time import sleep

import numpy as np

from multiproc.shared_np_arr import shm_as_ndarray, ndarray_to_shm


def func_for_proc(to_:Connection):
    print('start proc')
    while True:
        res = to_.recv()
        if res is None:
            print('exiting process...')
            break
        print(res)
        # print(f'processing {sa} and {sa_shape}')
        # sa, sa_shape = res
        # a = shm_as_ndarray(sa, shape=sa_shape)
        # a = a + 1000


def main():
    res = multiprocessing.Pipe()
    from_, to_ = res
    from_: Connection
    to_: Connection


    proc = multiprocessing.Process(target=func_for_proc, args=(to_,))
    proc.start()

    a = np.random.random(size=(300, 300))
    sa = ndarray_to_shm(a)
    from_.send('hi!! I am Python')
    sleep(1)
    from_.send((sa,np.shape(a)))
    from_.close()

    proc.join()
    print(a[0, 0])

if __name__ == '__main__':
    main()


