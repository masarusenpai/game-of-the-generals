from termcolor import colored
from typing import Callable


BOLD: Callable[[str], str] = lambda target: colored(target, attrs=["bold"])
BLINK: Callable[[str], str] = lambda target: colored(target, attrs=["blink"])


def to_banner(title: str) -> str:
    left_side = colored("===", "blue")
    star =  colored(" ★ ", "yellow")
    right_side = colored("===", "red")
    return BOLD(left_side + star + title + star + right_side)


def marker_formatting(mark: str, colour: str) -> str:
    return colored(f"[{mark}]", colour, attrs=["bold"])
