import os
import constants as cn
from time import sleep
from piece import PIECES, MOVES, Board


clear = ""
console = ""
in_game = False
board = Board()


def set_console(message="") -> None:
    global console
    console = message


def board_and_console() -> None:
    print()
    print(console)
    print()
    print("=== ⭐ GAME OF THE GENERALS ⭐ ===".center(cn.PRINT_LEN(cn.BOARD_WID)))
    print()
    board.print_board()
    print()


# TODO
def display_rules() -> None:
    os.system(clear)
    print("\n\n")
    print("=== ⭐ RULES ⭐ ===\n".center(cn.PRINT_LEN(cn.BOARD_WID)))
    print("Rules coming soon...")
    input("\nPress 'ENTER' to return to main menu.")


def display_legend() -> None:
    os.system(clear)
    print("\n\n")
    print("=== ⭐ LEGEND ⭐ ===\n".center(cn.PRINT_LEN(cn.BOARD_WID)))
    print("EMOJI                                    PIECE")
    print("=" * cn.PRINT_LEN(cn.BOARD_WID))
    for i, piece in enumerate(list(PIECES)):
        print(f"{cn.RANK_TO_SYMBOL.get(i)}{piece.rjust(cn.PRINT_LEN(cn.BOARD_WID) - 2)}")

    if in_game:
        input_message = "\nPress 'ENTER' to return to game."
    else:
        input_message = "\nPress 'ENTER' to return to main menu."

    input(input_message)


def print_commands() -> None:
    print("COMMAND                               FUNCTION")
    print("=" * cn.PRINT_LEN(cn.BOARD_WID))
    print("(PLAY/P)                            Start game")
    print("(RULES/R)                           View rules")
    print("(LEGEND/L)                   View emoji legend")
    print("(EXIT/E)                                  Exit")
    print("(CTRL+C / CTRL+D)                   Force exit\n")


def letter_to_coord(letter: str) -> int:
    return ord(letter) - cn.ORD_OFFSET


# TODO
def handle_game() -> None:
    pass


# TODO
def start() -> None:
    global in_game
    end_loop = False

    os.system(clear)
    while True:
        board_and_console()

        if end_loop:
            sleep(1)
            break

        print_commands()
        print("Please input a command.")
        cmd = input("> ").lower()
        set_console()

        match cmd:
            case "play" | "p":
                in_game = True
                handle_game()
            case "rules" | "r":
                display_rules()
            case "legend" | "l":
                display_legend()
            case "exit" | "e":
                set_console("Paalam (Goodbye)! 👋")
                end_loop = True
            case _:
                set_console(f"'{cmd}': invalid command.")

        os.system(clear)


if __name__ == "__main__":
    if os.name == "posix":
        clear = "clear"
    else:
        clear = "cls"

    try:
        start()
    except (KeyboardInterrupt, EOFError):
        os.system(clear)
        print("\nForce exiting...")
        sleep(2)
    finally:
        os.system(clear)
