from typing import NamedTuple, Self, final

from nalpy import math


@final
class Rect(NamedTuple):
    """
    A 2D Rectangle defined by X and Y position, width and height.

    In this rectangle the origin represents the top-left corner and Y increases downwards.
    """

    position: math.Vector2
    size: math.Vector2

    #region Constructors
    @classmethod
    def from_corners(cls, topleft: math.Vector2, bottomright: math.Vector2) -> Self:
        size = bottomright - topleft
        return cls(topleft, size)

    @classmethod
    def from_sides(cls, left: float, top: float, right: float, bottom: float) -> Self:
        topleft = math.Vector2(left, top)
        size = math.Vector2(right - left, bottom - top)
        return cls(topleft, size)

    @classmethod
    def from_center(cls, center: math.Vector2, size: math.Vector2) -> Self:
        topleft = center - (size / 2)
        return cls(topleft, size)
    #endregion

    #region Properties
    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    @property
    def w(self) -> float:
        return self.size.x

    @property
    def h(self) -> float:
        return self.size.y

    @property
    def left(self) -> float:
        return self.position.x

    @property
    def right(self) -> float:
        return self.position.x + self.size.x

    @property
    def top(self) -> float:
        return self.position.y

    @property
    def bottom(self) -> float:
        return self.position.y + self.size.y

    @property
    def topleft(self) -> math.Vector2:
        return math.Vector2(self.left, self.top)

    @property
    def bottomleft(self) -> math.Vector2:
        return math.Vector2(self.left, self.bottom)

    @property
    def topright(self) -> math.Vector2:
        return math.Vector2(self.right, self.top)

    @property
    def bottomright(self) -> math.Vector2:
        return math.Vector2(self.right, self.bottom)

    @property
    def midtop(self) -> math.Vector2:
        return math.Vector2(self.center_x, self.top)

    @property
    def midbottom(self) -> math.Vector2:
        return math.Vector2(self.center_x, self.bottom)

    @property
    def midleft(self) -> math.Vector2:
        return math.Vector2(self.left, self.center_y)

    @property
    def midright(self) -> math.Vector2:
        return math.Vector2(self.right, self.center_y)

    @property
    def center_y(self) -> float:
        return self.position.y + (self.size.y / 2.0)

    @property
    def center_x(self) -> float:
        return self.position.x + (self.size.x / 2.0)

    @property
    def center(self) -> math.Vector2:
        return math.Vector2(self.center_x, self.center_y)
    #endregion

    # __eq__ and __hash__ are provided by NamedTuple

    #region Collision checks
    def collide_point(self, point: math.Vector2) -> bool:
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

    #region Normalization
    @classmethod
    def normalized_to_point(cls, rect: Self, normalized_rect_coordinates: math.Vector2) -> math.Vector2:
        return math.Vector2(
            math.lerp(rect.left, rect.right, normalized_rect_coordinates.x),
            math.lerp(rect.top, rect.bottom, normalized_rect_coordinates.y)
        )

    @classmethod
    def point_to_normalized(cls, rect: Self, point: math.Vector2) -> math.Vector2:
        return math.Vector2(
            math.inverse_lerp(rect.left, rect.right, point.x),
            math.inverse_lerp(rect.top, rect.bottom, point.y)
        )
    #endregion

    def to_float_tuple(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.w, self.h)

    def to_int_tuple(self) -> tuple[int, int, int, int]:
        x: int = round(self.x)
        y: int = round(self.y)
        w: int = round(self.w)
        h: int = round(self.h)
        return (x, y, w, h)

    def to_float_dict(self) -> dict[str, float]:
        return self._asdict()
