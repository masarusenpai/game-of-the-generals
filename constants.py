from typing import Callable


SUCCESS = 0
EMPTY_CELL = 1
OUT_OF_BOUNDS = 2
FRIENDLY_FIRE = 3

PRINT_LEN: Callable[[int], int] = lambda d: d * 6 - 8
BOARD_LEN = 8
BOARD_WID = 9

RANK_TO_SYMBOL: dict[int, str] = {
    0: "🏳️",
    1: "🪖",
    2: "🔼",
    3: "🔺",
    4: "🔻",
    5: "⚓",
    6: "☀️",
    7: "✴️",
    8: "🔰",
    9: "🌟",
    10: "💫",
    11: "✨",
    12: "⚔️",
    13: "👑",
    14: "👀"
}
