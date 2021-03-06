from __future__ import annotations as _annotations

from math import pi as _math_module_pi_constant
import sys as _sys
import typing as _typing

#region public imports of math library functions

# Operations
from math import pow as pow
from math import sqrt as sqrt
from math import log as log

# Geometry
from math import tan as tan
from math import atan as atan
from math import atan2 as atan2
from math import sin as sin
from math import asin as asin
from math import cos as cos
from math import acos as acos

from math import degrees as degrees
from math import radians as radians
from math import hypot as hypot

# Rounding
from math import ceil as ceil
from math import floor as floor

# Value checking
from math import isclose as isclose
from math import isinf as isinf
from math import isnan as isnan

# Value manipulation
from math import modf as modf

#endregion

#region Public imports of components
from nalpy.math.vector2 import Vector2 as Vector2
from nalpy.math.rect import Rect as Rect
#endregion

#region Constants
PI = _math_module_pi_constant
GOLDEN_RATIO = (1 + sqrt(5)) / 2

EPSILON = _sys.float_info.epsilon
"""Difference between 1.0 and the least value greater than 1.0 that is representable as a float."""

INFINITY = float("inf")
NEGATIVEINFINITY = float("-inf")
NAN = float("nan")

MAXVALUE = _sys.maxsize
"""
Maximum size of integer-dependant things.

NOTE: Python integers don't have a maximum value.
"""

MINVALUE = -MAXVALUE - 1
"""
Minimum size of integer-dependant things.

NOTE: Python integers don't have a minimum value.
"""
#endregion

# Initialize TypeVar
Value = _typing.TypeVar("Value", int, float)

#region Basic math functions
def cbrt(__x: _typing.SupportsFloat) -> float:
    x = float(__x)
    if x >= 0:
        return pow(x, 1.0 / 3.0) # Division will be optimized during bytecode compilation
    else:
        return pow(-x, 1.0 / 3.0) * -1 # Division will be optimized during bytecode compilation

def sign(__x: _typing.SupportsFloat) -> int:
    """
    A number that indicates the sign of ``__x``.

    ```
    -1 | less than zero
     0 | equal to zero
    +1 | greater than zero
    ```
    """
    return bool(float(__x) > 0.0) - bool(float(__x) < 0.0)
    # return int(math.copysign(1.0, __x))
    # copysign behaviour is not consistent across different platforms


def is_positive_inf(__x: _typing.SupportsFloat) -> bool:
    """Return ``True`` if ``x`` is positive infinity, and ``False`` otherwise."""
    x = float(__x)
    return isinf(x) and x > 0 # faster than f == INFINITY, supposedly

def is_negative_inf(__x: _typing.SupportsFloat) -> bool:
    """Return ``True`` if ``x`` is negative infinity, and ``False`` otherwise."""
    x = float(__x)
    return isinf(x) and x < 0 # faster than f == NEGATIVEINFINITY, supposedly

def delta_angle(current: float, target: float) -> float:
    """Calculates the shortest difference between two given angles."""
    delta = (target - current) % 360.0
    if delta > 180.0:
        delta -= 360.0
    return delta
#endregion

#region Value Manipulation
def clamp(value: Value, _min: Value, _max: Value) -> Value:
    """Clamps the value to the specified range. Both ends are inclusive."""
    return max(_min, min(value, _max))

def clamp01(value: float) -> float:
    """Shorthand for `math.clamp(value, 0.0, 1.0)`"""
    return clamp(value, 0.0, 1.0)


def remap(value: float, from1: float, to1: float, from2: float, to2: float) -> float:
    """Converts a value to another value within the given arguments. Ends are inclusive."""
    return (value - from1) / (to1 - from1) * (to2 - from2) + from2

def remap01(value: float, from1: float, to1: float) -> float:
    """Converts a value to another value within 0.0 and 1.0. Ends are inclusive."""
    return (value - from1) / (to1 - from1)
#endregion

#region Rounding
#region Away from zero
def round_away_from_zero(__x: _typing.SupportsFloat) -> int:
    """
    Round a number to an integer.
    When a number is halfway between two others, it's rounded toward the nearest number that's away from zero.
    """
    if isnan(__x) or isinf(__x):
        raise ValueError(f"Cannot round value: '{__x}'")

    # Split integral and fractional parts
    fraction, float_value = modf(__x)
    value = int(float_value)

    # Rounding
    if abs(fraction) >= 0.5:
        value += sign(fraction)

    return value
#endregion

#region Nearest n
def round_to_nearest_n(__x: _typing.SupportsFloat, n: int) -> int:
    """
    Round a number to the nearest multiple of ``n``.
    When a number is halfway between two multiples of n, it's rounded toward the nearest number that's away from zero.
    """
    if n == 0: # Prevent division by zero. Any multiple of zero is always zero.
        return 0
    return round_away_from_zero(float(__x) / n) * n

def floor_to_nearest_n(__x: _typing.SupportsFloat, n: int) -> int:
    """
    Floor a number to the nearest multiple of ``n``.
    """
    return floor(float(__x) / n) * n

def ceil_to_nearest_n(__x: _typing.SupportsFloat, n: int) -> int:
    """
    Ceil a number to the nearest multiple of ``n``.
    """
    return ceil(float(__x) / n) * n
#endregion

#region Round to digits
def ceil_to_digits(__x: _typing.SupportsFloat, digits: int = 0) -> float:
    """Return the ceiling of x as a float with specified decimal accuracy."""
    pow10: float = pow(10.0, digits)
    return ceil(float(__x) * pow10) / pow10 # dividing changes output to float

def floor_to_digits(__x: _typing.SupportsFloat, digits: int = 0) -> float:
    """Return the floor of x as a float with specified decimal accuracy."""
    pow10: float = pow(10.0, digits)
    return floor(float(__x) * pow10) / pow10 # dividing changes output to float


def round_away_from_zero_to_digits(__x: _typing.SupportsFloat, digits: int = 0) -> float:
    """
    Round a number to a given precision in decimal digits.
    When a number is halfway between two others, it's rounded toward the nearest number that's away from zero.

    ``digits`` may be negative.
    """
    pow10: float = pow(10.0, digits)
    return round_away_from_zero(float(__x) * pow10) / pow10 # dividing changes output to float


def round_to_nearest_n_to_digits(__x: _typing.SupportsFloat, n: int, digits: int = 0) -> float:
    """
    Round a number to the nearest multiple of ``n`` with specified decimal accuracy.
    """
    pow10: float = pow(10.0, digits)
    return round_to_nearest_n(float(__x) * pow10, n) / pow10 # dividing changes output to float

def floor_to_nearest_n_to_digits(__x: _typing.SupportsFloat, n: int, digits: int = 0) -> float:
    """
    Floor a number to the nearest multiple of ``n`` with specified decimal accuracy.
    """
    pow10: float = pow(10.0, digits)
    return floor_to_nearest_n(float(__x) * pow10, n) / pow10 # dividing changes output to float

def ceil_to_nearest_n_to_digits(__x: _typing.SupportsFloat, n: int, digits: int = 0) -> float:
    """
    Ceil a number to the nearest multiple of ``n`` with specified decimal accuracy.
    """
    pow10: float = pow(10.0, digits)
    return ceil_to_nearest_n(float(__x) * pow10, n) / pow10 # dividing changes output to float
#endregion
#endregion

#region Interpolation
def lerp(a: float, b: float, t: float) -> float:
    """
    Linearly interpolates between ``a`` and ``b`` by ``t``.

    The parameter ``t`` is clamped to the range [0, 1].
    """
    return a + (b - a) * clamp01(t)

def lerp_unclamped(a: float, b: float, t: float) -> float:
    """
    Linearly interpolates between ``a`` and ``b`` by ``t``.

    The parameter ``t`` is not clamped.
    """
    return a + (b - a) * t

def lerp_angle(a: float, b: float, t: float) -> float:
    """
    Same as ``lerp``, but makes sure the values interpolate correctly when they wrap around 360 degrees.

    The parameter t is clamped to the range [0, 1]. Variables a and b are assumed to be in degrees.
    """
    return a + delta_angle(a, b) * clamp01(t)

def smooth_step(a: float, b: float, t: float) -> float:
    """
    Smoothly interpolates between a and b by t.

    The parameter t is clamped to the range [0, 1].
    """
    t = clamp01(t)
    t = -2.0 * t * t * t + 3.0 * t * t
    return b * t + a * (1 - t)

def move_towards(current: float, target: float, maxDelta: float) -> float:
    """
    Moves a value current towards target.

    This is essentially the same as Lerp, but instead the function will ensure that the speed never exceeds maxDelta. Negative values of maxDelta pushes the value away from target.
    """
    if abs(target - current) <= maxDelta:
        return target
    return current + sign(target - current) * maxDelta

def move_towards_angle(current: float, target: float, maxDelta: float) -> float:
    """
    Same as MoveTowards but makes sure the values interpolate correctly when they wrap around 360 degrees.

    Variables current and target are assumed to be in degrees. For optimization reasons, negative values of maxDelta are not supported and may cause oscillation. To push current away from a target angle, add 180 to that angle instead.
    """

    deltaAngle = delta_angle(current, target)
    if -maxDelta < deltaAngle and deltaAngle < maxDelta:
        return target
    target = current + deltaAngle
    return move_towards(current, target, maxDelta)

def ping_pong(t: float, length: float) -> float:
    """
    Returns a value that will increment and decrement between the value 0 and length.

   ``t`` has to be a self-incrementing value.
    """
    t = t % (length * 2.0)
    return length - abs(t - length)
#endregion

#region Iterables
def closest(value: int | float, iterable: _typing.Iterable[Value]) -> Value:
    """Return the value in the iterable that is closest to the given value."""
    comparison_function = lambda k: abs(k - value)
    return min(iterable, key=comparison_function)

def furthest(value: int | float, iterable: _typing.Iterable[Value]) -> Value:
    """Return the value in the iterable that is furthest from the given value."""
    comparison_function = lambda k: abs(k - value)
    return max(iterable, key=comparison_function)
#endregion
