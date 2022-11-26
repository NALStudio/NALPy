from enum import IntEnum as _IntEnum
import re as _re
from nalpy.humanizer.numbers import number_to_words_converter as _number_to_words_converter
from nalpy.humanizer.numbers import heading_converter as _heading_converter

class NumberFormat(_IntEnum):
    NONE = 0
    NUMERALS = 1
    SPACED_NUMERALS = 2
    WORDS = 3


def format(num: int, _format: NumberFormat) -> str:
    if _format == NumberFormat.NONE:
        return ""
    if _format == NumberFormat.NUMERALS:
        return str(num)
    if _format == NumberFormat.SPACED_NUMERALS:
        reversed_str: str = "".join(reversed(str(num)))
        joined = ' '.join(_re.findall(r'.{1,3}', reversed_str))
        return "".join(reversed(joined))
    if _format == NumberFormat.WORDS:
        return to_words(num)
    raise ValueError()

def ordinalize(num: int, _format: NumberFormat = NumberFormat.NUMERALS) -> str:
    if num < 1:
        raise ValueError("Number cannot be less than one!")

    if _format == NumberFormat.WORDS:
        return to_ordinal_words(num)

    out: str = format(num, _format)
    last_digit: int = num % 10

    if last_digit == 1:
        return out + "st"
    if last_digit == 2:
        return out + "nd"
    if last_digit == 3:
        return out + "rd"
    return out + "th"

def to_words(num: int, add_and: bool = True) -> str:
    return _number_to_words_converter.convert(num, False, add_and)

def to_ordinal_words(num: int) -> str:
    return _number_to_words_converter.convert(num, True)

def to_percent(num: int | float, _format: NumberFormat = NumberFormat.NUMERALS) -> str:
    if isinstance(num, float):
        num = round(num * 100)

    if _format == NumberFormat.SPACED_NUMERALS:
        return f"{format(num, _format)} %"
    if _format == NumberFormat.WORDS:
        return f"{to_words(num)} percent"
    return f"{format(num, _format)}%"

# def to_metric(num: int) -> str:
#     raise NotImplementedError()

def to_heading(degrees: float) -> str:
    return _heading_converter.get_heading_from_set(degrees, _heading_converter.HEADINGS_LONG)

def to_abbreviated_heading(degrees: float) -> str:
    return _heading_converter.get_heading_from_set(degrees, _heading_converter.HEADINGS_SHORT)

def to_heading_arrow(degrees: float) -> str:
    return _heading_converter.get_heading_from_set(degrees, _heading_converter.HEADINGS_ARROW)

def tupleize(count: int) -> str:
    match count:
        case 1:
            return "single"
        case 2:
            return "double"
        case 3:
            return "triple"
        case 4:
            return "quadruple"
        case 5:
            return "quintuple"
        case 6:
            return "sextuple"
        case 7:
            return "septuple"
        case 8:
            return "octuple"
        case 9:
            return "nonuple"
        case 10:
            return "decuple"
        case 100:
            return "centuple"
        case 1000:
            return "milluple"
        case _:
            return f"{count}-tuple"
