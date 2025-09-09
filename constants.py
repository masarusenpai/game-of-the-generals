from typing import Callable


SUCCESS       = 0
EMPTY_CELL    = 1
OUT_OF_BOUNDS = 2
FRIENDLY_FIRE = 3

MOVE_MADE  = 0
OPP_ELIM   = 1
USR_ELIM   = 2
SPLIT      = 3
USR_WINNER = -OPP_ELIM
OPP_WINNER = -USR_ELIM

PRINT_LEN: Callable[[int], int] = lambda d: d * 6 - 8
BOARD_LEN = 8
BOARD_WID = 9

RANK_TO_SYMBOL: dict[int, str] = {
    0 : "🏳️",
    1 : "🪖",
    2 : "🔼",
    3 : "🔺",
    4 : "🔻",
    5 : "⚓",
    6 : "☀️",
    7 : "✴️",
    8 : "🔰",
    9 : "🌟",
    10: "💫",
    11: "✨",
    12: "⚔️",
    13: "👑",
    14: "👀"
}
