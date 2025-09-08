from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable


PIECES = [
    "FLAG",
    "PRIVATE",
    "SERGEANT",
    "2ND LIEUTENANT",
    "1ST LIEUTENANT",
    "CAPTAIN",
    "MAJOR",
    "LIEUTENANT COLONEL",
    "COLONEL",
    "BRIGADIER GENERAL",
    "MAJOR GENERAL",
    "LIEUTENANT GENERAL",
    "GENERAL",
    "GENERAL OF THE ARMY"
]


class Board:
    LEN = 8
    WID = 9
    PRINT_LEN: Callable[[int], int] = lambda d: d * 6 - 8

    def __init__(self) -> None:
        self.list_repr: list[list[Piece | None]] = []
        self._initialise_board()

    def _initialise_board(self) -> None:
        for y in range(self.LEN):
            self.list_repr.append([])
            curr_row = self.list_repr[y]

            for _ in range(self.WID):
                curr_row.append(None)

    def print_board(self) -> None:
        print("-" * (Board.PRINT_LEN(self.WID)))

        for y in range(self.LEN - 1, -1, -1):
            for x in range(self.WID):
                curr_pc = self.list_repr[y][x]
                print(f"| {'  ' if curr_pc is None else curr_pc} ", end="")

            print("|")
            print("-" * (Board.PRINT_LEN(self.WID)))

    def is_empty(self, x: int, y: int) -> bool:
        return self.list_repr[y][x] is None


class Piece(ABC):
    def __init__(self, rank: int, x_pos: int, y_pos: int, opp: bool) -> None:
        self.rank = rank
        self._x_pos = x_pos
        self._y_pos = y_pos
        self.opp = opp
        self.symb = self._rank_to_symb()

    def _rank_to_symb(self) -> str:
        match self.rank:
            case 0:
                return "🏳️"
            case 1:
                return "🪖"
            case 2:
                return "🔺"
            case 3:
                return "🔻"
            case 4:
                return "⚓"
            case 5:
                return "☀️"
            case 6:
                return "✴️"
            case 7:
                return "🔰"
            case 8:
                return "⭐"
            case 9:
                return "🌟"
            case 10:
                return "✨"
            case 11:
                return "💫"
            case 12:
                return "👑"
            case 13:
                return "👀"

    def get_x(self) -> int:
        return self._x_pos

    def get_y(self) -> int:
        return self._y_pos

    @abstractmethod
    def attack(self, target: Piece) -> Piece:
        pass
