#cython: language_level=3

from libc.math cimport hypot, acos, fabs

cdef double _rad2deg = 180.0 / 3.14159265358979323846

cdef inline _Vector2Angle(Vector2 _from, Vector2 _to):
    cdef double denom = hypot(_from.x, _from.y) * hypot(_to.x, _to.y) # Multiply magnitudes
    if denom == 0.0:
        return 0.0

    cdef double dot = (_from.x * _to.x) + (_from.y * _to.y)

    cdef double cos_val = dot / denom
    if cos_val < -1.0: # Clamp to range [-1, 1]
        cos_val = -1.0
    elif cos_val > 1.0:
        cos_val = 1.0

    return acos(cos_val) * _rad2deg

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
        # Duplicated code because inline function didn't work for some reason...
        if isinstance(other, Vector2):
            return Vector2(other.x * self.x, other.y * self.y)
        elif isinstance(other, (float, int)):
            return Vector2(other * self.x, other * self.y)
        else:
            return NotImplemented

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
        return Vector2(fabs(self.x), fabs(self.y))

    def __eq__(self, Vector2 other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def magnitude(self):
        return hypot(self.x, self.y)

    @property
    def normalized(self):
        magnitude = hypot(self.x, self.y)
        if magnitude == 0.0:
            raise ValueError("Vector does not have a direction to normalize to.")
        return Vector2(self.x / magnitude, self.y / magnitude)

    @staticmethod
    def dot(Vector2 a, Vector2 b):
        return (a.x * b.x) + (a.y * b.y)

    @staticmethod
    def lerp(Vector2 a, Vector2 b, double t):
        if t < 0.0: # clamp01 substitute
            t = 0.0
        elif t > 1.0:
            t = 1.0

        lerp_x = a.x + ((b.x - a.x) * t)
        lerp_y = a.y + ((b.y - a.y) * t)
        return Vector2(lerp_x, lerp_y)

    @staticmethod
    def lerp_unclamped(Vector2 a, Vector2 b, double t):
        lerp_x = a.x + ((b.x - a.x) * t)
        lerp_y = a.y + ((b.y - a.y) * t)
        return Vector2(lerp_x, lerp_y)

    @staticmethod
    def move_towards(Vector2 current, Vector2 target, double max_distance_delta):
        cdef double to_vector_x = target.x - current.x
        cdef double to_vector_y = target.y - current.y

        cdef double dist = hypot(to_vector_x, to_vector_y)

        if dist == 0 or (max_distance_delta >= 0 and dist <= max_distance_delta):
            return target

        cdef double move_x = current.x + to_vector_x / dist * max_distance_delta
        cdef double move_y = current.y + to_vector_y / dist * max_distance_delta
        return Vector2(move_x, move_y)

    @staticmethod
    def perpendicular(Vector2 vector):
        return Vector2(-vector.y, vector.x)

    @staticmethod
    def reflect(Vector2 vector, Vector2 normal):
        cdef double dot = (normal.x * vector.x) + (normal.y * vector.y)
        cdef double factor = -2.0 * dot
        return Vector2(factor * normal.x + vector.x, factor * normal.y + vector.y)

    @staticmethod
    def angle(Vector2 _from, Vector2 _to):
        return _Vector2Angle(_from, _to)
        # Extracted into a separate inline method to increase signed_angle performance.
        # From my testing this makes Vector2.angle slower by around 2 % which is basically randomness
        # But on the other hand this change makes Vector2.signed_angle around 12 % faster.

    @staticmethod
    def signed_angle(Vector2 _from, Vector2 _to):
        cdef double unsigned_angle = _Vector2Angle(_from, _to)
        if ((_from.x * _to.y) - (_from.y * _to.x)) < 0.0:
            return -unsigned_angle
        else:
            return unsigned_angle

    @staticmethod
    def distance(Vector2 a, Vector2 b):
        cdef double diff_x = a.x - b.x
        cdef double diff_y = a.y - b.y
        return hypot(diff_x, diff_y)

    @staticmethod
    def min(Vector2 a, Vector2 b):
        """Returns a vector that is made from the smallest components of two vectors."""
        return Vector2(min(a.x, b.x), min(a.y, b.y))

    @staticmethod
    def max(Vector2 a, Vector2 b):
        """Returns a vector that is made from the largest components of two vectors."""
        return Vector2(max(a.x, b.x), max(a.y, b.y))
