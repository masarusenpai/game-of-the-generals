import os
from random import randrange
from time import sleep
from gog.components.board import Board
from gog.components.operation import MOVES
from gog.components.piece import PIECES, Piece, Flag
from gog.config import constants as con
from gog.config.style import BOLD, BLINK, to_banner, marker_formatting


remaining_pieces: dict[str, int]
opp_pieces: list[Piece] = []

clear = ""
console = ""
marker = ""
in_game = False
final_state = 0
board = Board()
flag_index = -1


def set_piece_dict() -> None:
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


def set_console_status(status="GAME", colour="white") -> None:
    global marker
    marker = marker_formatting(status, colour)


def set_console(message="") -> None:
    """
    Display `message` to game console. By default, console message is set to blank.
    """
    global console
    if message:
        console = f"{marker} {message}"
    else:
        console = ""


def set_game_status(status: bool) -> None:
    global in_game
    in_game = status


def set_final_state(code: int) -> None:
    global final_state
    final_state = code


def dead_opp(opp: Piece) -> bool:
    x, y = opp.get_pos()
    return x < 0 and y < 0


def reveal_opp_pieces() -> None:
    for piece in opp_pieces:
        piece.reveal()


def board_and_console() -> None:
    print()
    print(console)
    print()
    print((" " * 7) + to_banner("GAME OF THE GENERALS"))
    print()
    board.print_board()
    print()


def display_rules() -> None:
    os.system(clear)
    print("\n\n")
    print((" " * 14) + to_banner("RULES"))
    print()

    with open("../resources/rules.txt", "r") as fd:
        for line in fd.readlines():
            print(line, end="")

    if in_game:
        input_message = f"\nPress {BOLD('[ENTER]')} to return to game."
    else:
        input_message = f"\nPress {BOLD('[ENTER]')} to return to main menu."
    input(input_message)


def display_legend() -> None:
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
    print("COMMAND                               FUNCTION")
    print("=" * con.PRINT_LEN(con.BOARD_WID))
    print("(PLAY/P)                            Start game")
    print("(RULES/R)                           View rules")
    print("(LEGEND/L)                   View emoji legend")
    print("(EXIT/E)                                  Exit")
    print("(CTRL+C / CTRL+D)                   Force exit\n")


def print_pre_game_commands() -> None:
    print("OTHER SUPPORTED COMMANDS")
    print("=" * con.PRINT_LEN(con.BOARD_WID))
    print("(PIECE/P)                  View unadded pieces")
    print("(UNDO/U)                                  Undo")
    print("(EXIT/E)                                  Exit")
    print("(CTRL+C / CTRL+D)                   Force exit")
    print("(!)            Randomise pieces (if you dare!)\n")


def print_in_game_commands() -> None:
    print("OTHER SUPPORTED COMMANDS")
    print("=" * con.PRINT_LEN(con.BOARD_WID))
    print("(WHICH <POS>)      View name of piece at <POS>")
    print("(RULES/R)                           View rules")
    print("(FORFEIT)                     Forfeit the game")
    print("(CTRL+C / CTRL+D)                   Force exit\n")


def empty_box() -> bool:
    for no in list(remaining_pieces.values()):
        if no:
            return False
    return True


def parse_coords(raw_inp: str) -> tuple[int, int] | tuple[None, None]:
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


def show_piece_box() -> None:
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
    set_console()
    os.system(clear)
    board_and_console()
    print(f"Are you sure you wish to {action}?")
    print(f"Enter {BOLD('YES')} to confirm your choice or anything else to reject it.")
    return input(BLINK("> ")).lower() == "yes"


def set_opponent_pieces(opp=True) -> None:
    for piece in list(PIECES):
        y_lower_bound = 5 if opp else 0
        y_upper_bound = 8 if opp else 3
        n_pieces = 1

        match piece:
            case "PRIVATE":
                n_pieces = 6
            case "SPY":
                n_pieces = 2

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
                    clear_game()
                    sleep(1)
                    set_opponent_pieces(opp=False)
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
                    opp_pieces.clear()
                    set_console()
                    sleep(1)
                    return -1
                continue

        cmds = cmd.split()
        if len(cmds) < 2:
            set_console_status("ERROR", "red")
            set_console("Invalid command.")
            continue

        piece_input = " ".join(cmds[:-1])
        piece_name = con.KEYWORD_MAPPER.get(piece_input.upper())
        if piece_name is None:
            set_console_status("ERROR", "red")
            set_console(f"No such piece '{piece_input}' exists.")
            continue
        if not remaining_pieces.get(piece_name):
            set_console_status("ERROR", "red")
            set_console(f"All pieces of {piece_name} have already been placed.")
            continue

        pos_input = cmds[-1]
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
    input("All pieces have been placed! Press 'ENTER' to begin the game.")
    return 0


def handle_turn(result: int) -> None:
    set_console_status()

    if result != con.MOVE_MADE:
        if result == con.USR_END or result == con.OPP_END:
            set_final_state(result)
            set_console("It's your turn!")
            return 0

        fallen = board.recently_killed()
        rank = fallen.rank
        set_console("CHALLENGE! Examining outcome...")
        board.challenge()
        os.system(clear)
        board_and_console()
        sleep(1)
        board.challenge(restore=True)

        match result:
            case con.OPP_ELIM:
                set_console(f"You ate the opponent's {fallen.name()} {con.SYMBOLS[rank]}!")
            case con.USR_ELIM:
                set_console(f"The opponent ate your {fallen.name()} {con.SYMBOLS[rank]}!")
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
            input("Press 'ENTER' to return to main menu.")
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
        case _:
            set_console("It's your turn!")
            return 0

    reveal_opp_pieces()
    os.system(clear)
    board_and_console()
    input("Press 'ENTER' to return to main menu.")
    return 1


def handle_game() -> None:
    if place_pieces():
        set_game_status(False)
        return

    os.system(clear)
    set_console_status()
    set_console("Your opponent (simulation) is placing its pieces...")
    board_and_console()
    sleep(1)

    set_opponent_pieces()
    set_console("It's your turn!")

    while True:
        os.system(clear)
        board_and_console()
        print("To move pieces, use the command <POS> <OPERATION> (e.g. A3 UP).\n")
        print_in_game_commands()
        cmd = input(BLINK("> "))

        match cmd.lower():
            case "rules" | "r":
                display_rules()
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

        cmds = cmd.split()
        if len(cmds) != 2:
            set_console_status("ERROR", "red")
            set_console(f"Error: invalid command '{cmd}'.")
            continue

        if cmds[0].lower() == 'which':
            x, y = parse_coords(cmds[1])
            if x is None and y is None:
                set_console_status("ERROR", "red")
                set_console(f"Error: invalid position '{cmds[1]}'.")
                continue

            selected_piece = board.get_at(x, y)
            if selected_piece is None:
                set_console_status("ERROR", "red")
                set_console("Error: blank position selected.")
                continue

            set_console_status()
            if selected_piece.opp:
                set_console(f"Piece at {cmds[1].upper()}: UNKNOWN (enemy piece selected)")
            else:
                set_console(f"Piece at {cmds[1].upper()}: {selected_piece.name()} {selected_piece}")
            continue

        x, y = parse_coords(cmds[0])
        if x is None and y is None:
            set_console_status("ERROR", "red")
            set_console(f"Error: invalid position '{cmds[0]}'.")
            continue
        operation = MOVES.get(cmds[1].lower())
        if operation is None:
            set_console_status("ERROR", "red")
            set_console(f"Error: invalid operation '{cmds[1]}'.")
            continue

        if board.get_at(x, y) is not None and board.get_at(x, y).opp:
            set_console_status("ERROR", "red")
            set_console("Error: enemy piece selected.")
            continue

        status, result = operation.generate_move().execute(board, x, y)
        if status != con.SUCCESS:
            set_console_status("ERROR", "red")
            match status:
                case con.EMPTY_CELL:
                    set_console("Error: empty cell selected.")
                case con.OUT_OF_BOUNDS:
                    set_console("Error: out-of-bounds move.")
                case con.FRIENDLY_FIRE:
                    set_console("Error: move blocked by a friendly piece.")
            continue

        if handle_turn(result):
            break

        set_console_status()
        set_console("It's the opponent's turn. Calculating move...")
        os.system(clear)
        board_and_console()
        sleep(2)

        # TODO: move opponent flag forward if there is clear path from flag to end, make opponent
        # immediately randomly eat adjacent user piece
        if board.clear_path_to_end():
            flag_x, flag_y = board.opp_flag.get_pos()
            res = MOVES.get("down").generate_move().execute(board, flag_x, flag_y)[1]
            handle_turn(res)
            continue

        # Repeatedly choose random piece until valid movable piece is chosen
        opp_choice = opp_pieces[randrange(len(opp_pieces))]
        opp_x, opp_y = opp_choice.get_pos()
        while (dead_opp(opp_choice)
                or board.is_surrounded(opp_choice)
                or not opp_choice.opp):
            opp_choice = opp_pieces[randrange(len(opp_pieces))]
            opp_x, opp_y = opp_choice.get_pos()

        # Repeatedly choose random move until valid move is chosen
        move_obj = MOVES.get(list(MOVES)[randrange(4)]).generate_move()
        opp_status, opp_res = move_obj.execute(board, opp_x, opp_y)
        while opp_status != con.SUCCESS:
            move_obj = MOVES.get(list(MOVES)[randrange(4)]).generate_move()
            opp_status, opp_res = move_obj.execute(board, opp_x, opp_y)

        if handle_turn(opp_res):
            break

    clear_game()
    set_console()
    set_game_status(False)


def start() -> None:
    while True:
        os.system(clear)
        board_and_console()
        print_commands()
        print(f"Please input a command.")
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
                set_console(f"'{cmd}': invalid command.")


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
