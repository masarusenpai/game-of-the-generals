from typing import Callable


ORD_OFFSET = 97

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

KEYWORD_MAPPER: dict[str, str] = {
    "FLAG"               : "FLAG",
    "FLG"                : "FLAG",
    "PRIVATE"            : "PRIVATE",
    "PRV"                : "PRIVATE",
    "SERGEANT"           : "SERGEANT",
    "SGT"                : "SERGEANT",
    "2ND LIEUTENANT"     : "2ND LIEUTENANT",
    "2LT"                : "2ND LIEUTENANT",
    "1ST LIEUTENANT"     : "1ST LIEUTENANT",
    "1LT"                : "1ST LIEUTENANT",
    "CAPTAIN"            : "CAPTAIN",
    "CPT"                : "CAPTAIN",
    "MAJOR"              : "MAJOR",
    "MJR"                : "MAJOR",
    "LIEUTENANT COLONEL" : "LIEUTENANT COLONEL",
    "LTC"                : "LIEUTENANT COLONEL",
    "COLONEL"            : "COLONEL",
    "COL"                : "COLONEL",
    "BRIGADIER GENERAL"  : "BRIGADIER GENERAL",
    "BRG"                : "BRIGADIER GENERAL",
    "MAJOR GENERAL"      : "MAJOR GENERAL",
    "MJG"                : "MAJOR GENERAL",
    "LIEUTENANT GENERAL" : "LIEUTENANT GENERAL",
    "LTG"                : "LIEUTENANT GENERAL",
    "GENERAL"            : "GENERAL",
    "GNR"                : "GENERAL",
    "GENERAL OF THE ARMY": "GENERAL OF THE ARMY",
    "GOA"                : "GENERAL OF THE ARMY",
    "SPY"                : "SPY"
}
