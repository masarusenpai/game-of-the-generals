"""
Module containing the `Board` class.
"""
from gog.components.piece import Piece, Flag, challenge_icon, Private
from gog.config import constants as con


class Board:
    """
    Class representing the game board.
    """
    def __init__(self) -> None:
        self.list_repr: list[list[Piece | None]] = []
        self.graveyard: list[Piece] = []
        self.cache: list[tuple[int, int]] = []
        self.challenge_restore: list[Piece] = []
        self.opp_flag: Flag = None

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
                self.graveyard.append(dest)
            elif src is None:
                code = con.SPLIT
                self.graveyard.append(piece if piece.opp else dest)
            else:
                code = con.USR_ELIM if not piece.opp else con.OPP_ELIM
                self.graveyard.append(piece)

            if isinstance(self.graveyard[-1], Flag):
                code *= -1

        self.list_repr[y][x] = src
        self.cache.append((x, y))
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

    def recently_killed(self) -> Piece | None:
        """
        Returns the most recently killed `Piece` object. Technically returns `None` if no pieces
        have been killed yet, but this should not happen in-game.
        """
        if not self.graveyard:
            return None # This should never happen!
        return self.graveyard[-1]

    def undo_place(self) -> Piece | None:
        """
        Remove the last `Piece` object placed on the board and return it. If there's nothing to
        undo, return `None`.
        """
        if not self.cache:
            return None
        x, y = self.cache.pop()
        piece = self.get_at(x, y)
        self.clear(x, y)
        return piece

    def challenge(self, restore=False) -> None:
        """
        Set a challenge icon at the position where the last elimination occurred. After the
        'challenge' animation sequence, when `restore` is set to `True`, return the original piece
        to its original position.
        """
        x, y = self.cache[-1]
        if restore:
            x, y = self.cache[-1]
            self.clear(x, y)
            if self.challenge_restore:
                self.place(self.challenge_restore.pop(), x, y)
        else:
            loc = self.get_at(x, y)
            if loc is not None:
                self.challenge_restore.append(loc)
            self.place(challenge_icon(), x, y)

    def is_surrounded(self, piece: Piece) -> bool:
        """
        Returns whether an opponent piece is surrounded by other opponent pieces (or walls, which
        have `self.op = True` by default).
        """
        x, y = piece.get_pos()
        adjacent = [
            self.get_at(x + 1, y), self.get_at(x - 1, y),
            self.get_at(x, y + 1), self.get_at(x, y - 1)
        ]
        return all(adj_piece is not None and adj_piece.opp for adj_piece in adjacent)

    def can_be_challenged(self, piece: Piece) -> list[str]:
        """
        Indicates whether a piece can be challenged by an adjacent opposing piece.
        """
        x, y = piece.get_pos()
        adjacent = {
            "right": self.get_at(x + 1, y),
            "left": self.get_at(x - 1, y),
            "up": self.get_at(x, y + 1),
            "down": self.get_at(x, y - 1)
        }
        killer_moves: list[str] = []

        for adj_piece in list(adjacent):
            curr_piece = adjacent.get(adj_piece)
            if (curr_piece is not None
                    and curr_piece.opp != piece.opp
                    and curr_piece.rank != con.WALL):
                killer_moves.append(adj_piece)
        
        return killer_moves
    
    def set_opp_flag(self, flag: Flag) -> None:
        self.opp_flag = flag

    def clear_path_to_end(self) -> bool:
        x, y = self.opp_flag.get_pos()
        return all(self.get_at(x, all_y) is None for all_y in range(y))
