from __future__ import annotations
from abc import ABC, abstractmethod
import constants as cn


class Piece:
    def __init__(self, rank: int) -> None:
        self.rank = rank
        self._x_pos = -1
        self._y_pos = -1
        self.symb = cn.SYMBOLS[self.rank]
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


class PieceFactory(ABC):
    @abstractmethod
    def generate_piece(self) -> Piece:
        pass


class FlagFactory(PieceFactory):
    def generate_piece(self):
        return Flag()


class PrivateFactory(PieceFactory):
    def generate_piece(self):
        return Private()


class SergeantFactory(PieceFactory):
    def generate_piece(self):
        return Sergeant()


class SecondLieutenantFactory(PieceFactory):
    def generate_piece(self):
        return SecondLieutenant()


class FirstLieutenantFactory(PieceFactory):
    def generate_piece(self):
        return FirstLieutenant()


class CaptainFactory(PieceFactory):
    def generate_piece(self):
        return Captain()


class MajorFactory(PieceFactory):
    def generate_piece(self):
        return Major()


class LieutenantColonelFactory(PieceFactory):
    def generate_piece(self):
        return LieutenantColonel()


class ColonelFactory(PieceFactory):
    def generate_piece(self):
        return Colonel()


class BrigadierGeneralFactory(PieceFactory):
    def generate_piece(self):
        return BrigadierGeneral()


class MajorGeneralFactory(PieceFactory):
    def generate_piece(self):
        return MajorGeneral()


class LieutenantGeneralFactory(PieceFactory):
    def generate_piece(self):
        return LieutenantGeneral()


class GeneralFactory(PieceFactory):
    def generate_piece(self):
        return General()


class GeneralOfTheArmyFactory(PieceFactory):
    def generate_piece(self):
        return GeneralOfTheArmy()


class SpyFactory(PieceFactory):
    def generate_piece(self):
        return Spy()
    

def challenge_icon() -> Piece:
    return Piece(cn.CHALLENGE)


PIECES: dict[str, PieceFactory] = {
    "FLAG": FlagFactory(), "PRIVATE": PrivateFactory(), "SERGEANT": SergeantFactory(),
    "2ND LIEUTENANT": SecondLieutenantFactory(), "1ST LIEUTENANT": FirstLieutenantFactory(),
    "CAPTAIN": CaptainFactory(), "MAJOR": MajorFactory(),
    "LIEUTENANT COLONEL": LieutenantColonelFactory(), "COLONEL": ColonelFactory(),
    "BRIGADIER GENERAL": BrigadierGeneralFactory(), "MAJOR GENERAL": MajorGeneralFactory(),
    "LIEUTENANT GENERAL": LieutenantGeneralFactory(), "GENERAL": GeneralFactory(),
    "GENERAL OF THE ARMY": GeneralOfTheArmyFactory(), "SPY": SpyFactory()
}
