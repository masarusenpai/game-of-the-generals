"""
Module containing the abstract class `Piece`.

The `Piece` class implements the factory method and the composite pattern.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from gog.config import constants as con


class Piece:
    """
    Abstract class representing a piece on the board.
    """
    def __init__(self, rank: int) -> None:
        self.rank = rank
        self._x_pos = -1
        self._y_pos = -1
        self.symb = con.SYMBOLS[self.rank]
        self.opp = False

    def get_pos(self) -> tuple[int, int]:
        """
        Returns the position of the piece as a tuple.
        """
        return self._x_pos, self._y_pos

    def set_pos(self, x: int, y: int) -> None:
        """
        Sets the position of the piece as (`x`, `y`).
        """
        self._x_pos = x
        self._y_pos = y

    def set_opp(self) -> None:
        """
        Sets the piece as an opposing piece.
        """
        self.opp = True

    def reveal(self) -> None:
        """
        Reveals the identity of the piece if it is an opposing piece.
        """
        self.opp = False

    def attack(self, target: Piece) -> Piece | None:
        """
        Handles the attacking logic when the piece challenges `target`.
        """
        if self.rank == target.rank:
            return None
        if self.rank > target.rank:
            return self
        return target

    def name(self) -> str:
        """
        Returns the actual name of the piece (as opposed to `__str__`, which returns the emoji
        representing the piece.)
        """
        return list(PIECES)[self.rank]

    def __str__(self) -> str:
        return self.symb if not self.opp else "❔"


class Flag(Piece):
    """
    Class representing the flag piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(0)

    def set_opp(self):
        self.opp = True
        self.symb = "🏴"

    def attack(self, target):
        return self if self.rank == target.rank else target


class Private(Piece):
    """
    Class representing the private piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(1)

    def attack(self, target):
        if isinstance(target, (Flag, Spy)):
            return self
        if self.rank == target.rank:
            return None
        return target


class Sergeant(Piece):
    """
    Class representing the sergeant piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(2)


class SecondLieutenant(Piece):
    """
    Class representing the second lieutenant piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(3)


class FirstLieutenant(Piece):
    """
    Class representing the first lieutenant piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(4)


class Captain(Piece):
    """
    Class representing the captain piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(5)


class Major(Piece):
    """
    Class representing the major piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(6)


class LieutenantColonel(Piece):
    """
    Class representing the lieutenant colonel piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(7)


class Colonel(Piece):
    """
    Class representing the colonel piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(8)


class BrigadierGeneral(Piece):
    """
    Class representing the brigadier general piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(9)


class MajorGeneral(Piece):
    """
    Class representing the major general piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(10)


class LieutenantGeneral(Piece):
    """
    Class representing the lieutenant general piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(11)


class General(Piece):
    """
    Class representing the general piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(12)


class GeneralOfTheArmy(Piece):
    """
    Class representing the general of the army piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(13)


class Spy(Piece):
    """
    Class representing the spy piece. Inherits from the class `Piece`.
    """
    def __init__(self):
        super().__init__(14)

    def attack(self, target):
        if isinstance(target, Private):
            return target
        if self.rank == target.rank:
            return None
        return self


class PieceFactory(ABC):
    """
    Generates instances of `Piece` using the factory method.
    """
    @abstractmethod
    def generate_piece(self) -> Piece:
        """
        Generate a `Piece` instance.
        """


class FlagFactory(PieceFactory):
    """
    Generates instances of `Flag`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return Flag()


class PrivateFactory(PieceFactory):
    """
    Generates instances of `Private`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return Private()


class SergeantFactory(PieceFactory):
    """
    Generates instances of `Sergeant`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return Sergeant()


class SecondLieutenantFactory(PieceFactory):
    """
    Generates instances of `SecondLieutenant`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return SecondLieutenant()


class FirstLieutenantFactory(PieceFactory):
    """
    Generates instances of `FirstLieutenant`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return FirstLieutenant()


class CaptainFactory(PieceFactory):
    """
    Generates instances of `Captain`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return Captain()


class MajorFactory(PieceFactory):
    """
    Generates instances of `Major`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return Major()


class LieutenantColonelFactory(PieceFactory):
    """
    Generates instances of `LieutenantColonel`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return LieutenantColonel()


class ColonelFactory(PieceFactory):
    """
    Generates instances of `Colonel`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return Colonel()


class BrigadierGeneralFactory(PieceFactory):
    """
    Generates instances of `BrigadierGeneral`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return BrigadierGeneral()


class MajorGeneralFactory(PieceFactory):
    """
    Generates instances of `MajorGeneral`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return MajorGeneral()


class LieutenantGeneralFactory(PieceFactory):
    """
    Generates instances of `LieutenantGeneral`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return LieutenantGeneral()


class GeneralFactory(PieceFactory):
    """
    Generates instances of `General`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return General()


class GeneralOfTheArmyFactory(PieceFactory):
    """
    Generates instances of `GeneralOfTheArmy`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return GeneralOfTheArmy()


class SpyFactory(PieceFactory):
    """
    Generates instances of `Spy`. Inherits from the class `PieceFactory`.
    """
    def generate_piece(self):
        return Spy()


def challenge_icon() -> Piece:
    """
    Generate a special piece indicating an occuring challenge.
    """
    return Piece(con.CHALLENGE)


PIECES: dict[str, PieceFactory] = {
    "FLAG": FlagFactory(), "PRIVATE": PrivateFactory(), "SERGEANT": SergeantFactory(),
    "2ND LIEUTENANT": SecondLieutenantFactory(), "1ST LIEUTENANT": FirstLieutenantFactory(),
    "CAPTAIN": CaptainFactory(), "MAJOR": MajorFactory(),
    "LIEUTENANT COLONEL": LieutenantColonelFactory(), "COLONEL": ColonelFactory(),
    "BRIGADIER GENERAL": BrigadierGeneralFactory(), "MAJOR GENERAL": MajorGeneralFactory(),
    "LIEUTENANT GENERAL": LieutenantGeneralFactory(), "GENERAL": GeneralFactory(),
    "GENERAL OF THE ARMY": GeneralOfTheArmyFactory(), "SPY": SpyFactory()
}
