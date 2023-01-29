from typing import NamedTuple, final

from nalpy import math

@final
class RectOffsetInt(NamedTuple):
    left: int
    right: int
    top: int
    bottom: int

    @property
    def horizontal(self) -> int:
        return self.left + self.right

    @property
    def vertical(self) -> int:
        return self.top + self.bottom

    def add(self, rect: math.RectInt) -> math.RectInt:
        """Add the border offsets to a rect."""

        return math.RectInt.from_sides(
            rect.left + self.left,
            rect.top + self.top,
            rect.right - self.right,
            rect.bottom - self.bottom
        )

    def remove(self, rect: math.RectInt) -> math.RectInt:
        """Remove the border offsets from a rect."""

        return math.RectInt.from_sides(
            rect.left - self.left,
            rect.top - self.top,
            rect.right + self.right,
            rect.bottom + self.bottom
        )
