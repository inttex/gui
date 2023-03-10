import numpy as np
a = np.array([1, 1, 2, 3, 5, 8])  # Start with an existing NumPy array
from multiprocessing import shared_memory
shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
# Now create a NumPy array backed by shared memory
b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
b[:] = a[:]  # Copy the original data into shared memory
b
array([1, 1, 2, 3, 5, 8])
type(b)


class 'numpy.ndarray'
type(a)
class 'numpy.ndarray'>
shm.name  # We did not specify a name so one was chosen for us
'psm_21467_46075'


see https://docs.python.org/3/library/multiprocessing.shared_memory.html