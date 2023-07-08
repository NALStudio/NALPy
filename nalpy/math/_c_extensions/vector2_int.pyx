#cython: language_level=3

from libc.math cimport hypot, ceil, floor, llround
from libc.stdlib cimport llabs

from .vector2 import Vector2

ctypedef long long int int_t

cdef extern from "Python.h":
    int SIZEOF_PY_HASH_T

# Hashing
ctypedef unsigned long long int _Vec_uhash_t

cdef _Vec_uhash_t _VecHASH_XXPRIME_1 = 11400714785074694791ULL
cdef _Vec_uhash_t _VecHASH_XXPRIME_2 = 14029467366897019727ULL
cdef _Vec_uhash_t _VecHASH_XXPRIME_5 = 2870177450012600261ULL
cdef inline _Vec_uhash_t _VecHASH_XXROTATE(_Vec_uhash_t x):
    return ((x << 31) | (x >> 33)) # Rotate left 31 bits
# Hashing

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

    def __len__(self):
        return 2

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

    # Adapted from tuplehash https://github.com/python/cpython/blob/3.11/Objects/tupleobject.c#L321
    # Doesn't work when extracted into a .pxd file for some reason, that's why this has been copied from vector2.pyx
    def __hash__(self):
        if SIZEOF_PY_HASH_T != 8:
            raise RuntimeError("64 bit hash type required.")

        cdef _Vec_uhash_t xlane = <_Vec_uhash_t>hash(self.x)
        cdef _Vec_uhash_t ylane = <_Vec_uhash_t>hash(self.y)

        if xlane == <_Vec_uhash_t>-1 or ylane == <_Vec_uhash_t>-1:
            return -1

        cdef _Vec_uhash_t acc = _VecHASH_XXPRIME_5

        # X
        acc += xlane * _VecHASH_XXPRIME_2
        acc = _VecHASH_XXROTATE(acc)
        acc *= _VecHASH_XXPRIME_1

        # Y
        acc += ylane * _VecHASH_XXPRIME_2
        acc = _VecHASH_XXROTATE(acc)
        acc *= _VecHASH_XXPRIME_1

        acc += (<Py_ssize_t>2) ^ (_VecHASH_XXPRIME_5 ^ 3527539UL)
        # To keep compatibility with tuple's hash implementation
        # The performance improvement by removing this is negligible

        if acc == <_Vec_uhash_t>-1:
            return 1546275796

        return acc

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

    def to_tuple(self):
        return (self.x, self.y)

    def to_dict(self):
        return {"x": self.x, "y": self.y}
