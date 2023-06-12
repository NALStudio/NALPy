#cython: language_level=3

cdef class Vector2:
    zero = Vector2(0.0, 0.0)
    one = Vector2(1.0, 1.0)

    up = Vector2(0.0, 1.0)
    down = Vector2(0.0, -1.0)
    left = Vector2(-1.0, 0.0)
    right = Vector2(1.0, 0.0)


    cdef readonly double x
    cdef readonly double y

    def __init__(self, double x, double y):
        # Vector2(x, y)
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
        return f"Vector2({self.x}, {self.y})"

    def __add__(self, Vector2 other):
        # self + other
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, Vector2 other):
        # self - other
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        # self * other
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (float, int)):
            return Vector2(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        # other * self
        return self.__mul__(other)

    def __truediv__(self, other):
        # self / other
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        elif isinstance(other, (float, int)):
            return Vector2(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        # self // other
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        elif isinstance(other, (float, int)):
            return Vector2(self.x // other, self.y // other)
        else:
            return NotImplemented

    def __mod__(self, other):
        # self % other
        if isinstance(other, Vector2):
            return Vector2(self.x % other.x, self.y % other.y)
        elif isinstance(other, (float, int)):
            return Vector2(self.x % other, self.y % other)
        else:
            return NotImplemented

    def __divmod__(self, other):
        # divmod(self, other)
        cdef double x
        cdef double y
        if isinstance(other, Vector2):
            x = other.x
            y = other.y
        elif isinstance(other, (float, int)):
            x = other
            y = other
        else:
            return NotImplemented

        x_fdiv, x_mod = divmod(self.x, x)
        y_fdiv, y_mod = divmod(self.y, y)
        return (Vector2(x_fdiv, y_fdiv), Vector2(x_mod, y_mod))

    def __neg__(self):
        # -self
        return Vector2(-self.x, -self.y)

    def __abs__(self):
        # abs(self)
        return Vector2(abs(self.x), abs(self.y))

    def __eq__(self, Vector2 other):
        return self.x == other.x and self.y == other.y

    # TODO: Implement __hash__
