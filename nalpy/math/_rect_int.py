from typing import Iterable, NamedTuple, Self, final

from nalpy import math


@final
class RectInt(NamedTuple):
    """
    A 2D Rectangle defined by X and Y position, width and height.

    In this rectangle the origin represents the top-left corner and Y increases downwards.
    """

    position: math.Vector2Int
    size: math.Vector2Int

    #region Constructors
    @classmethod
    def from_corners(cls, topleft: math.Vector2Int, bottomright: math.Vector2Int) -> Self:
        size = bottomright - topleft
        return cls(topleft, size)

    @classmethod
    def from_sides(cls, left: int, top: int, right: int, bottom: int) -> Self:
        topleft = math.Vector2Int(left, top)
        size = math.Vector2Int(right - left, bottom - top)
        return cls(topleft, size)
    #endregion

    #region Properties
    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    @property
    def w(self) -> int:
        return self.size.x

    @property
    def h(self) -> int:
        return self.size.y

    @property
    def left(self) -> int:
        return self.position.x

    @property
    def right(self) -> int:
        return self.position.x + self.size.x

    @property
    def top(self) -> int:
        return self.position.y

    @property
    def bottom(self) -> int:
        return self.position.y + self.size.y

    @property
    def topleft(self) -> math.Vector2Int:
        return math.Vector2Int(self.left, self.top)

    @property
    def bottomleft(self) -> math.Vector2Int:
        return math.Vector2Int(self.left, self.bottom)

    @property
    def topright(self) -> math.Vector2Int:
        return math.Vector2Int(self.right, self.top)

    @property
    def bottomright(self) -> math.Vector2Int:
        return math.Vector2Int(self.right, self.bottom)

    @property
    def all_positions_within(self) -> Iterable[math.Vector2Int]:
        for y in range(self.h): # Return by row. (x first then y)
            for x in range(self.w):
                yield math.Vector2Int(self.x + x, self.y + y)
    #endregion

    # __eq__ and __hash__ are provided by NamedTuple

    #region Collision checks
    def collide_point(self, point: math.Vector2Int) -> bool:
        """Checks whether a point lies within the borders of this rect. Includes points that are at the edge of this rect."""
        if self.w <= 0 or self.h <= 0:
            return False # zero or negative sized rects should not collide with anything.

        return (self.left <= point.x <= self.right
                and self.top <= point.y <= self.bottom)

    def collide_rect(self, rect: Self) -> bool:
        """Checks whether another rect overlaps with the borders of this rect. Includes rects that are at the edge of this rect."""
        if self.w <= 0 or self.h <= 0 or rect.w <= 0 or rect.h <= 0:
            return False # zero or negative sized rects should not collide with anything.

        # If any of the checks fail the rectangles don't overlap
        return (
                self.left   <= rect.right
            and self.top    <= rect.bottom
            and self.right  >= rect.left
            and self.bottom >= rect.top
        )
    #endregion

    def to_int_tuple(self) -> tuple[int, int, int, int]:
        """Shorthand for ``(rect.x, rect.y, rect.w, rect.h)``"""
        return (self.x, self.y, self.w, self.h)

    def to_int_dict(self) -> dict[str, int]:
        return self._asdict()
