import os
from random import randrange
from time import sleep
from components.board import Board
from components.operation import MOVES
from components.piece import PIECES, Piece
import constants as cn


remaining_pieces: dict[str, int]
opp_pieces: list[Piece] = []

clear = ""
console = ""
in_game = False
board = Board()


def append_opp_pieces(piece: Piece) -> None:
    global opp_pieces
    opp_pieces.append(piece)


def reveal_opp_pieces() -> None:
    global opp_pieces
    for piece in opp_pieces:
        piece.reveal()


def clear_opp_pieces() -> None:
    global opp_pieces
    opp_pieces.clear()


def set_piece_dict() -> None:
    global remaining_pieces
    remaining_pieces = {
        "FLAG": 1, "PRIVATE": 6, "SERGEANT": 1, "2ND LIEUTENANT": 1, "1ST LIEUTENANT": 1,
        "CAPTAIN": 1, "MAJOR": 1, "LIEUTENANT COLONEL": 1, "COLONEL": 1, "BRIGADIER GENERAL": 1,
        "MAJOR GENERAL": 1, "LIEUTENANT GENERAL": 1, "GENERAL": 1, "GENERAL OF THE ARMY": 1,
        "SPY": 2
    }


def clear_board() -> None:
    """
    Simply clear the `Board` object (at the end of the game usually).
    """
    global board
    board = Board()


def set_console(message="") -> None:
    """
    Display `message` to game console. By default, console message is set to blank.
    """
    global console
    console = message


def set_game_status(status: bool) -> None:
    global in_game
    in_game = status


def board_and_console() -> None:
    print()
    print(console)
    print()
    print("=== ⭐ GAME OF THE GENERALS ⭐ ===".center(cn.PRINT_LEN(cn.BOARD_WID)))
    print()
    board.print_board()
    print()


def display_rules() -> None:
    os.system(clear)
    print("\n\n")
    print("=== ⭐ RULES ⭐ ===\n".center(cn.PRINT_LEN(cn.BOARD_WID)))
    print("Rules coming soon...") # TODO: rules

    if in_game:
        input_message = "\nPress 'ENTER' to return to game."
    else:
        input_message = "\nPress 'ENTER' to return to main menu."
    input(input_message)


def display_legend() -> None:
    os.system(clear)
    print("\n\n")
    print("=== ⭐ LEGEND ⭐ ===\n".center(cn.PRINT_LEN(cn.BOARD_WID)))
    print("EMOJI                                    PIECE")
    print("=" * cn.PRINT_LEN(cn.BOARD_WID))
    for i, piece in enumerate(list(PIECES)):
        print(f"{cn.SYMBOLS[i]}{piece.rjust(cn.PRINT_LEN(cn.BOARD_WID) - 2)}")

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


def print_pre_game_commands() -> None:
    print("OTHER SUPPORTED COMMANDS")
    print("=" * cn.PRINT_LEN(cn.BOARD_WID))
    print("(PIECE/P)                  View unadded pieces")
    print("(UNDO/U)                                  Undo")
    print("(EXIT/E)                                  Exit")
    print("(CTRL+C / CTRL+D)                   Force exit")
    print("(!)            Randomise pieces (if you dare!)\n")


def print_in_game_commands() -> None:
    print("OTHER SUPPORTED COMMANDS")
    print("=" * cn.PRINT_LEN(cn.BOARD_WID))
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
    x = ord(inp[0]) - cn.ORD_OFFSET
    if x < 0 or x > 8 or not inp[1].isnumeric():
        return None, None
    y = int(inp[1])

    if y < 1 or y > 8:
        return None, None
    return x, y - 1


def show_piece_box() -> None:
    os.system(clear)
    print("\n\n")
    print("=== ⭐ REMAINING PIECES ⭐ ===\n".center(cn.PRINT_LEN(cn.BOARD_WID)))

    for i, (piece, no) in enumerate(remaining_pieces.items()):
        if i == len(remaining_pieces) - 1:
            keyword = ""
        else:
            keyword = f" ({list(cn.KEYWORD_MAPPER)[i * 2 + 1]})"

        if no:
            print(f"{(piece + keyword).ljust(cn.PRINT_LEN(cn.BOARD_WID) - 2)}{no}")

    print("\nHint: You may use abbreviations when placing pieces (e.g. CPT H2)!")
    input("\nPress 'ENTER' to return to game.")


def verify_user_action(action: str) -> bool:
    set_console()
    os.system(clear)
    board_and_console()
    print(f"Are you sure you wish to {action}?")
    print("Enter 'YES' to confirm your choice or anything else to reject it.")
    return input("> ").lower() == "yes"


def set_opponent_pieces(opp=True) -> None:
    for piece in list(PIECES):
        y_lower_bound = 5 if opp else 0
        y_upper_bound = 8 if opp else 3
        n_pieces = 1

        match piece:
            case "FLAG":
                if opp:
                    y_lower_bound = 6
                else:
                    y_upper_bound = 2
            case "PRIVATE":
                n_pieces = 6
            case "SPY":
                n_pieces = 2

        piece_obj = PIECES.get(piece).generate_piece()
        if opp:
            piece_obj.set_opp()
            append_opp_pieces(piece_obj)

        for _ in range(n_pieces):
            x, y = randrange(9), randrange(y_lower_bound, y_upper_bound)
            while board.get_at(x, y) is not None:
                x, y = randrange(9), randrange(y_lower_bound, y_upper_bound)
            board.place(piece_obj, x, y)


def place_pieces() -> int:
    global remaining_pieces
    set_piece_dict()

    while not empty_box():
        os.system(clear)
        board_and_console()
        print("Add pieces to the board with the command <PIECE> <POSITION> (e.g. FLAG A3).")
        print("When all pieces are added, you will prompted to start the game.\n")
        print_pre_game_commands()
        cmd = input("> ")

        match cmd.lower():
            case "piece" | "p":
                show_piece_box()
                continue
            case "undo" | "u":
                removed_piece = board.undo_place()
                if removed_piece is None:
                    set_console("Error: nothing to undo.")
                else:
                    set_console(f"Undo: removed {removed_piece.name()}.")
                    remaining_pieces[removed_piece.name()] += 1
                continue
            case "!":
                if verify_user_action("randomise piece positions"):
                    set_console("Randomising piece positions...")
                    os.system(clear)
                    board_and_console()
                    clear_board()
                    sleep(1)
                    set_opponent_pieces(opp=False)
                    set_console()
                    break
                continue
            case "exit" | "e":
                if verify_user_action("exit"):
                    set_console("Exiting to main menu...")
                    os.system(clear)
                    board_and_console()
                    clear_board()
                    clear_opp_pieces()
                    set_console()
                    sleep(1)
                    return -1
                continue

        cmds = cmd.split()
        if len(cmds) < 2:
            set_console("Error: invalid command.")
            continue

        piece_input = " ".join(cmds[:-1])
        piece_name = cn.KEYWORD_MAPPER.get(piece_input.upper())
        if piece_name is None:
            set_console(f"Error: no such piece '{piece_input}' exists.")
            continue
        if not remaining_pieces.get(piece_name):
            set_console(f"Error: all pieces of {piece_name} have already been placed.")
            continue

        pos_input = cmds[-1]
        x, y = parse_coords(pos_input)
        if x is None and y is None:
            set_console(f"Error: invalid or forbidden position '{pos_input}'.")
            continue

        pos = pos_input.upper()
        if board.get_at(x, y) is not None:
            set_console(f"Error: {pos} occupied by {board.get_at(x, y).name()}.")
            continue

        piece = PIECES.get(piece_name).generate_piece()
        remaining_pieces[piece_name] -= 1
        set_console(f"{piece_name} placed at position {pos}!")
        board.place(piece, x, y)

    os.system(clear)
    board_and_console()
    input("All pieces have been placed! Press 'ENTER' to begin the game.")
    return 0


def handle_turn(result: int) -> None:
    if result != cn.MOVE_MADE:
        fallen = board.recently_killed()
        rank = fallen.rank

        set_console("CHALLENGE! Examining outcome...")
        board.set_challenge()
        os.system(clear)
        board_and_console()
        sleep(1)

        board.restore_position()
        match result:
            case cn.OPP_ELIM:
                set_console(f"You ate the opponent's {fallen.name()} {cn.SYMBOLS[rank]}!")
            case cn.USR_ELIM:
                set_console(f"The opponent ate your {fallen.name()} {cn.SYMBOLS[rank]}!")
            case cn.SPLIT:
                set_console("Split! Both your pieces have been eliminated (same rank).")
            case cn.USR_WINNER:
                set_console("You ate the opponent's FLAG 🏳️ and won!")
            case cn.OPP_WINNER:
                set_console("The opponent captured your FLAG 🏳️. Better luck next time!")

        if result < 0:
            reveal_opp_pieces()
            os.system(clear)
            board_and_console()
            input("Press 'ENTER' to return to main menu.")
            clear_board()
            set_console()
            return 1

        os.system(clear)
        board_and_console()
        sleep(2)

    set_console("It's your turn!")
    return 0


def handle_game() -> None:
    if place_pieces():
        set_game_status(False)
        return

    os.system(clear)
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
        cmd = input("> ")

        match cmd.lower():
            case "rules" | "r":
                display_rules()
                continue
            case "forfeit":
                if verify_user_action("forfeit"):
                    set_console("Game forfeited. Exiting to main menu...")
                    reveal_opp_pieces()
                    os.system(clear)
                    board_and_console()
                    clear_board()
                    sleep(2)
                    set_console()
                    break
                continue

        cmds = cmd.split()
        if len(cmds) != 2:
            set_console(f"Error: invalid command '{cmd}'.")
            continue

        if cmds[0].lower() == 'which':
            x, y = parse_coords(cmds[1])
            if x is None and y is None:
                set_console(f"Error: invalid position '{cmds[1]}'.")
                continue

            selected_piece = board.get_at(x, y)
            if selected_piece is None:
                set_console("Error: blank position selected.")
                continue

            if selected_piece.opp:
                set_console(f"Piece at {cmds[1].upper()}: UNKNOWN (enemy piece selected)")
            else:
                set_console(f"Piece at {cmds[1].upper()}: {selected_piece.name()} {selected_piece}")
            continue

        x, y = parse_coords(cmds[0])
        if x is None and y is None:
            set_console(f"Error: invalid position '{cmds[0]}'.")
            continue
        operation = MOVES.get(cmds[1].lower())
        if operation is None:
            set_console(f"Error: invalid operation '{cmds[1]}'.")
            continue

        if board.get_at(x, y) is not None and board.get_at(x, y).opp:
            set_console("Error: enemy piece selected.")
            continue

        status, result = operation.generate_move().execute(board, x, y)
        if status != cn.SUCCESS:
            match status:
                case cn.EMPTY_CELL:
                    set_console("Error: empty cell selected.")
                case cn.OUT_OF_BOUNDS:
                    set_console("Error: out-of-bounds move.")
                case cn.FRIENDLY_FIRE:
                    set_console("Error: move blocked by a friendly piece.")
            continue

        if handle_turn(result):
            break

        set_console("It's the opponent's turn. Calculating move...")
        os.system(clear)
        board_and_console()
        sleep(2)

        # Repeatedly choose random piece until valid movable piece is chosen
        opp_choice = opp_pieces[randrange(len(opp_pieces))]
        opp_x, opp_y = opp_choice.get_pos()
        while ((opp_x == -1 and opp_y == -1)
                or board.is_surrounded(opp_choice)
                or not opp_choice.opp):
            opp_choice = opp_pieces[randrange(len(opp_pieces))]
            opp_x, opp_y = opp_choice.get_pos()

        # Repeatedly choose random move until valid move is chosen
        move_obj = MOVES.get(list(MOVES)[randrange(4)]).generate_move()
        opp_status, opp_res = move_obj.execute(board, opp_x, opp_y)
        while opp_status != cn.SUCCESS:
            move_obj = MOVES.get(list(MOVES)[randrange(4)]).generate_move()
            opp_status, opp_res = move_obj.execute(board, opp_x, opp_y)

        if handle_turn(opp_res):
            break

    set_game_status(False)
    clear_opp_pieces()


def start() -> None:
    while True:
        os.system(clear)
        board_and_console()
        print_commands()
        print("Please input a command.")
        cmd = input("> ").lower()
        set_console()

        match cmd:
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
