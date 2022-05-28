from __future__ import annotations
from typing import Sequence


HEADINGS_LONG = ( "north", "north-northeast", "northeast", "east-northeast", "east", "east-southeast", "southeast", "south-southeast", "south", "south-southwest", "southwest", "west-southwest", "west", "west-northwest", "northwest", "north-northwest" )
HEADINGS_SHORT = ( "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW" )
HEADINGS_ARROW = ( '↑', '↗', '→', '↘', '↓', '↙', '←', '↖' )

def get_heading_from_set(heading: float, collection: Sequence[str]):
    ln = len(collection)
    val = round(heading / (360 / ln))
    return collection[val % ln]
