from typing import Self, final

from .. import hypot, clamp01, sqrt, clamp, acos, degrees, sign, INFINITY, Vector2

@final
class MVector2:
    """A mutable two-dimensional vector"""
    __slots__ = "x", "y"

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    @classmethod
    def from_immutable(cls, immutable: Vector2) -> Self:
        return cls(immutable.x, immutable.y)

    #region Class Properties
    @classmethod
    @property
    def zero(cls) -> Self:
        """Shorthand for ``math.MVector2(0.0, 0.0)``"""
        return cls(0.0, 0.0)

    @classmethod
    @property
    def one(cls) -> Self:
        """Shorthand for ``math.MVector2(1.0, 1.0)``"""
        return cls(1.0, 1.0)


    @classmethod
    @property
    def up(cls) -> Self:
        """A unit vector pointing up (vector j). Shorthand for ``math.MVector2(0.0, 1.0)``"""
        return cls(0.0, 1.0)

    @classmethod
    @property
    def down(cls) -> Self:
        """A unit vector pointing down. Shorthand for ``math.MVector2(0.0, -1.0)``"""
        return cls(0.0, -1.0)

    @classmethod
    @property
    def left(cls) -> Self:
        """A unit vector pointing left. Shorthand for ``math.MVector2(-1.0, 0.0)``"""
        return cls(-1.0, 0.0)

    @classmethod
    @property
    def right(cls) -> Self:
        """A unit vector pointing right (vector i). Shorthand for ``math.MVector2(1.0, 0.0)``"""
        return cls(1.0, 0.0)
    #endregion

    #region Operators

    # Provides __str__ also
    def __repr__(self) -> str:
        """Unambiguous string representation of the vector."""
        return f"MVector2({self.x}, {self.y})"

    def __add__(self, other: Self) -> Self:
        """Add (self + other)"""
        if not isinstance(other, MVector2):
            return NotImplemented
        return MVector2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Self) -> Self:
        """Inline Add (self += other)"""
        if not isinstance(other, MVector2):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Self) -> Self:
        """Subtract (self - other)"""
        if not isinstance(other, MVector2):
            return NotImplemented
        return MVector2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Self) -> Self:
        """Inline Subtract (self -= other)"""
        if not isinstance(other, MVector2):
            return NotImplemented
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Self | float | int) -> Self:
        """Multiply (self * other)"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2(self.x * x, self.y * y)

    def __rmul__(self, other: Self | float | int) -> Self:
        """Reverse multiply (other * self)"""
        return self.__mul__(other) # other * self = self * other

    def __imul__(self, other: Self | float | int) -> Self:
        """Inline Multiply (self *= other)"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        self.x *= x
        self.y *= y
        return self

    def __truediv__(self, other: Self | float | int) -> Self:
        """Divide (self / other)"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2(self.x / x, self.y / y)

    def __itruediv__(self, other: Self | float | int) -> Self:
        """Inline Divide (self /= other)"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        self.x /= x
        self.y /= y
        return self

    def __floordiv__(self, other: Self | float | int) -> Self:
        """Floor Divide (self // other)"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2(self.x // x, self.y // y)

    def __ifloordiv__(self, other: Self | float | int) -> Self:
        """Inline Floor Divide (self //= other)"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        self.x //= x
        self.y //= y
        return self


    def __mod__(self, other: Self | float | int) -> Self:
        """Modulo (self % other)"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2(self.x % x, self.y % y)

    def __divmod__(self, other: Self | float | int) -> tuple[Self, Self]:
        """Floor division and modulo (divmod(self, other))"""
        x: float | int
        y: float | int
        if isinstance(other, MVector2):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        x_fdiv, x_mod = divmod(self.x, x)
        y_fdiv, y_mod = divmod(self.y, y)
        return (MVector2(x_fdiv, y_fdiv), MVector2(x_mod, y_mod))


    def __neg__(self) -> Self:
        """Negate (-self)"""
        return MVector2(-self.x, -self.y)

    def __abs__(self) -> Self:
        """Absolute value (abs(self))"""
        return MVector2(abs(self.x), abs(self.y))

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, MVector2):
            return self.x == other.x and self.y == other.y
        return False
    # Hash not implemented because object is mutable.

    #endregion

    #region Instance Properties
    @property
    def magnitude(self) -> float:
        """The length of this vector."""
        return hypot(self.x, self.y)

    @property
    def normalized(self) -> Self:
        """A copy of this vector with a magnitude of 1"""
        mag: float = self.magnitude
        if mag == 0:
            raise ValueError("Vector does not have a direction to normalize to.")
        return MVector2(self.x / mag, self.y / mag)
    #endregion

    #region Mathematic Operations
    @classmethod
    def dot(cls, a: Self, b: Self) -> float:
        """Dot Product of two vectors."""
        return (a.x * b.x) + (a.y * b.y)
    #endregion

    #region Interpolation
    @classmethod
    def lerp(cls, a: Self, b: Self, t: float) -> Self:
        """
        Linearly interpolates between vectors ``a`` and ``b`` by ``t``.

        The parameter ``t`` is clamped to the range [0, 1].
        """
        t = clamp01(t)
        lerp_x = a.x + ((b.x - a.x) * t)
        lerp_y = a.y + ((b.y - a.y) * t)
        return MVector2(lerp_x, lerp_y)

    @classmethod
    def lerp_unclamped(cls, a: Self, b: Self, t: float) -> Self:
        """
        Linearly interpolates between vectors ``a`` and ``b`` by ``t``.

        The parameter ``t`` is not clamped.
        """
        lerp_x = a.x + ((b.x - a.x) * t)
        lerp_y = a.y + ((b.y - a.y) * t)
        return MVector2(lerp_x, lerp_y)

    @classmethod
    def move_towards(cls, current: Self, target: Self, max_distance_delta: float):
        """Moves a point current towards target."""
        to_vector_x: float = target.x - current.x
        to_vector_y: float = target.y - current.y

        sqDist: float = to_vector_x * to_vector_x + to_vector_y * to_vector_y

        if sqDist == 0 or (max_distance_delta >= 0 and sqDist <= max_distance_delta * max_distance_delta):
            return target

        dist: float = sqrt(sqDist)

        move_x = current.x + to_vector_x / dist * max_distance_delta
        move_y = current.y + to_vector_y / dist * max_distance_delta
        return MVector2(move_x, move_y)

    @classmethod
    def smooth_damp(cls, current: Vector2, target: Vector2, current_velocity: Self, smooth_time: float, delta_time: float, max_speed: float = INFINITY):
        """Due to Python limitations, this method needs to be implemented in MVector2. This will be moved to Vector2 whenever it becomes possible."""
        smooth_time = max(0.0001, smooth_time)
        omega: float = 2.0 / smooth_time

        x: float = omega * delta_time
        exp: float = 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)

        change_x: float = current.x - target.x
        change_y: float = current.y - target.y
        originalTo: Vector2 = target

        # Clamp maximum speed
        maxChange: float = max_speed * smooth_time

        maxChangeSq: float = maxChange * maxChange
        sqDist: float = change_x * change_x + change_y * change_y
        if sqDist > maxChangeSq:
            mag: float = sqrt(sqDist)
            change_x = change_x / mag * maxChange
            change_y = change_y / mag * maxChange

        target = Vector2(current.x - change_x, current.y - change_y)

        temp_x: float = (current_velocity.x + omega * change_x) * delta_time
        temp_y: float = (current_velocity.y + omega * change_y) * delta_time

        current_velocity.x = (current_velocity.x - omega * temp_x) * exp
        current_velocity.y = (current_velocity.y - omega * temp_y) * exp

        output_x: float = target.x + (change_x + temp_x) * exp
        output_y: float = target.y + (change_y + temp_y) * exp

        # Prevent overshooting
        origMinusCurrent_x: float = originalTo.x - current.x
        origMinusCurrent_y: float = originalTo.y - current.y
        outMinusOrig_x: float = output_x - originalTo.x
        outMinusOrig_y: float = output_y - originalTo.y

        if origMinusCurrent_x * outMinusOrig_x + origMinusCurrent_y * outMinusOrig_y > 0:
            output_x = originalTo.x
            output_y = originalTo.y

            current_velocity.x = (output_x - originalTo.x) / delta_time
            current_velocity.y = (output_y - originalTo.y) / delta_time

        return Vector2(output_x, output_y)
    #endregion

    #region Rotation
    @classmethod
    def perpendicular(cls, vector: Self) -> Self:
        """
        Returns a 2D vector with the same magnitude, but perpendicular to the given 2D vector.
        The result is always rotated 90-degrees in a counter-clockwise direction for a 2D coordinate system where the positive Y axis goes up.
        """
        return MVector2(-vector.y, vector.x)

    @classmethod
    def reflect(cls, vector: Self, normal: Self):
        """Reflects a vector off the vector defined by a normal."""
        factor: float = -2 * MVector2.dot(normal, vector)
        return MVector2(factor * normal.x + vector.x, factor * normal.y + vector.y)
    #endregion

    #region Relation
    @classmethod
    def angle(cls, _from: Self, _to: Self) -> float:
        """
        Gets the unsigned angle in degrees between from and to.

        NOTE: The angle returned will always be between 0 and 180 degrees, because the method returns the smallest angle between the vectors.
        """
        denom: float = _from.magnitude * _to.magnitude
        if denom == 0.0:
            return 0.0

        dot: float = MVector2.dot(_from, _to)
        cos_val: float = clamp(dot / denom, -1.0, 1.0)
        return degrees(acos(cos_val))

    @classmethod
    def signed_angle(cls, _from: Self, _to: Self) -> float:
        """
        Gets the signed angle in degrees between from and to. The angle returned is the signed counterclockwise angle between the two vectors.

        NOTE: The angle returned will always be between -180 and 180 degrees, because the method returns the smallest angle between the vectors.
        """
        unsigned_angle: float = MVector2.angle(_from, _to)
        s: float = sign((_from.x * _to.y) - (_from.y * _to.x))
        return unsigned_angle * s

    @classmethod
    def distance(cls, a: Self, b: Self):
        """Returns the distance between a and b."""
        diff = a - b
        return diff.magnitude
    #endregion

    #region Contructors
    @classmethod
    def min(cls, a: Self, b: Self) -> Self:
        """Returns a vector that is made from the smallest components of two vectors."""
        return cls(min(a.x, b.x), min(a.y, b.y))

    @classmethod
    def max(cls, a: Self, b: Self) -> Self:
        """Returns a vector that is made from the largest components of two vectors."""
        return cls(max(a.x, b.x), max(a.y, b.y))
    #endregion

    #region Conversion
    def to_int_tuple(self) -> tuple[int, int]:
        return (round(self.x), round(self.y))

    def to_immutable(self) -> Vector2:
        return Vector2(self.x, self.y)

    def to_float_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y}
    #endregion
