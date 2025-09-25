"""
Module responsible for running the game.
"""
import os
from random import choice, randrange
from time import sleep
from gog.components.board import Board
from gog.components.operation import MOVES
from gog.components.piece import Flag, Piece, PIECES
from gog.config import constants as con
from gog.config.style import marker_formatting, to_banner, BLINK, BOLD


remaining_pieces: dict[str, int]
opp_pieces: list[Piece] = []

clear = ""
console = ""
marker = ""
in_game = False
final_state = 0
board = Board()


def set_piece_dict() -> None:
    """
    Initialises a global dictionary of pieces mapping from piece name to the amount of pieces which
    must be placed on the board.
    """
    global remaining_pieces
    remaining_pieces = {
        "FLAG": 1, "PRIVATE": 6, "SERGEANT": 1, "2ND LIEUTENANT": 1, "1ST LIEUTENANT": 1,
        "CAPTAIN": 1, "MAJOR": 1, "LIEUTENANT COLONEL": 1, "COLONEL": 1, "BRIGADIER GENERAL": 1,
        "MAJOR GENERAL": 1, "LIEUTENANT GENERAL": 1, "GENERAL": 1, "GENERAL OF THE ARMY": 1,
        "SPY": 2
    }


def clear_game() -> None:
    """
    Clear (mostly) all game-related variables (`Board` object, list of opponent pieces, final
    state).
    """
    global board, final_state
    board = Board()
    opp_pieces.clear()
    final_state = 0
    set_piece_dict()


def set_console_status(status="GAME", colour="white") -> None:
    """
    Sets status (marker) of the console to `status` with colour `colour`. By default, console status
    is set to '`[GAME]`' (in white).
    """
    global marker
    marker = marker_formatting(status, colour)


def set_console(message="") -> None:
    """
    Display `message` to game console along with the status. By default, console message is set to
    blank.
    """
    global console
    if message:
        console = f"{marker} {message}"
    else:
        console = ""


def set_game_status(status: bool) -> None:
    """
    Set `status` of game which indicates whether user is in a game or not.
    """
    global in_game
    in_game = status


def set_final_state(code: int) -> None:
    """
    Set the state of the game with `code`, indicating whether an endgame has been reached (a flag
    has reached the end of the board).
    """
    global final_state
    final_state = code


def reveal_opp_pieces() -> None:
    """
    Reveal all oponent pieces at the end of a game with `Piece.reveal()`.
    """
    for piece in opp_pieces:
        piece.reveal()


def board_and_console() -> None:
    """
    Print to `stdout` the console and the board with a formatted banner displaying the game title.
    """
    print()
    print(console)
    print()
    print((" " * 7) + to_banner("GAME OF THE GENERALS"))
    print()
    board.print_board()
    print()


def display_rules() -> None:
    """
    Print the rules of the game to `stdout`. Content is copied and pasted from README.md.
    """
    os.system(clear)
    print("\n\n")
    print((" " * 14) + to_banner("RULES"))
    print()

    with open("../resources/rules.txt", "r", encoding="utf-8") as fd:
        for line in fd.readlines():
            print(line, end="")

    input(f"\nPress {BOLD('[ENTER]')} to return to main menu.")


def display_legend() -> None:
    """
    Print to `stdout` the legend of emojis representing pieces.
    """
    os.system(clear)
    print("\n\n")
    print((" " * 14) + to_banner("LEGEND"))
    print()
    print("EMOJI                                    PIECE")
    print("=" * con.PRINT_LEN(con.BOARD_WID))
    for i, piece in enumerate(list(PIECES)):
        print(f"{con.SYMBOLS[i]}{piece.rjust(con.PRINT_LEN(con.BOARD_WID) - 2)}")

    if in_game:
        input_message = f"\nPress {BOLD('[ENTER]')} to return to game."
    else:
        input_message = f"\nPress {BOLD('[ENTER]')} to return to main menu."
    input(input_message)


def print_commands() -> None:
    """
    Print main menu commands to `stdout`.
    """
    print("COMMAND                               FUNCTION")
    print("=" * con.PRINT_LEN(con.BOARD_WID))
    print("(PLAY/P)                            Start game")
    print("(RULES/R)                           View rules")
    print("(LEGEND/L)                   View emoji legend")
    print("(EXIT/E)                                  Exit")
    print("(CTRL+C / CTRL+D)                   Force exit\n")


def print_pre_game_commands() -> None:
    """
    Print pre-game commands to `stdout` (while user is placing pieces).
    """
    print("OTHER SUPPORTED COMMANDS")
    print("=" * con.PRINT_LEN(con.BOARD_WID))
    print("(PIECE/P)                  View unadded pieces")
    print("(UNDO/U)                                  Undo")
    print("(EXIT/E)                                  Exit")
    print("(CTRL+C / CTRL+D)                   Force exit")
    print("(!)            Randomise pieces (if you dare!)\n")


def print_in_game_commands() -> None:
    """
    Print support in-game commands to `stdout`.
    """
    print("OTHER SUPPORTED COMMANDS")
    print("=" * con.PRINT_LEN(con.BOARD_WID))
    print("(WHICH <POS>)      View name of piece at <POS>")
    print("(LEGEND/L)                   View emoji legend")
    print("(FORFEIT)                     Forfeit the game")
    print("(CTRL+C / CTRL+D)                   Force exit\n")


def empty_box() -> bool:
    """
    Return whether there are leftover pieces to be placed or not.
    """
    return all(n_pieces == 0 for n_pieces in list(remaining_pieces.values()))


def parse_coords(raw_inp: str) -> tuple[int, int] | tuple[None, None]:
    """
    Parses `raw_input` for valid coordinates. Returns tuple of 0-indexed coordinates if successful
    and tuple of `None` values if not.
    """
    inp = raw_inp.lower()
    if len(inp) != 2:
        return None, None
    x = ord(inp[0]) - con.ORD_OFFSET
    if x < 0 or x > 8 or not inp[1].isnumeric():
        return None, None
    y = int(inp[1])

    if y < 1 or y > 8:
        return None, None
    return x, y - 1


def indices_to_coords(x: int, y: int) -> str:
    """
    Convert zero-based indices `x` and `y` for accessing the list representation of the board into
    valid, command-formatted coordinates.
    """
    return f"{chr(x + con.CHR_OFFSET)}{y + 1}"


def show_piece_box() -> None:
    """
    Display all remaining unplaced pieces and their quantities to `stdout`.
    """
    os.system(clear)
    print("\n\n")
    print((" " * 9) + to_banner("REMAINING PIECES"))
    print()

    for i, (piece, no) in enumerate(remaining_pieces.items()):
        if i == len(remaining_pieces) - 1:
            keyword = ""
        else:
            keyword = f" ({list(con.KEYWORD_MAPPER)[i * 2 + 1]})"

        if no:
            print(f"{(piece + keyword).ljust(con.PRINT_LEN(con.BOARD_WID) - 2)}{no}")

    print("\nHint: You may use abbreviations when placing pieces (e.g. CPT H2)!")
    input(f"\nPress {BOLD('[ENTER]')} to return to game.")


def verify_user_action(action: str) -> bool:
    """
    Verify the `action` of a user. Returns `True` if user inputs 'yes' (case insensitive).
    """
    set_console()
    os.system(clear)
    board_and_console()
    print(f"Are you sure you wish to {action}?")
    print(f"Enter {BOLD('YES')} to confirm your choice or anything else to reject it.")
    return input(BLINK("> ")).lower() == "yes"


def randomise_piece_placement(opp=True) -> None:
    """
    Sets all remaining pieces at random. If `opp` is set to `False`, piece placement is randomised
    in the user's side of the board.
    """
    if opp:
        set_piece_dict()

    for piece in list(remaining_pieces):
        y_lower_bound = 5 if opp else 0
        y_upper_bound = 8 if opp else 3
        n_pieces = remaining_pieces.get(piece)

        for _ in range(n_pieces):
            piece_obj = PIECES.get(piece).generate_piece()
            if opp:
                piece_obj.set_opp()
                opp_pieces.append(piece_obj)
            x, y = randrange(9), randrange(y_lower_bound, y_upper_bound)
            while board.get_at(x, y) is not None:
                x, y = randrange(9), randrange(y_lower_bound, y_upper_bound)
            board.place(piece_obj, x, y)
            if isinstance(piece_obj, Flag):
                board.set_opp_flag(piece_obj)


def place_pieces() -> int:
    """
    Handles manual piece placement.
    """
    set_piece_dict()
    while not empty_box():
        os.system(clear)
        board_and_console()
        print("Add pieces to the board with the command <PIECE> <POSITION> (e.g. FLAG A3).")
        print("When all pieces are added, you will prompted to start the game.\n")
        print_pre_game_commands()
        cmd = input(BLINK("> "))

        match cmd.lower():
            case "piece" | "p":
                show_piece_box()
                continue
            case "undo" | "u":
                removed_piece = board.undo_place()
                if removed_piece is None:
                    set_console_status("ERROR", "red")
                    set_console("Nothing to undo.")
                else:
                    set_console_status()
                    set_console(f"Removed {removed_piece.name()}.")
                    remaining_pieces[removed_piece.name()] += 1
                continue
            case "!":
                if verify_user_action("randomise piece positions"):
                    set_console_status()
                    set_console("Randomising piece positions...")
                    os.system(clear)
                    board_and_console()
                    sleep(1)
                    randomise_piece_placement(opp=False)
                    set_console()
                    break
                continue
            case "exit" | "e":
                if verify_user_action("exit"):
                    set_console_status()
                    set_console("Exiting to main menu...")
                    os.system(clear)
                    board_and_console()
                    clear_game()
                    set_console()
                    sleep(1)
                    return 1
                continue

        cmd_tokens = cmd.split()
        if len(cmd_tokens) < 2:
            set_console_status("ERROR", "red")
            set_console(f"Invalid command '{cmd}'.")
            continue

        piece_input = " ".join(cmd_tokens[:-1])
        piece_name = con.KEYWORD_MAPPER.get(piece_input.upper())
        if piece_name is None:
            set_console_status("ERROR", "red")
            set_console(f"No such piece '{piece_input}' exists.")
            continue
        if not remaining_pieces.get(piece_name):
            set_console_status("ERROR", "red")
            set_console(f"All pieces of {piece_name} have already been placed.")
            continue

        pos_input = cmd_tokens[-1]
        x, y = parse_coords(pos_input)
        if (x is None and y is None) or y > 2:
            set_console_status("ERROR", "red")
            set_console(f"Invalid or forbidden position '{pos_input}'.")
            continue

        pos = pos_input.upper()
        if board.get_at(x, y) is not None:
            set_console_status("ERROR", "red")
            set_console(f"{pos} occupied by {board.get_at(x, y).name()}.")
            continue

        set_console_status()
        piece = PIECES.get(piece_name).generate_piece()
        remaining_pieces[piece_name] -= 1
        set_console(f"{piece_name} placed at position {pos}!")
        board.place(piece, x, y)

    os.system(clear)
    board_and_console()
    input(f"All pieces have been placed! Press {BOLD('[ENTER]')} to begin the game.")
    return 0


def handle_turn(result: int) -> None:
    """
    Handles console messages / game status based on `result` code.
    """
    set_console_status()
    match result:
        case con.USR_END | con.OPP_END:
            set_final_state(result)
            set_console("It's your turn!")
            return 0
        case con.USR_AUTO_WIN:
            set_final_state(con.USR_END)
        case con.OPP_AUTO_WIN:
            set_final_state(con.OPP_END)

    if result != con.MOVE_MADE and result < con.USR_END: # i.e. if a challenge has occurred
        fallen = board.get_last_killed()

        set_console("CHALLENGE! Examining outcome...")
        board.challenge()
        os.system(clear)
        board_and_console()
        sleep(2)
        board.challenge(restore=True)

        match result:
            case con.OPP_ELIM:
                set_console(f"You ate the opponent's {fallen.name()} {fallen.symb}!")
            case con.USR_ELIM:
                set_console(f"The opponent ate your {fallen.name()} {fallen.symb}!")
            case con.SPLIT:
                set_console("Split! Both your pieces have been eliminated (same rank).")
            case con.USR_WINNER:
                set_console_status("VICTORY", "green")
                set_console("You ate the opponent's FLAG 🏴 and won!")
            case con.OPP_WINNER:
                set_console_status("GAME OVER", "red")
                set_console("The opponent captured your FLAG 🏳️.")

        if result < 0: # i.e. if result == con.USR_WINNER or result == con.OPP_WINNER
            reveal_opp_pieces()
            os.system(clear)
            board_and_console()
            input(f"Press {BOLD('[ENTER]')} to return to main menu.")
            return 1

        os.system(clear)
        board_and_console()
        sleep(2)

    match final_state:
        case con.USR_END:
            set_console_status("VICTORY", "green")
            set_console("Your FLAG 🏳️ successfully reached the end of the board!")
        case con.OPP_END:
            set_console_status("GAME OVER", "red")
            set_console("The opponent's FLAG 🏴 successfully reached the end of the board!")

    if final_state: # i.e. if final_state matches any of the above cases
        reveal_opp_pieces()
        os.system(clear)
        board_and_console()
        input(f"Press {BOLD('[ENTER]')} to return to main menu.")
        return 1

    set_console("It's your turn!")
    return 0


def handle_game() -> None:
    """
    Handles the actual game mechanics between user and simulation (using `random.randrange`).
    """
    if place_pieces():
        set_game_status(False)
        return

    os.system(clear)
    set_console_status("OPP")
    set_console("Arranging pieces...")
    board_and_console()
    sleep(1)

    randomise_piece_placement()
    set_console_status()
    set_console("It's your turn!")

    while True:
        os.system(clear)
        board_and_console()
        print("To move pieces, use the command <POS> <OPERATION> (e.g. A3 UP).\n")
        print_in_game_commands()
        cmd = input(BLINK("> "))

        match cmd.lower():
            case "legend" | "l":
                display_legend()
                continue
            case "forfeit":
                if verify_user_action("forfeit"):
                    set_console_status()
                    set_console("Game forfeited. Exiting to main menu...")
                    reveal_opp_pieces()
                    os.system(clear)
                    board_and_console()
                    sleep(2)
                    break
                set_console("It's your turn!")
                continue

        cmd_tokens = cmd.split()
        if len(cmd_tokens) != 2:
            set_console_status("ERROR", "red")
            set_console(f"Invalid command '{cmd}'.")
            continue

        if cmd_tokens[0].lower() == 'which':
            x, y = parse_coords(cmd_tokens[1])
            if x is None and y is None:
                set_console_status("ERROR", "red")
                set_console(f"Invalid position '{cmd_tokens[1]}'.")
                continue

            selected_piece = board.get_at(x, y)
            if selected_piece is None:
                set_console_status("ERROR", "red")
                set_console("Blank position selected.")
                continue

            set_console_status()
            if selected_piece.opp:
                set_console(f"Piece at {cmd_tokens[1].upper()}: UNKNOWN ❔ (enemy piece selected)")
            else:
                set_console(
                    f"Piece at {cmd_tokens[1].upper()}: {selected_piece.name()} {selected_piece}"
                )
            continue

        x, y = parse_coords(cmd_tokens[0])
        if x is None and y is None:
            set_console_status("ERROR", "red")
            set_console(f"Invalid position '{cmd_tokens[0]}'.")
            continue
        operation = MOVES.get(cmd_tokens[1].lower())
        if operation is None:
            set_console_status("ERROR", "red")
            set_console(f"Invalid operation '{cmd_tokens[1]}'.")
            continue

        if board.get_at(x, y) is not None and board.get_at(x, y).opp:
            set_console_status("ERROR", "red")
            set_console("Enemy piece selected.")
            continue

        status, result = operation.generate_move().execute(board, x, y)
        if status != con.SUCCESS:
            set_console_status("ERROR", "red")
            match status:
                case con.EMPTY_CELL:
                    set_console("Empty cell selected.")
                case con.OUT_OF_BOUNDS:
                    set_console("Out-of-bounds move.")
                case con.FRIENDLY_FIRE:
                    set_console("Move blocked by a friendly piece.")
            continue

        if handle_turn(result):
            break

        set_console_status("OPP")
        set_console("Calculating move...")
        os.system(clear)
        board_and_console()
        sleep(2)

        if board.clear_path_to_end():
            flag_x, flag_y = board.get_opp_flag().get_pos()
            flag_res = MOVES.get("down").generate_move().execute(board, flag_x, flag_y)[1]
            if handle_turn(flag_res):
                break
            continue

        challenger_pieces = [
            challenger for challenger in opp_pieces
            if challenger.active and board.can_be_challenged(challenger)
        ]

        opp_choice: Piece = None
        if challenger_pieces:
            # If at least one opponent piece has an adjacent challengeable piece, randomly
            # choose from those pieces to move
            opp_choice = choice(challenger_pieces)
        else:
            # Otherwise, select a piece from a list of moveable, active opponent pieces
            movable_opp_pieces = [
                opp_p for opp_p in opp_pieces
                if opp_p.active and not board.is_surrounded(opp_p)
            ]
            opp_choice = choice(movable_opp_pieces)

        opp_x, opp_y = opp_choice.get_pos()
        valid_moves = board.get_valid_moves(opp_choice)
        if "down" in valid_moves:
            valid_moves.append("down")
        chosen_move = choice(valid_moves)

        set_console(f"{indices_to_coords(opp_x, opp_y)} {chosen_move.upper()}")
        os.system(clear)
        board_and_console()
        sleep(2)

        opp_res = MOVES.get(chosen_move).generate_move().execute(board, opp_x, opp_y)[1]
        if handle_turn(opp_res):
            break

    clear_game()
    set_console()
    set_game_status(False)


def start() -> None:
    """
    Starts the actual game. Called in the entry point of the code.
    """
    while True:
        os.system(clear)
        board_and_console()
        print_commands()
        print("Please input a command.")
        cmd = input(BLINK("> "))
        set_console_status()
        set_console()

        match cmd.lower():
            case "play" | "p":
                set_game_status(True)
                handle_game()
            case "rules" | "r":
                display_rules()
            case "legend" | "l":
                display_legend()
            case "exit" | "e":
                set_console("Paalam (Goodbye)! 👋")
                os.system(clear)
                board_and_console()
                sleep(2)
                break
            case _:
                set_console_status("ERROR", "red")
                set_console(f"Unknown command '{cmd}'.")


if __name__ == "__main__":
    # Configure 'clear screen' command based on the OS of the user.
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
