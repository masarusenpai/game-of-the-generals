import constants as cn
from piece import Piece, Flag


class Board:
    def __init__(self) -> None:
        self.list_repr: list[list[Piece | None]] = []
        self.graveyard: list[Piece] = []
        self.cache: list[tuple[int, int]] = []
        self._initialise_board()

    def _initialise_board(self) -> None:
        for y in range(cn.BOARD_LEN):
            self.list_repr.append([])
            curr_row = self.list_repr[y]

            for _ in range(cn.BOARD_WID):
                curr_row.append(None)

    def print_board(self) -> None:
        print("    ", end="")
        for i in range(cn.BOARD_WID):
            print(f"{chr(i + 65)}    ", end="")

        print(f"\n  +{'-' * (cn.PRINT_LEN(cn.BOARD_WID) - 2)}+")
        for y in range(cn.BOARD_LEN - 1, -1, -1):
            print(f"{y + 1} ", end="")
            for x in range(cn.BOARD_WID):
                curr_pc = self.list_repr[y][x]
                print(f"| {'  ' if curr_pc is None else curr_pc} ", end="")
            print("|")

            if y:
                print(f"  {'-' * cn.PRINT_LEN(cn.BOARD_WID)}")
            else:
                print(f"  +{'-' * (cn.PRINT_LEN(cn.BOARD_WID) - 2)}+")

    def get_at(self, x: int, y: int) -> Piece | None:
        try:
            return self.list_repr[y][x]
        except IndexError:
            return None

    def place(self, piece: Piece, x: int, y: int) -> int:
        code = cn.MOVE_MADE

        src = piece
        dest = self.get_at(x, y)
        if dest is not None:
            src = piece.attack(dest)

            if src == piece:
                code = cn.OPP_ELIM
                self.graveyard.append(dest)
            elif src is None:
                code = cn.SPLIT
                self.graveyard.append(dest)
            else:
                code = cn.USR_ELIM
                self.graveyard.append(piece)

            if isinstance(dest, Flag):
                code *= -1

        self.list_repr[y][x] = src
        piece.set_pos(x, y)
        return code

    def clear(self, x: int, y: int) -> None:
        self.list_repr[y][x] = None
    
    def recently_killed(self) -> str:
        if not self.graveyard:
            return "" # This should never happen!
        fallen = self.graveyard[-1]
        return f"{fallen.name()} {cn.RANK_TO_SYMBOL.get(fallen.rank)}"

    def undo_place(self) -> None:
        if not self.cache:
            return
        x, y = self.cache.pop()
        self.clear(x, y)
