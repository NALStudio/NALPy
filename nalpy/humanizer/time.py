from __future__ import annotations
from datetime import datetime, date, time, timedelta
from enum import Enum
from dataclasses import dataclass
from typing import Iterable
from nalpy import math
from nalpy.humanizer import inflections


@dataclass
class UnitData:
    name: str
    seconds_length: float
    special_one_past_string: str | None = None
    special_one_future_string: str | None = None

    @property
    def raw_name(self):
        return self.name.split(" ", maxsplit=1)[-1]

    def get_suffix(self, future: bool):
        return "from now" if future else "ago"

    def format_as_words(self, amount: int, future: bool):
        if amount == 1:
            if future and self.special_one_future_string is not None:
                return self.special_one_future_string
            if not future and self.special_one_past_string is not None:
                return self.special_one_past_string
            return f"{self.name} {self.get_suffix(future)}"
        else:
            return f"{amount} {self.raw_name}s {self.get_suffix(future)}"

    def format_as_numbers(self, amount: int):
        return inflections.quick_quantisize(self.raw_name, amount)

class TimeUnit(Enum): # NOTE: Must be ordered from smallest to largest
    MILLISECOND = UnitData("a millisecond", 0.001)
    SECOND = UnitData("a second", 1.0)
    MINUTE = UnitData("a minute", 60.0)
    HOUR = UnitData("an hour", 3_600.0)
    DAY = UnitData("a day", 86_400, "yesterday", "tomorrow")
    WEEK = UnitData("a week", 604_800)
    MONTH = UnitData("a month", (365.242199 / 12) * 86_400)
    YEAR = UnitData("a year", 365.242199 * 86_400)


def _get_all_units() -> list[UnitData]:
    return [tu.value for tu in TimeUnit]

def _pick_optimal_unit(seconds: float, min_unit: TimeUnit, max_unit: TimeUnit) -> UnitData:
    units: list[UnitData] = _get_all_units()
    optimal_unit_index: int = units.index(max_unit.value)
    while (seconds / units[optimal_unit_index].seconds_length) < 1.0:
        optimal_unit_index -= 1
        if units[optimal_unit_index] == min_unit.value:
            break
    return units[optimal_unit_index]

def humanize_datetime(_datetime: datetime, just_now_seconds: float = 10.0, min_unit: TimeUnit = TimeUnit.MILLISECOND, max_unit: TimeUnit = TimeUnit.YEAR) -> str:
    """Humanize a datetime

    Args:
        datetime (datetime): The datetime to humanize.
        just_now_seconds (float, optional): Return 'just now' if the difference in seconds is less than the specified value. -1 to disable. Defaults to 10.0.
        min_unit (TimeUnit, optional): The minimum unit to use. Defaults to TimeUnit.Millisecond.
        max_unit (TimeUnit, optional): The maximum unit to use. Defaults to TimeUnit.Year.

    Returns:
        str: [description]
    """
    now = datetime.now()

    delta: timedelta
    if isinstance(_datetime, datetime):
        delta = _datetime - now
    else:
        delta = _datetime - now.date()

    seconds_raw = delta.total_seconds()
    seconds = abs(seconds_raw)

    if seconds < just_now_seconds: # -1 evaluates to false
        return "just now"

    unit = _pick_optimal_unit(seconds, min_unit, max_unit)
    amount = math.floor(seconds / unit.seconds_length)
    return unit.format_as_words(amount, seconds_raw >= 0.0)

def humanize_timedelta(_timedelta: timedelta, precision: int = 1, min_unit: TimeUnit = TimeUnit.MILLISECOND, max_unit: TimeUnit = TimeUnit.YEAR, collection_separator: str = ", ", include_zeros: bool = False, to_words: bool = False) -> str:
    seconds = abs(_timedelta.total_seconds())
    if seconds == 0 and to_words:
        return "no time"

    all_units = _get_all_units()
    optimal = _pick_optimal_unit(seconds, min_unit, max_unit)
    optimal_index = all_units.index(optimal)
    display_units = all_units[max(optimal_index - precision + 1, all_units.index(min_unit.value)):optimal_index + 1]
    display_units.reverse()

    amount_strings: list[str] = []
    remaining_seconds: float = seconds
    for unit in display_units:
        amount = math.floor(remaining_seconds / unit.seconds_length)
        if amount != 0 or include_zeros:
            amount_strings.append(unit.format_as_numbers(amount))
            remaining_seconds -= amount * unit.seconds_length

    return collection_separator.join(amount_strings)

def to_ordinal_words(datetime: datetime | date):
    raise NotImplementedError()

def to_clock_notation(time: time):
    raise NotImplementedError()
