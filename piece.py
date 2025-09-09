from __future__ import annotations
from typing import Callable
import constants as cn


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


class Piece:
    def __init__(self, rank: int) -> None:
        self.rank = rank
        self._x_pos = -1
        self._y_pos = -1
        self.symb: str = cn.RANK_TO_SYMBOL.get(self.rank)
        self.opp = False

    def get_pos(self) -> tuple[int, int]:
        return self._x_pos, self._y_pos

    def set_pos(self, x: int, y: int) -> None:
        self._x_pos = x
        self._y_pos = y

    def set_opp(self) -> None:
        self.opp = True

    def attack(self, target: Piece) -> Piece | None:
        if self.rank == target.rank:
            return None
        if self.rank > target.rank:
            return self
        return target

    def name(self) -> str:
        return list(PIECES)[self.rank]

    def __str__(self) -> str:
        return self.symb if not self.opp else "❔"


class Flag(Piece):
    def __init__(self):
        super().__init__(0)

    def attack(self, target):
        return self if self.rank == target.rank else target


class Private(Piece):
    def __init__(self):
        super().__init__(1)

    def attack(self, target):
        if isinstance(target, Spy):
            return self
        if self.rank == target.rank:
            return None
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
            return target
        if self.rank == target.rank:
            return None
        return self
