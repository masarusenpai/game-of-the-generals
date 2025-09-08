from __future__ import annotations
import constants as cn
from abc import ABC, abstractmethod
from typing import Callable


PIECES: dict[str, Callable[[], Piece]] = {
    "FLAG"               : lambda: Flag(),
    "PRIVATE"            : lambda: Private(),
    "SERGEANT"           : lambda: Sergeant(),
    "2ND LIEUTENANT"     : lambda: SecondLieutenant(),
    "1ST LIEUTENANT"     : lambda: FirstLieutenant(),
    "CAPTAIN"            : lambda: Captain(),
    "MAJOR"              : lambda: Major(),
    "LIEUTENANT COLONEL" : lambda: LieutenantColonel(),
    "COLONEL"            : lambda: Colonel(),
    "BRIGADIER GENERAL"  : lambda: BrigadierGeneral(),
    "MAJOR GENERAL"      : lambda: MajorGeneral(),
    "LIEUTENANT GENERAL" : lambda: LieutenantGeneral(),
    "GENERAL"            : lambda: General(),
    "GENERAL OF THE ARMY": lambda: GeneralOfTheArmy(),
    "SPY"                : lambda: Spy()
}


class Move(ABC):
    @abstractmethod
    def execute(self, board: Board, x: int, y: int) -> int:
        pass


class MoveUp(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL

        if y >= cn.BOARD_LEN - 1:
            return cn.OUT_OF_BOUNDS

        block = board.get_at(x, y + 1)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE
        
        board.place(my_piece, x, y + 1)
        board.clear(x, y)
        return cn.SUCCESS


class MoveDown(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL

        if y <= 0:
            return cn.OUT_OF_BOUNDS

        block = board.get_at(x, y - 1)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE

        board.place(my_piece, x, y - 1)
        board.clear(x, y)
        return cn.SUCCESS


class MoveRight(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL

        if x >= cn.BOARD_WID - 1:
            return cn.OUT_OF_BOUNDS

        block = board.get_at(x + 1, y)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE

        board.place(my_piece, x + 1, y)
        board.clear(x, y)
        return cn.SUCCESS


class MoveLeft(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL

        if x <= 0:
            return cn.OUT_OF_BOUNDS

        block = board.get_at(x - 1, y)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE

        board.place(my_piece, x - 1, y)
        board.clear(x, y)
        return cn.SUCCESS


class Board:
    def __init__(self) -> None:
        self.list_repr: list[list[Piece | None]] = []
        self._initialise_board()

    def _initialise_board(self) -> None:
        for y in range(cn.BOARD_LEN):
            self.list_repr.append([])
            curr_row = self.list_repr[y]

            for _ in range(cn.BOARD_WID):
                curr_row.append(None)

    def print_board(self) -> None:
        print("-" * (cn.PRINT_LEN(cn.BOARD_WID)))

        for y in range(cn.BOARD_LEN - 1, -1, -1):
            for x in range(cn.BOARD_WID):
                curr_pc = self.list_repr[y][x]
                print(f"| {'  ' if curr_pc is None else curr_pc} ", end="")

            print("|")
            print("-" * (cn.PRINT_LEN(cn.BOARD_WID)))

    def get_at(self, x: int, y: int) -> Piece | None:
        try:
            return self.list_repr[y][x]
        except IndexError:
            return None

    def place(self, piece: Piece, x: int, y: int) -> None:
        # TODO: attack sequence
        self.list_repr[y][x] = piece
        piece.set_pos(x, y)

    def clear(self, x: int, y: int) -> None:
        self.list_repr[y][x] = None

    # TODO: Delete if not needed
    def get_adjacent_cells(self, piece: Piece) -> dict[str, Piece | None]:
        x, y = piece.get_pos()
        adjacent: dict[str, Piece | None] = {
            "up"   : self.get_at(x, y + 1),
            "down" : self.get_at(x, y - 1),
            "left" : self.get_at(x - 1, y),
            "right": self.get_at(x + 1, y)
        }
        return adjacent


class Piece:
    def __init__(self, rank: int) -> None:
        self.rank = rank
        self._x_pos = -1
        self._y_pos = -1
        self.symb = cn.RANK_TO_SYMBOL.get(self.rank)
        self.opp = False

    def get_pos(self) -> tuple[int, int]:
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

    def name(self) -> str:
        return list(PIECES)[self.rank]

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
