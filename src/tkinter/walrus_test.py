class A():
    def __init__(self, a, b, c):
        self.c = c
        self.b = b
        self.a = a


def func(asdf, awe, dv):
    return asdf


def main():
    a = A(2, 4, 5)
    b = a.a

    # NOT WORKING :(
    func(b := 564, awe=3, dv=3)

    print(a.a)


if __name__ == '__main__':
    main()
