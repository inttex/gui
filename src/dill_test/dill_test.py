from dataclasses import dataclass

import dill
import numpy as np


@dataclass
class MyClass:
    a: np.array
    f: float


def f(x):
    c = locals()
    print(c)

    dill.dump_session(main=locals())
    y = x ** 2
    z = y + x
    return z


def main():
    arr = np.array([1, 3, 5, 7, 4])
    obj = MyClass(a=arr, f=4)
    res = f(3)
    print(res)


if __name__ == '__main__':
    main()

arr = np.array([1, 3, 5, 7, 4])
obj = MyClass(a=arr, f=4)
res = f(3)
dill.dump_session()
