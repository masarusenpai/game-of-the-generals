"""
Module containing the abstract class `Move`.

The `Move` class implements the factory method and command pattern.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from gog.components.board import Board
from gog.config import constants as con


class Move(ABC):
    """
    Abstract class representing a movement (up, down, left or right) in the game.
    """
    @abstractmethod
    def execute(self, board: Board, x: int, y: int) -> tuple[int, int]:
        """
        Execute movement on `board` on piece at position (`x`, `y`).
        """


class MoveUp(Move):
    """
    Class representing the 'up' movement. Inherits from the class `Move`.
    """
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return con.EMPTY_CELL, -1

        if y >= con.BOARD_LEN - 1:
            return con.OUT_OF_BOUNDS, -1

        block = board.get_at(x, y + 1)
        if block is not None and block.opp == my_piece.opp:
            return con.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return con.SUCCESS, board.place(my_piece, x, y + 1)


class MoveDown(Move):
    """
    Class representing the 'down' movement. Inherits from the class `Move`.
    """
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return con.EMPTY_CELL, -1

        if y <= 0:
            return con.OUT_OF_BOUNDS, -1

        block = board.get_at(x, y - 1)
        if block is not None and block.opp == my_piece.opp:
            return con.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return con.SUCCESS, board.place(my_piece, x, y - 1)


class MoveRight(Move):
    """
    Class representing the 'right' movement. Inherits from the class `Move`.
    """
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return con.EMPTY_CELL, -1

        if x >= con.BOARD_WID - 1:
            return con.OUT_OF_BOUNDS, -1

        block = board.get_at(x + 1, y)
        if block is not None and block.opp == my_piece.opp:
            return con.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return con.SUCCESS, board.place(my_piece, x + 1, y)


class MoveLeft(Move):
    """
    Class representing the 'left' movement. Inherits from the class `Move`.
    """
    def execute(self, board, x, y):
        my_piece = board.get_at(x, y)
        if my_piece is None:
            return con.EMPTY_CELL, -1

        if x <= 0:
            return con.OUT_OF_BOUNDS, -1

        block = board.get_at(x - 1, y)
        if block is not None and block.opp == my_piece.opp:
            return con.FRIENDLY_FIRE, -1

        board.clear(x, y)
        return con.SUCCESS, board.place(my_piece, x - 1, y)


class MoveFactory(ABC):
    """
    Generates instances of `Move` using the factory method.
    """
    @abstractmethod
    def generate_move(self) -> Move:
        """
        Generate an executable `Move` instance.
        """


class MoveUpFactory(MoveFactory):
    """
    Generates instances of `MoveUp`. Inherits from the class `MoveFactory`.
    """
    def generate_move(self):
        return MoveUp()


class MoveDownFactory(MoveFactory):
    """
    Generates instances of `MoveUp`. Inherits from the class `MoveFactory`.
    """
    def generate_move(self):
        return MoveDown()


class MoveRightFactory(MoveFactory):
    """
    Generates instances of `MoveUp`. Inherits from the class `MoveFactory`.
    """
    def generate_move(self):
        return MoveRight()


class MoveLeftFactory(MoveFactory):
    """
    Generates instances of `MoveUp`. Inherits from the class `MoveFactory`.
    """
    def generate_move(self):
        return MoveLeft()


MOVES: dict[str, MoveFactory] = {
    "up": MoveUpFactory(), "down": MoveDownFactory(),
    "left": MoveLeftFactory(), "right": MoveRightFactory()
}
