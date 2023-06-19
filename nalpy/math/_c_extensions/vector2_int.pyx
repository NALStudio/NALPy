#cython: language_level=3

from libc.math cimport hypot, ceil, floor, llround
from libc.stdlib cimport llabs

from nalpy.math import Vector2

ctypedef long long int int_t

cdef class Vector2Int:
    zero = Vector2Int(0, 0)
    one = Vector2Int(1, 1)

    up = Vector2Int(0, 1)
    down = Vector2Int(0, -1)
    left = Vector2Int(-1, 0)
    right = Vector2Int(1, 0)


    cdef readonly int_t x
    cdef readonly int_t y

    def __init__(self, int_t x, int_t y):
        # Vector2Int(x, y)
        self.x = x
        self.y = y

    def __getitem__(self, char i):
        # self[i]
        if i == 0:
            return self.x
        if i == 1:
            return self.y

        raise IndexError(i)

    def __repr__(self):
        # repr(self)
        return f"Vector2Int({self.x}, {self.y})"

    def __add__(self, Vector2Int other):
        # self + other
        return Vector2Int(self.x + other.x, self.y + other.y)

    def __sub__(self, Vector2Int other):
        # self - other
        return Vector2Int(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        # self * other
        if isinstance(other, Vector2Int):
            return Vector2Int(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Vector2Int(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        # other * self
        # Duplicated code because inline function didn't work for some reason...
        if isinstance(other, Vector2Int):
            return Vector2Int(other.x * self.x, other.y * self.y)
        elif isinstance(other, (float, int)):
            return Vector2Int(other * self.x, other * self.y)
        else:
            return NotImplemented

    def __truediv__(self, other):
        # self / other, NOTE: Returns Vector2
        if isinstance(other, Vector2Int):
            return Vector2(self.x / other.x, self.y / other.y)
        elif isinstance(other, (float, int)):
            return Vector2(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        # self // other
        if isinstance(other, Vector2Int):
            return Vector2Int(self.x // other.x, self.y // other.y)
        elif isinstance(other, int):
            return Vector2Int(self.x // other, self.y // other)
        else:
            return NotImplemented

    def __mod__(self, other):
        # self % other
        if isinstance(other, Vector2Int):
            return Vector2Int(self.x % other.x, self.y % other.y)
        elif isinstance(other, int):
            return Vector2Int(self.x % other, self.y % other)
        else:
            return NotImplemented

    def __divmod__(self, other):
        # divmod(self, other)
        cdef int_t x
        cdef int_t y
        if isinstance(other, Vector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int):
            x = other
            y = other
        else:
            return NotImplemented

        x_fdiv, x_mod = divmod(self.x, x)
        y_fdiv, y_mod = divmod(self.y, y)
        return (Vector2Int(x_fdiv, y_fdiv), Vector2Int(x_mod, y_mod))

    def __neg__(self):
        # -self
        return Vector2Int(-self.x, -self.y)

    def __abs__(self):
        # abs(self)
        return Vector2Int(llabs(self.x), llabs(self.y))

    def __eq__(self, Vector2Int other):
        return self.x == other.x and self.y == other.y

    # TODO: Implement __hash__

    @property
    def magnitude(self):
        return hypot(self.x, self.y)

    @staticmethod
    def distance(Vector2Int a, Vector2Int b):
        cdef int_t diff_x = a.x - b.x
        cdef int_t diff_y = a.y - b.y
        return hypot(diff_x, diff_y)

    @staticmethod
    def ceil(v: Vector2) -> Vector2Int:
       return Vector2Int(<int_t>ceil(v.x), <int_t>(ceil(v.y)))

    @staticmethod
    def floor(v: Vector2) -> Vector2Int:
        return Vector2Int(<int_t>floor(v.x), <int_t>(floor(v.y)))

    @staticmethod
    def round(v: Vector2) -> Vector2Int:
        return Vector2Int(<int_t>llround(v.x), <int_t>llround(v.y))
        # Casting in case we change the int_t later. long long int can always hold a rounded double.

    @staticmethod
    def trunc(v: Vector2) -> Vector2Int:
        return Vector2Int(<int_t>v.x, <int_t>v.y) # Casting floating point to integer truncates

    @staticmethod
    def min(Vector2Int a, Vector2Int b):
        return Vector2Int(min(a.x, b.x), min(a.y, b.y))

    @staticmethod
    def max(Vector2Int a, Vector2Int b):
        return Vector2Int(max(a.x, b.x), max(a.y, b.y))

    def to_vector2(self) -> Vector2:
        return Vector2(<double>self.x, <double>self.y)