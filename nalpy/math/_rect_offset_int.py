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

    def to_rect_offset(self) -> math.RectOffset:
        return math.RectOffset(
            float(self.left), float(self.right),
            float(self.top), float(self.bottom)
        )

    def to_int_tuple(self) -> tuple[int, int, int, int]:
        """Shorthand for ``(rect.left, rect.right, rect.top, rect.bottom)``"""
        return (self.left, self.right, self.top, self.bottom)

    def to_int_dict(self) -> dict[str, int]:
        return self._asdict()
