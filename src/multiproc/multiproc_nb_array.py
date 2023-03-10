import multiprocessing
from multiprocessing.managers import SharedMemoryManager
import numpy as np


# see https://docs.python.org/3/library/multiprocessing.shared_memory.html


def square_list(memory_lock, shared_mem, m_shape, m_type):
    with memory_lock:
        # create np array, using the existing shared memory
        c = np.ndarray(m_shape, dtype=m_type, buffer=shared_mem.buf)
        for i, val in enumerate(c):
            c[i] = val * val
    print(f"Result(in process p1): {c}, type = {type(c)}, dtype = {c.dtype}")


if __name__ == "__main__":
    with SharedMemoryManager() as smm:
        # create shared memory with a given size
        a = np.arange(5)  # .astype('uint8')
        shared_mem = smm.SharedMemory(a.nbytes)

        # create np array, using the existing shared memory
        b = np.ndarray(a.shape, dtype=a.dtype, buffer=shared_mem.buf)
        b[:] = a[:]  # copy values in shared memory, using the syntax of numpy array

        # example with lock (which in this case is useless)
        memory_lock = multiprocessing.Lock()

        p1 = multiprocessing.Process(target=square_list, args=(memory_lock, shared_mem, a.shape, a.dtype))
        p1.start()
        p1.join()

        print(f"Result(in main): {b}, type = {type(b)}, dtype = {b.dtype}")
