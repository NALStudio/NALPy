from __future__ import annotations

from typing import NamedTuple

from nalpy import math


class Vector2(NamedTuple):
    """An immutable two-dimensional vector"""
    x: float
    y: float

    #region Class Properties
    @classmethod
    @property
    def zero(cls) -> math.Vector2:
        """Shorthand for ``math.Vector2(0.0, 0.0)``"""
        return _ZERO #  Returning single instance, because Vector2 is immutable

    @classmethod
    @property
    def one(cls) -> math.Vector2:
        """Shorthand for ``math.Vector2(1.0, 1.0)``"""
        return _ONE #  Returning single instance, because Vector2 is immutable
    #endregion

    #region Operators
    def __str__(self) -> str:
        """Human-readable string representation of the vector."""
        return f"Vector2({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Unambiguous string representation of the vector."""
        return repr((self.x, self.y))

    def __add__(self, other: Vector2) -> Vector2:
        """Add"""
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        """Subtract"""
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Vector2 | float | int) -> Vector2:
        """Multiply"""
        x: float
        y: float
        if isinstance(other, Vector2):
            x = other.x
            y = other.y
        else:
            x = other
            y = other

        return Vector2(self.x * x, self.y * y)

    def __truediv__(self, other: Vector2 | float | int) -> Vector2:
        """Divide"""
        x: float
        y: float
        if isinstance(other, Vector2):
            x = other.x
            y = other.y
        else:
            x = other
            y = other

        return Vector2(self.x / x, self.y / y)

    def __floordiv__(self, other: Vector2 | float | int) -> Vector2:
        """Floor Divide"""
        x: float | int
        y: float | int
        if isinstance(other, Vector2):
            x = other.x
            y = other.y
        else:
            x = other
            y = other

        return Vector2(self.x // x, self.y // y)

    def __neg__(self) -> Vector2:
        """Negate"""
        return Vector2(-self.x, -self.y)

    def __abs__(self) -> Vector2:
        return Vector2(abs(self.x), abs(self.y))

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Vector2) and __o.x == self.x and __o.y == self.y
    #endregion

    #region Modifier Properties
    @property
    def magnitude(self) -> float:
        """The length of this vector."""
        return math.hypot(self.x, self.y)

    @property
    def normalized(self) -> Vector2:
        """A copy of this vector with a magnitude of 1"""
        mag: float = self.magnitude
        if mag == 0:
            raise ZeroDivisionError("Vector's magnitude is zero!")
        return Vector2(self.x / mag, self.y / mag)
    #endregion

    #region Mathematic Operations
    @staticmethod
    def dot(a: Vector2, b: Vector2):
        """Dot Product of two vectors."""
        return (a.x * b.x) + (a.y * b.y)
    #endregion

    #region Interpolation
    @staticmethod
    def lerp(a: Vector2, b: Vector2, t: float) -> Vector2:
        """
        Linearly interpolates between vectors ``a`` and ``b`` by ``t``.

        The parameter ``t`` is clamped to the range [0, 1].
        """
        t = math.clamp01(t)
        lerp_x = a.x + ((b.x - a.x) * t)
        lerp_y = a.y + ((b.y - a.y) * t)
        return Vector2(lerp_x, lerp_y)

    @staticmethod
    def lerp_unclamped(a: Vector2, b: Vector2, t: float) -> Vector2:
        """
        Linearly interpolates between vectors ``a`` and ``b`` by ``t``.

        The parameter ``t`` is not clamped.
        """
        lerp_x = a.x + ((b.x - a.x) * t)
        lerp_y = a.y + ((b.y - a.y) * t)
        return Vector2(lerp_x, lerp_y)

    @staticmethod
    def move_towards(current: Vector2, target: Vector2, max_distance_delta: float):
        to_vector_x: float = target.x - current.x
        to_vector_y: float = target.y - current.y

        sqDist: float = to_vector_x * to_vector_x + to_vector_y * to_vector_y

        if sqDist == 0 or (max_distance_delta >= 0 and sqDist <= max_distance_delta * max_distance_delta):
            return target

        dist: float = math.sqrt(sqDist)

        move_x = current.x + to_vector_x / dist * max_distance_delta
        move_y = current.y + to_vector_y / dist * max_distance_delta
        return Vector2(move_x, move_y)
    #endregion

    #region Rotation
    @staticmethod
    def perpendicular(vector: Vector2) -> Vector2:
        """
        Returns a 2D vector with the same magnitude, but perpendicular to the given 2D vector.
        The result is always rotated 90-degrees in a counter-clockwise direction for a 2D coordinate system where the positive Y axis goes up.
        """
        return Vector2(-vector.y, vector.x)

    @staticmethod
    def reflect(vector: Vector2, normal: Vector2):
        """Reflects a vector off the vector defined by a normal."""
        factor: float = -2 * Vector2.dot(normal, vector)
        return Vector2(factor * normal.x + vector.x, factor * normal.y + vector.y)
    #endregion

    #region Relation
    @staticmethod
    def angle(_from: Vector2, _to: Vector2) -> float:
        """Gets the unsigned angle in degrees between from and to."""
        denom: float = _from.magnitude * _to.magnitude
        if denom == 0:
            return 0.0

        dot: float = Vector2.dot(_from, _to)
        cos_val: float = math.clamp(dot / denom, -1.0, 1.0)
        return math.degrees(math.acos(cos_val))

    @staticmethod
    def signed_angle(_from: Vector2, _to: Vector2) -> float:
        unsigned_angle: float = Vector2.angle(_from, _to)
        sign: float = math.sign((_from.x * _to.y) - (_from.y * _to.x))
        return unsigned_angle * sign

    @staticmethod
    def distance(a: Vector2, b: Vector2):
        diff = a - b
        return diff.magnitude
    #endregion

    def to_float_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def to_int_tuple(self) -> tuple[int, int]:
        return (round(self.x), round(self.y))

_ZERO = Vector2(0.0, 0.0)
_ONE = Vector2(1.0, 1.0)
