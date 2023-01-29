from typing import NamedTuple, final

from nalpy import math

@final
class RectOffset(NamedTuple):
    left: float
    right: float
    top: float
    bottom: float

    @property
    def horizontal(self) -> float:
        return self.left + self.right

    @property
    def vertical(self) -> float:
        return self.top + self.bottom

    def add(self, rect: math.Rect) -> math.Rect:
        """Add the border offsets to a rect."""

        return math.Rect.from_sides(
            rect.left + self.left,
            rect.top + self.top,
            rect.right - self.right,
            rect.bottom - self.bottom
        )

    def remove(self, rect: math.Rect) -> math.Rect:
        """Remove the border offsets from a rect."""

        return math.Rect.from_sides(
            rect.left - self.left,
            rect.top - self.top,
            rect.right + self.right,
            rect.bottom + self.bottom
        )

    def to_float_tuple(self) -> tuple[float, float, float, float]:
        return (self.left, self.right, self.top, self.bottom)

    def to_int_tuple(self) -> tuple[int, int, int, int]:
        left: int = round(self.left)
        right: int = round(self.right)
        top: int = round(self.top)
        bottom: int = round(self.bottom)
        return (left, right, top, bottom)

    def to_float_dict(self) -> dict[str, float]:
        return self._asdict()
