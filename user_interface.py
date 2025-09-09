import os
import constants as cn
from time import sleep
from typing import Callable
from piece import PIECES, MOVES, Board


clear: str


def display_legend() -> None:
    print("=== LEGEND ===")
    for i, piece in enumerate(list(PIECES)):
        print(f"{cn.RANK_TO_SYMBOL.get(i)} -> {piece}")


# TODO
def start() -> None:
    os.system(clear)
    print("\n")
    while True:
        inp = input("> ").lower()
        os.system(clear)

        if not inp:
            print("User inputted nothing.\n")
        else:
            print(f"User inputted: '{inp}'\n")


if __name__ == "__main__":
    if os.name == "posix":
        clear = "clear"
    else:
        clear = "cls"

    try:
        start()
    except (KeyboardInterrupt, EOFError):
        os.system(clear)
        print("\nCTRL+C/D detected. Exiting...")
        sleep(2)
        os.system(clear)
