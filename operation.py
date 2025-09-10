from __future__ import annotations
from abc import ABC, abstractmethod
from board import Board
import constants as cn


class Move(ABC):
    @abstractmethod
    def execute(self, board: Board, x: int, y: int) -> tuple[int, int]:
        """
        Execute movement on `board` on piece at position (`x`, `y`).
        """
        pass


class MoveUp(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL, -1

        if y >= cn.BOARD_LEN - 1:
            return cn.OUT_OF_BOUNDS, -1

        block = board.get_at(x, y + 1)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return cn.SUCCESS, board.place(my_piece, x, y + 1)


class MoveDown(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL, -1

        if y <= 0:
            return cn.OUT_OF_BOUNDS, -1

        block = board.get_at(x, y - 1)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return cn.SUCCESS, board.place(my_piece, x, y - 1)


class MoveRight(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL, -1

        if x >= cn.BOARD_WID - 1:
            return cn.OUT_OF_BOUNDS, -1

        block = board.get_at(x + 1, y)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return cn.SUCCESS, board.place(my_piece, x + 1, y)


class MoveLeft(Move):
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return cn.EMPTY_CELL, -1

        if x <= 0:
            return cn.OUT_OF_BOUNDS, -1

        block = board.get_at(x - 1, y)
        if block is not None and block.opp == my_piece.opp:
            return cn.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return cn.SUCCESS, board.place(my_piece, x - 1, y)


class MoveFactory(ABC):
    @abstractmethod
    def generate_move(self) -> Move:
        pass


class MoveUpFactory(MoveFactory):
    def generate_move(self):
        return MoveUp()


class MoveDownFactory(MoveFactory):
    def generate_move(self):
        return MoveDown()


class MoveRightFactory(MoveFactory):
    def generate_move(self):
        return MoveRight()


class MoveLeftFactory(MoveFactory):
    def generate_move(self):
        return MoveLeft()


MOVES: dict[str, MoveFactory] = {
    "up": MoveUpFactory(), "down": MoveDownFactory(),
    "left": MoveLeftFactory(), "right": MoveRightFactory()
}
