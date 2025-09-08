from __future__ import annotations
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
    "GENERAL OF THE ARMY",
    "SPY"
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
    
    def place(self, piece: Piece, x: int, y: int) -> None:
        self.list_repr[y][x] = piece


class Piece:
    def __init__(self, rank: int) -> None:
        self.rank = rank
        self._x_pos: int | None = None
        self._y_pos: int | None = None
        self.symb = rank_to_symbol(self.rank)
        self.opp = False

    def get_pos(self) -> tuple[int, int | None, None]:
        return self._x_pos, self._y_pos

    def set_pos(self, x: int, y: int) -> None:
        self._x_pos = x
        self._y_pos = y

    def set_opp(self) -> None:
        self.opp = True

    def kill(self) -> None:
        self.symb = ""

    def attack(self, target: Piece) -> Piece | None:
        if self.rank == target.rank:
            self.kill()
            target.kill()
            return None

        if self.rank > target.rank:
            target.kill()
            return self

        self.kill()
        return target

    def __str__(self) -> str:
        return self.symb if not self.opp else "🔘"


class Flag(Piece):
    def __init__(self):
        super().__init__(0)

    def attack(self, target):
        if self.rank == target.rank:
            target.kill()
            return self

        self.kill()
        return target


class Private(Piece):
    def __init__(self):
        super().__init__(1)
    
    def attack(self, target):
        if isinstance(target, Spy):
            target.kill()
            return self

        if self.rank == target.rank:
            self.kill()
            target.kill()
            return None

        self.kill()
        return target


class Sergeant(Piece):
    def __init__(self):
        super().__init__(2)


class SecondLieutenant(Piece):
    def __init__(self):
        super().__init__(3)


class FirstLieutenant(Piece):
    def __init__(self):
        super().__init__(4)


class Captain(Piece):
    def __init__(self):
        super().__init__(5)


class Major(Piece):
    def __init__(self):
        super().__init__(6)


class LieutenantColonel(Piece):
    def __init__(self):
        super().__init__(7)


class Colonel(Piece):
    def __init__(self):
        super().__init__(8)


class BrigadierGeneral(Piece):
    def __init__(self):
        super().__init__(9)


class MajorGeneral(Piece):
    def __init__(self):
        super().__init__(10)


class LieutenantGeneral(Piece):
    def __init__(self):
        super().__init__(11)


class General(Piece):
    def __init__(self):
        super().__init__(12)


class GeneralOfTheArmy(Piece):
    def __init__(self):
        super().__init__(13)


class Spy(Piece):
    def __init__(self):
        super().__init__(14)
    
    def attack(self, target):
        if isinstance(target, Private):
            self.kill()
            return target

        if self.rank == target.rank:
            self.kill()
            target.kill()
            return None

        target.kill()
        return self


def rank_to_symbol(rank: int) -> str:
        match rank:
            case 0:
                return "🏳️"
            case 1:
                return "🪖"
            case 2:
                return "🔼"
            case 3:
                return "🔺"
            case 4:
                return "🔻"
            case 5:
                return "⚓"
            case 6:
                return "☀️"
            case 7:
                return "✴️"
            case 8:
                return "🔰"
            case 9:
                return "🌟"
            case 10:
                return "🌠"
            case 11:
                return "✨"
            case 12:
                return "💫"
            case 13:
                return "👑"
            case 14:
                return "👀"


def display_legend() -> None:
    print("=== LEGEND ===")
    for i, piece in enumerate(PIECES):
        print(f"{rank_to_symbol(i)} -> {piece}")


display_legend()