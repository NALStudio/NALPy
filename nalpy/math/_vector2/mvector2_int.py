from typing import Self, final

from .. import hypot, ceil, floor, MVector2, Vector2Int

@final
class MVector2Int:
    """A mutable two-dimensional vector with integer precision."""
    __slots__ = "x", "y"

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    @classmethod
    def from_immutable(cls, immutable: Vector2Int) -> Self:
        return cls(immutable.x, immutable.y)

    #region Class Properties
    @classmethod
    @property
    def zero(cls) -> Self:
        """Shorthand for ``math.Vector2Int(0, 0)``"""
        return cls(0, 0)

    @classmethod
    @property
    def one(cls) -> Self:
        """Shorthand for ``math.Vector2Int(1, 1)``"""
        return cls(1, 1)


    @classmethod
    @property
    def up(cls) -> Self:
        """A unit vector pointing up (vector j). Shorthand for ``math.Vector2Int(0, 1)``"""
        return cls(0, 1)

    @classmethod
    @property
    def down(cls) -> Self:
        """A unit vector pointing down. Shorthand for ``math.Vector2Int(0, -1)``"""
        return cls(0, -1)

    @classmethod
    @property
    def left(cls) -> Self:
        """A unit vector pointing left. Shorthand for ``math.Vector2Int(-1, 0)``"""
        return cls(-1, 0)

    @classmethod
    @property
    def right(cls) -> Self:
        """A unit vector pointing right (vector i). Shorthand for ``math.Vector2Int(1, 0)``"""
        return cls(1, 0)
    #endregion

    #region Operators

    # Provides __str__ also
    def __repr__(self) -> str:
        """Unambiguous string representation of the vector."""
        return f"MVector2Int({self.x}, {self.y})"

    def __add__(self, other: Self) -> Self:
        """Add (self + other)"""
        if not isinstance(other, MVector2Int):
            return NotImplemented
        return MVector2Int(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Self) -> Self:
        """Inline Add (self += other)"""
        if not isinstance(other, MVector2Int):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Self) -> Self:
        """Subtract (self - other)"""
        if not isinstance(other, MVector2Int):
            return NotImplemented
        return MVector2Int(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Self) -> Self:
        """Inline Subtract (self -= other)"""
        if not isinstance(other, MVector2Int):
            return NotImplemented
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Self | int) -> Self:
        """Multiply (self * other)"""
        x: int
        y: int
        if isinstance(other, MVector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2Int(self.x * x, self.y * y)

    def __rmul__(self, other: Self | int) -> Self:
        """Reverse multiply (other * self)"""
        return self.__mul__(other) # other * self = self * other

    def __imul__(self, other: Self | int) -> Self:
        """Inline Multiply (self *= other)"""
        x: int
        y: int
        if isinstance(other, MVector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int):
            x = other
            y = other
        else:
            return NotImplemented

        self.x *= x
        self.y *= y
        return self

    def __truediv__(self, other: Self | int | float) -> MVector2:
        """Divide (self / other)"""
        x: float
        y: float
        if isinstance(other, MVector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int | float):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2(self.x / x, self.y / y)

    def __floordiv__(self, other: Self | int) -> Self:
        """Floor Divide (self // other)"""
        x: int
        y: int
        if isinstance(other, MVector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2Int(self.x // x, self.y // y)

    def __ifloordiv__(self, other: Self | int) -> Self:
        """Inline Floor Divide (self //= other)"""
        x: int
        y: int
        if isinstance(other, MVector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int):
            x = other
            y = other
        else:
            return NotImplemented

        self.x //= x
        self.y //= y
        return self


    def __mod__(self, other: Self | int) -> Self:
        """Modulo (self % other)"""
        x: int
        y: int
        if isinstance(other, MVector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int):
            x = other
            y = other
        else:
            return NotImplemented

        return MVector2Int(self.x % x, self.y % y)

    def __divmod__(self, other: Self | int) -> tuple[Self, Self]:
        """Floor division and modulo (divmod(self, other))"""
        x: int
        y: int
        if isinstance(other, MVector2Int):
            x = other.x
            y = other.y
        elif isinstance(other, int):
            x = other
            y = other
        else:
            return NotImplemented

        x_fdiv, x_mod = divmod(self.x, x)
        y_fdiv, y_mod = divmod(self.y, y)
        return (MVector2Int(x_fdiv, y_fdiv), MVector2Int(x_mod, y_mod))


    def __neg__(self) -> Self:
        """Negate (-self)"""
        return MVector2Int(-self.x, -self.y)

    def __abs__(self) -> Self:
        """Absolute value (abs(self))"""
        return MVector2Int(abs(self.x), abs(self.y))

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, MVector2Int):
            return self.x == other.x and self.y == other.y
        return False
    # Hash not implemented because object is mutable.

    #endregion

    #region Instance Properties
    @property
    def magnitude(self) -> float:
        """The length of this vector."""
        return hypot(self.x, self.y)
    #endregion

    #region Relation
    @classmethod
    def distance(cls, a: Self, b: Self):
        """Returns the distance between a and b."""
        diff = a - b
        return diff.magnitude
    #endregion

    #region Constructors
    @classmethod
    def ceil(cls, v: MVector2) -> Self:
        return cls(ceil(v.x), ceil(v.y))

    @classmethod
    def floor(cls, v: MVector2) -> Self:
        return cls(floor(v.x), floor(v.y))

    @classmethod
    def round(cls, v: MVector2) -> Self:
        return cls(round(v.x), round(v.y))

    @classmethod
    def min(cls, a: Self, b: Self) -> Self:
        """Returns a vector that is made from the smallest components of two vectors."""
        return cls(min(a.x, b.x), min(a.y, b.y))

    @classmethod
    def max(cls, a: Self, b: Self) -> Self:
        """Returns a vector that is made from the largest components of two vectors."""
        return cls(max(a.x, b.x), max(a.y, b.y))
    #endregion

    #region Conversions
    def to_mvector2(self) -> MVector2:
        return MVector2(float(self.x), float(self.y))

    def to_immutable(self) -> Vector2Int:
        return Vector2Int(self.x, self.y)

    def to_int_dict(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y}
    #endregion
