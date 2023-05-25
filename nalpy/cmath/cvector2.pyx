#cython: language_level=3

cdef class CVector2:
    cdef readonly double x
    cdef readonly double y

    def __init__(self, double x, double y):
        self.x = x
        self.y = y

    def __getitem__(self, char i):
        if i == 0 or i == -2:
            return self.x
        if i == 1 or i == -1:
            return self.y

        raise IndexError(i)
