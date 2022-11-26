from enum import Enum
from nalpy import math
from typing import Iterable, NamedTuple, Self, TypeVar


class _Scale(NamedTuple):
    name: str
    symbol: str
    value_base: int
    value_exp: int

    @property
    def value(self) -> int:
        return pow(self.value_base, self.value_exp)

    @classmethod
    def create_empty_scale(cls, base: int) -> Self:
        return cls(name="", symbol="", value_base=base, value_exp=0)


class MetricPrefix(Enum):
    QUETTA = _Scale("quetta", "Q",  10,  30)
    RONNA  = _Scale("ronna",  "R",  10,  27)
    YOTTA  = _Scale("yotta",  "Y",  10,  24)
    ZETTA  = _Scale("zetta",  "Z",  10,  21)
    EXA    = _Scale("exa",    "E",  10,  18)
    PETA   = _Scale("peta",   "P",  10,  15)
    TERA   = _Scale("tera",   "T",  10,  12)
    GIGA   = _Scale("giga",   "G",  10,  9)
    MEGA   = _Scale("mega",   "M",  10,  6)
    KILO   = _Scale("kilo",   "k",  10,  3)
    HECTO  = _Scale("hecto",  "h",  10,  2)
    DECA   = _Scale("deca",   "da", 10,  1)

    DECI   = _Scale("deci",   "d",  10, -1)
    CENTI  = _Scale("centi",  "c",  10, -2)
    MILLI  = _Scale("milli",  "m",  10, -3)
    MICRO  = _Scale("micro",  "μ",  10, -6)
    NANO   = _Scale("nano",   "n",  10, -9)
    PICO   = _Scale("pico",   "p",  10, -12)
    FEMTO  = _Scale("femto",  "f",  10, -15)
    ATTO   = _Scale("atto",   "a",  10, -18)
    ZEPTO  = _Scale("zepto",  "z",  10, -21)
    YOCTO  = _Scale("yocto",  "y",  10, -24)
    RONTO  = _Scale("ronto",  "r",  10, -27)
    QUECTO = _Scale("quecto", "q",  10, -30)

    @property
    def value(self) -> _Scale:
        val = super().value
        assert isinstance(val, _Scale)
        return val

    @staticmethod
    def get_optimal_for_value(base_value: float):
        return _pick_optimal_prefix(base_value, MetricPrefix)

class BinaryPrefix(Enum):
    KIBI = _Scale("kibi", "Ki", 2, 10)
    MEBI = _Scale("mebi", "Mi", 2, 20)
    GIBI = _Scale("gibi", "Gi", 2, 30)
    TEBI = _Scale("tebi", "Ti", 2, 40)
    PEBI = _Scale("pebi", "Pi", 2, 50)
    EXBI = _Scale("exbi", "Ei", 2, 60)
    ZEBI = _Scale("zebi", "Zi", 2, 70)
    YOBI = _Scale("yobi", "Yi", 2, 80)

    @property
    def value(self) -> _Scale:
        val = super().value
        assert isinstance(val, _Scale)
        return val

    @staticmethod
    def get_optimal_for_value(base_value: float):
        return _pick_optimal_prefix(base_value, BinaryPrefix)

_PrefixT = TypeVar("_PrefixT", MetricPrefix, BinaryPrefix)

def convert_metric(input_: float, input_scale: MetricPrefix | BinaryPrefix | None, output_scale: MetricPrefix | BinaryPrefix | None) -> float:
    i_scale: _Scale
    if input_scale is not None:
        i_scale = input_scale.value
    elif output_scale is not None:
        i_scale = _Scale.create_empty_scale(output_scale.value.value_base)
    else:
        i_scale = _Scale.create_empty_scale(1)

    o_scale: _Scale = output_scale.value if output_scale is not None else _Scale.create_empty_scale(i_scale.value_base)

    scale_multiplier: float
    if i_scale.value_base == o_scale.value_base:
        scale_multiplier = math.pow(i_scale.value_base, i_scale.value_exp - o_scale.value_exp)
    elif i_scale.value_exp == o_scale.value_exp:
        scale_multiplier = math.pow(i_scale.value_base / o_scale.value_base, i_scale.value_exp)
    else:
        scale_multiplier = i_scale.value / o_scale.value

    return input_ * scale_multiplier

def to_metric(base_value: float, unit_prefix: MetricPrefix | BinaryPrefix, unit: str | None = None, with_space: bool = True, decimals: int = 0) -> str:
    scale: _Scale = unit_prefix.value
    return _to_metric(base_value, scale.value, scale.name, unit, with_space, decimals)

def to_short_metric(base_value: float, unit_prefix: MetricPrefix | BinaryPrefix, unit: str | None = None, with_space: bool = True, decimals: int = 0) -> str:
    scale: _Scale = unit_prefix.value
    return _to_metric(base_value, scale.value, scale.symbol, unit, with_space, decimals)

def _to_metric(base_value: float, scale_value: int, scale_name: str, unit: str | None, with_space: bool, decimals: int) -> str:
    space: str = " " if with_space else ""
    value = math.round_away_from_zero_to_digits(base_value / scale_value, digits=decimals)

    unit_str: str
    if unit is None:
        unit_str = ""
    elif decimals == 0 and int(value) == 1:
        unit_str = unit
    else:
        unit_str = unit + "s"

    return f"{value:.{decimals}f}{space}{scale_name}{unit_str}"

def _pick_optimal_prefix(base_value: float, prefixes: Iterable[_PrefixT]) -> _PrefixT:
    prefix: _PrefixT | None = None
    for prefix in sorted(prefixes, key=lambda s: s.value, reverse=True):
        scale = prefix.value
        if (base_value / scale.value) >= 1.0:
            return prefix

    if prefix is None:
        raise ValueError("No scales provided.")
    return prefix
