"""
Module containing formatting-related constants and functions.

Requires the `termcolor` module to work (see README.md).
"""
from typing import Callable
from termcolor import colored


BOLD: Callable[[str], str] = lambda target: colored(target, attrs=["bold"])
BLINK: Callable[[str], str] = lambda target: colored(target, attrs=["blink"])


def to_banner(title: str) -> str:
    """
    Returns a formatted string `title` as a banner.
    """
    left_side = colored("===", "blue")
    star =  colored(" ★ ", "yellow")
    right_side = colored("===", "red")
    return BOLD(left_side + star + title + star + right_side)


def marker_formatting(mark: str, colour: str) -> str:
    """
    Returns a formatted string `mark` as a console marker with colour `colour`.
    """
    return colored(f"[{mark}]", colour, attrs=["bold"])
