from typing import NamedTuple, Self, final, Final

from nalpy import math


@final
class Vector2Int(NamedTuple):
    """An immutable two-dimensional vector with integer precision."""
    x: int
    y: int

    #region Class Properties
    @classmethod
    @property
    def zero(cls) -> Self:
        """Shorthand for ``math.Vector2Int(0, 0)``"""
        return _ZERO #  Returning single instance, because Vector2Int is immutable

    @classmethod
    @property
    def one(cls) -> Self:
        """Shorthand for ``math.Vector2Int(1, 1)``"""
        return _ONE #  Returning single instance, because Vector2Int is immutable


    @classmethod
    @property
    def up(cls) -> Self:
        """A unit vector pointing up (vector j). Shorthand for ``math.Vector2Int(0, 1)``"""
        return _UP #  Returning single instance, because Vector2Int is immutable

    @classmethod
    @property
    def down(cls) -> Self:
        """A unit vector pointing down. Shorthand for ``math.Vector2Int(0, -1)``"""
        return _DOWN #  Returning single instance, because Vector2Int is immutable

    @classmethod
    @property
    def left(cls) -> Self:
        """A unit vector pointing left. Shorthand for ``math.Vector2Int(-1, 0)``"""
        return _LEFT #  Returning single instance, because Vector2Int is immutable

    @classmethod
    @property
    def right(cls) -> Self:
        """A unit vector pointing right (vector i). Shorthand for ``math.Vector2Int(1, 0)``"""
        return _RIGHT #  Returning single instance, because Vector2Int is immutable
    #endregion

    #region Operators

    # Provides __str__ also
    def __repr__(self) -> str:
        """Unambiguous string representation of the vector."""
        return f"Vector2Int({self.x}, {self.y})"

    def __add__(self, other: Self) -> Self:
        """Add"""
        return Vector2Int(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        """Subtract"""
        return Vector2Int(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Self | int) -> Self:
        """Multiply"""
        x: int
        y: int
        if isinstance(other, Vector2Int):
            x = other.x
            y = other.y
        else:
            x = other
            y = other

        return Vector2Int(self.x * x, self.y * y)

    def __truediv__(self, other: Self | float | int) -> math.Vector2:
        """Divide"""
        x: float
        y: float
        if isinstance(other, Vector2Int):
            x = other.x
            y = other.y
        else:
            x = other
            y = other

        return math.Vector2(self.x / x, self.y / y)

    def __floordiv__(self, other: Self | int) -> Self:
        """Floor Divide"""
        x: int
        y: int
        if isinstance(other, Vector2Int):
            x = other.x
            y = other.y
        else:
            x = other
            y = other

        return Vector2Int(self.x // x, self.y // y)

    def __neg__(self) -> Self:
        """Negate"""
        return Vector2Int(-self.x, -self.y)

    def __abs__(self) -> Self:
        return Vector2Int(abs(self.x), abs(self.y))

    # __eq__ and __hash__ are provided by NamedTuple

    #endregion

    #region Instance Properties
    @property
    def magnitude(self) -> float:
        """The length of this vector."""
        return math.hypot(self.x, self.y)
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
    def ceil(cls, v: math.Vector2) -> Self:
        return cls(math.ceil(v.x), math.ceil(v.y))

    @classmethod
    def floor(cls, v: math.Vector2) -> Self:
        return cls(math.floor(v.x), math.floor(v.y))

    @classmethod
    def round(cls, v: math.Vector2) -> Self:
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

    def to_int_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def to_int_dict(self) -> dict[str, int]:
        return self._asdict()

_ZERO: Final[Vector2Int] = Vector2Int(0, 0)
_ONE: Final[Vector2Int] = Vector2Int(1, 1)

_UP: Final[Vector2Int] = Vector2Int(0, 1)
_DOWN: Final[Vector2Int] = Vector2Int(0, -1)
_LEFT: Final[Vector2Int] = Vector2Int(-1, 0)
_RIGHT: Final[Vector2Int] = Vector2Int(1, 0)
