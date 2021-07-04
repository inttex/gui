import multiprocessing
import numpy as np

from multiproc.shared_np_arr import shm_as_ndarray, ndarray_to_shm


def func_for_proc(sa, sa_shape):
    a = shm_as_ndarray(sa, shape=sa_shape)
    a = a + 1000
    print(a[0, 0])


def main():
    a = np.random.random(size=(300, 300))
    print(a[0, 0])
    sa = ndarray_to_shm(a)
    proc = multiprocessing.Process(target=func_for_proc, args=(sa, np.shape(a)))
    proc.start()
    proc.join()
    print(a[0, 0])


if __name__ == '__main__':
    main()
