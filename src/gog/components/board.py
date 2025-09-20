"""
Module containing the `Board` class.
"""
from gog.components.piece import Piece, Flag, challenge_icon
from gog.config import constants as con


class Board:
    """
    Class representing the game board.
    """
    def __init__(self) -> None:
        self.list_repr: list[list[Piece | None]] = []
        self.__cache: list[tuple[int, int]] = []
        self.__challenge_cache: Piece = None
        self.__opp_flag: Flag = None
        self.__last_killed: Piece = None

        for y in range(con.BOARD_LEN):
            self.list_repr.append([])
            curr_row = self.list_repr[y]
            for _ in range(con.BOARD_WID):
                curr_row.append(None)

    def print_board(self) -> None:
        """
        Print the game board to `stdout`.
        """
        print("    ", end="")
        for i in range(con.BOARD_WID):
            print(f"{chr(i + 65)}    ", end="")

        print(f"\n  +{'-' * (con.PRINT_LEN(con.BOARD_WID) - 2)}+")
        for y in range(con.BOARD_LEN - 1, -1, -1):
            print(f"{y + 1} ", end="")
            for x in range(con.BOARD_WID):
                curr_pc = self.list_repr[y][x]
                print(f"| {'  ' if curr_pc is None else curr_pc} ", end="")
            print("|")

            if y:
                print(f"  {'-' * con.PRINT_LEN(con.BOARD_WID)}")
            else:
                print(f"  +{'-' * (con.PRINT_LEN(con.BOARD_WID) - 2)}+")

    def get_at(self, x: int, y: int) -> Piece | None:
        """
        Get the `Piece` object on the board at position (`x`, `y`). Returns `None` if position is
        empty or a 'wall' if position is out-of-bounds.
        """
        try:
            return self.list_repr[y][x]
        except IndexError:
            wall = Piece(con.WALL)
            wall.set_opp()
            return wall

    def place(self, piece: Piece, x: int, y: int) -> int:
        """
        Place a `Piece` object at position (`x`, `y`). Returns a status code indicating the current
        game status. Also manages the bulk of game elimination logic.
        """
        code = con.MOVE_MADE
        src = piece
        dest = self.get_at(x, y)
        if dest is not None:
            src = piece.attack(dest)
            if src == piece:
                code = con.OPP_ELIM if not piece.opp else con.USR_ELIM
                self.__last_killed = dest
            elif src is None:
                code = con.SPLIT
                self.__last_killed = piece if piece.opp else dest
            else:
                code = con.USR_ELIM if not piece.opp else con.OPP_ELIM
                self.__last_killed = piece

            if isinstance(self.__last_killed, Flag):
                code *= -1

        self.list_repr[y][x] = src
        self.__cache.append((x, y))
        piece.set_pos(x, y)

        if code == con.MOVE_MADE and isinstance(piece, Flag):
            if y == con.BOARD_LEN - 1 and not piece.opp:
                code = con.USR_END if self.can_be_challenged(piece) else con.USR_AUTO_WIN
            elif not y and piece.opp:
                code = con.OPP_END if self.can_be_challenged(piece) else con.OPP_AUTO_WIN

        return code

    def clear(self, x: int, y: int) -> None:
        """
        Clear position (`x`, `y`) on the board.
        """
        self.list_repr[y][x] = None

    def get_last_killed(self) -> Piece | None:
        """
        Returns the most recently killed `Piece` object. Technically returns `None` if no pieces
        have been killed yet, but this should not happen in-game.
        """
        return self.__last_killed

    def get_opp_flag(self) -> Flag:
        """
        Returns the `Flag` object representing the opposing flag.
        """
        return self.__opp_flag

    def undo_place(self) -> Piece | None:
        """
        Remove the last `Piece` object placed on the board and return it. If there's nothing to
        undo, return `None`.
        """
        if not self.__cache:
            return None
        x, y = self.__cache.pop()
        piece = self.get_at(x, y)
        self.clear(x, y)
        return piece

    def challenge(self, restore=False) -> None:
        """
        Set a challenge icon at the position where the last elimination occurred. After the
        'challenge' animation sequence, when `restore` is set to `True`, return the original piece
        to its original position.
        """
        x, y = self.__cache[-1]
        if restore:
            x, y = self.__cache[-1]
            self.clear(x, y)
            if self.__challenge_cache is not None:
                self.place(self.__challenge_cache, x, y)
                self.__challenge_cache = None
        else:
            loc = self.get_at(x, y)
            if loc is not None:
                self.clear(x, y)
                self.__challenge_cache = loc
            self.place(challenge_icon(), x, y)

    def __get_adjacent(self, piece: Piece) -> dict[str, Piece | None]:
        x, y = piece.get_pos()
        return {
            "right": self.get_at(x + 1, y),
            "left": self.get_at(x - 1, y),
            "up": self.get_at(x, y + 1),
            "down": self.get_at(x, y - 1)
        }

    def is_surrounded(self, piece: Piece) -> bool:
        """
        Returns whether an opponent piece is surrounded by other opponent pieces (or walls, which
        have `self.opp = True` by default).
        """
        adjacent = list(self.__get_adjacent(piece).values())
        return all(adj_piece is not None and adj_piece.opp for adj_piece in adjacent)

    def can_be_challenged(self, piece: Piece) -> bool:
        """
        Indicates whether a piece can be challenged by an adjacent opposing piece.
        """
        adjacent = list(self.__get_adjacent(piece).values())
        return not all(
            adj_piece is None or adj_piece.opp == piece.opp or adj_piece.rank == con.WALL
            for adj_piece in adjacent
        )

    def get_valid_moves(self, piece: Piece) -> list[str]:
        """
        Returns a list of valid moves `piece` may make.

        May not work as intended, so this must be used in conjunction with the error handling
        present in `run.py`.
        """
        adjacent = self.__get_adjacent(piece)
        return [
            move for move in list(adjacent)
            if adjacent.get(move) is None
                or (not adjacent.get(move).opp and adjacent.get(move).rank != con.WALL)
        ]

    def set_opp_flag(self, flag: Flag) -> None:
        """
        Sets `self.flag` to `flag` as an indicator for the opposing flag.
        """
        self.__opp_flag = flag

    def clear_path_to_end(self) -> bool:
        """
        Indicates whether there is a clear straight path from the opposing flag to the end of the
        board.
        """
        x, y = self.__opp_flag.get_pos()
        return all(self.get_at(x, all_y) is None for all_y in range(y))
