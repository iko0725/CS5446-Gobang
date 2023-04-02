import argparse
import json
from datetime import datetime
# from gomoku import main

argparser = argparse.ArgumentParser()

argparser.add_argument(
    "--board_size",
    type=int,
    default=9,
    help="The size of the board",
)

argparser.add_argument(
    "--player1_name",
    type=str,
    default="min_max",
    help="The symbol of player 1",
)

argparser.add_argument(
    "--player2_name",
    type=str,
    default="genetic",
    help="The symbol of player 2",
)


def save_game(move_history, winner, player1_name, player2_name):
    game_data = {
        "move_history": move_history,
        "winner": winner,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    filename = f"p1_{player1_name}_p2_{player2_name}_move_history.json"

    print('Current time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with open(filename, "a+") as outfile:
        json.dump(game_data, outfile)
    print(f"Game saved to {filename}")


def print_board(board):
    print("  ", end="")
    for i in range(len(board)):
        print(f"{i + 1:2}", end=" ")
    print()

    for i, row in enumerate(board):
        print(f"{i + 1:2}", end=" ")
        for cell in row:
            print(cell or ".", end="  ")
        print()


def get_move():

    while True:
        try:
            user_input = input(
                "Enter your move (row col) or type 'quit' to exit: ")
            if user_input.lower() == "quit":
                return None, None

            row, col = map(int, user_input.split())
            if 1 <= row <= BOARD_SIZE and 1 <= col <= BOARD_SIZE:
                return row - 1, col - 1
        except ValueError:
            pass
        print("Invalid move. Please try again.")


def is_won(board, row, col, player):
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        count = 0
        for d in range(-4, 5):
            r, c = row + dr * d, col + dc * d
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
                if count == 5:
                    print(f"Player {player} wins!")
                    return True
            else:
                count = 0
    return False


BOARD_SIZE = argparser.parse_args().board_size
player1_name = argparser.parse_args().player1_name
player2_name = argparser.parse_args().player2_name
board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
players = ["X", "O"]
# save actions to a dictionary
move_history = {"X": [], "O": []}

print("Gobang Game")
print("Player 1: X, Name: ", player1_name)
print("Player 2: O, Name: ", player2_name)
print()

print_board(board)

current_player = 0
winner = None

while True:
    row, col = get_move()
    if row is None and col is None:
        print("Exiting the game.")
        break

    if not board[row][col]:
        board[row][col] = players[current_player]
        move_history[players[current_player]].append((row + 1, col + 1))
        print_board(board)

        if is_won(board, row, col, players[current_player]):
            winner = players[current_player]
            print(
                f"Player {current_player + 1} ({players[current_player]}) wins!")
            break

        current_player = 1 - current_player
    else:
        print("Invalid move. The cell is already occupied. Please try again.")

save_game(move_history, winner, player1_name, player2_name)

print("Move history:", move_history)
