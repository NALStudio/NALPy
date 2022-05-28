from enum import IntEnum as _IntEnum

class ConsoleColor(_IntEnum):
    BLACK = 0
    DARK_RED = 1
    DARK_GREEN = 2
    DARK_YELLOW = 3
    DARK_BLUE = 4
    DARK_MAGENTA = 5
    DARK_CYAN = 6
    GRAY = 7

    DARK_GRAY = 10
    RED = 11
    GREEN = 12
    YELLOW = 13
    BLUE = 14
    MAGENTA = 15
    CYAN = 16
    WHITE = 17

class ConsoleStyle(_IntEnum):
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    STRIKE = 9


# Module imports
from nalpy.console_utils import progressbar as progressbar
from nalpy.console_utils import spinner as spinner

# Styling imports
from nalpy.console_utils.styling import set_foreground_color as set_foreground_color
from nalpy.console_utils.styling import set_background_color as set_background_color
from nalpy.console_utils.styling import set_style as set_style
from nalpy.console_utils.styling import reset_attributes as reset_attributes

# Command imports
from nalpy.console_utils.commands import bell as bell
from nalpy.console_utils.commands import backspace as backspace
from nalpy.console_utils.commands import tab as tab
from nalpy.console_utils.commands import line_feed as line_feed
from nalpy.console_utils.commands import form_feed as form_feed
from nalpy.console_utils.commands import carriage_return as carriage_return

# Cursor imports
from nalpy.console_utils.cursor import cursor_up as cursor_up
from nalpy.console_utils.cursor import cursor_down as cursor_down
from nalpy.console_utils.cursor import cursor_forward as cursor_forward
from nalpy.console_utils.cursor import cursor_back as cursor_back
from nalpy.console_utils.cursor import cursor_line_down as cursor_line_down
from nalpy.console_utils.cursor import cursor_line_up as cursor_line_up
from nalpy.console_utils.cursor import cursor_set_column as cursor_set_column
from nalpy.console_utils.cursor import cursor_set_pos as cursor_set_pos
from nalpy.console_utils.cursor import cursor_hide as cursor_hide
from nalpy.console_utils.cursor import cursor_show as cursor_show
from nalpy.console_utils.cursor import clear as clear
from nalpy.console_utils.cursor import lclear as lclear
from nalpy.console_utils.cursor import rclear as rclear
from nalpy.console_utils.cursor import erase as erase
from nalpy.console_utils.cursor import lerase as lerase
from nalpy.console_utils.cursor import rerase as rerase
from nalpy.console_utils.cursor import scroll_up as scroll_up
from nalpy.console_utils.cursor import scroll_down as scroll_down
from nalpy.console_utils.cursor import cursor_get_pos as cursor_get_pos
