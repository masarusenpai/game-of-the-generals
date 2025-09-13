from gog.components import constants as con
from gog.components.piece import Piece, Flag, challenge_icon


class Board:
    def __init__(self) -> None:
        self.list_repr: list[list[Piece | None]] = []
        self.graveyard: list[Piece] = []
        self.cache: list[tuple[int, int]] = []
        self.challenge_restore: list[Piece] = []
        self._initialise_board()

    def _initialise_board(self) -> None:
        for y in range(con.BOARD_LEN):
            self.list_repr.append([])
            curr_row = self.list_repr[y]

            for _ in range(con.BOARD_WID):
                curr_row.append(None)

    def print_board(self) -> None:
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
        try:
            return self.list_repr[y][x]
        except IndexError:
            wall = Piece(con.WALL)
            wall.set_opp()
            return wall

    def place(self, piece: Piece, x: int, y: int) -> int:
        code = con.MOVE_MADE
        src = piece
        dest = self.get_at(x, y)
        if dest is not None:
            src = piece.attack(dest)
            if src == piece:
                code = con.OPP_ELIM if not piece.opp else con.USR_ELIM
                self.graveyard.append(dest)
                dest.set_pos(-1, -1)
            elif src is None:
                code = con.SPLIT
                self.graveyard.append(dest)
                piece.set_pos(-1, -1)
                dest.set_pos(-1, -1)
            else:
                code = con.USR_ELIM if not piece.opp else con.OPP_ELIM
                self.graveyard.append(piece)
                piece.set_pos(-1, -1)

            if isinstance(self.graveyard[-1], Flag):
                code *= -1

        self.list_repr[y][x] = src
        self.cache.append((x, y))
        piece.set_pos(x, y)
        return code

    def clear(self, x: int, y: int) -> None:
        self.list_repr[y][x] = None

    def recently_killed(self) -> Piece | None:
        if not self.graveyard:
            return None # This should never happen!
        return self.graveyard[-1]

    def undo_place(self) -> Piece | None:
        if not self.cache:
            return None
        x, y = self.cache.pop()
        piece = self.get_at(x, y)
        self.clear(x, y)
        return piece

    def set_challenge(self) -> None:
        x, y = self.cache[-1]
        loc = self.get_at(x, y)
        if loc is not None:
            self.challenge_restore.append(loc)
        self.place(challenge_icon(), x, y)

    def restore_position(self) -> None:
        x, y = self.cache[-1]
        self.clear(x, y)
        if self.challenge_restore:
            self.place(self.challenge_restore.pop(), x, y)

    def is_surrounded(self, piece: Piece) -> bool:
        x, y = piece.get_pos()
        return self.get_at(x + 1, y) is not None and self.get_at(x + 1, y).opp \
               and self.get_at(x - 1, y) is not None and self.get_at(x - 1, y).opp \
               and self.get_at(x, y + 1) is not None and self.get_at(x, y + 1).opp \
               and self.get_at(x, y - 1) is not None and self.get_at(x, y - 1).opp
