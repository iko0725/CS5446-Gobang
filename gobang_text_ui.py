import argparse
import json
import copy
from datetime import datetime

from GeneticAlgorithm.GA_AI import Gobang_GA
from Minmax_Search.ai import AI as Minmax_AI
from MCTS.pure_MCTS import MCTS

import torch
from alphazero.alpha_zero_mcts import AlphaZeroMCTS
from alphazero.chess_board import ChessBoard
from alphazero.policy_value_net import PolicyValueNet
from alphazero.self_play_dataset import SelfPlayData, SelfPlayDataSet
from main import *
from evaluation import *
from DQN.test import *

argparser = argparse.ArgumentParser()

argparser.add_argument(
    "--board_size",
    type=int,
    default=9,
    help="The size of the board",
)

# ==== Choose from: genetic, alphazero, minmax, mcts, ====
# TODO: Support for DQN
argparser.add_argument(
    "--player1_name",
    type=str,
    default="genetic",
    help="The symbol of player 1",
)

argparser.add_argument(
    "--player2_name",
    type=str,
    default="mcts",
    help="The symbol of player 2",
)
argparser.add_argument(
    "--iteration",
    type=int,
    default="3000",
    help="The iteration of model",
)

argparser.add_argument(
    "--save_dir",
    type=str,
    default="results_size",
    help="The directory to save the model",
)

BOARD_SIZE = argparser.parse_args().board_size
player1_name = argparser.parse_args().player1_name
player2_name = argparser.parse_args().player2_name
iteration = argparser.parse_args().iteration
save_dir = argparser.parse_args().save_dir
board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
players = ["X", "O"]
# save actions to a dictionary
move_history = {"X": [], "O": []}


####################
# init alphazero, not available for self play
chessboard_alpha = ChessBoard(BOARD_SIZE, 6)
if player1_name == "alphazero" or player2_name == "alphazero":
    assert BOARD_SIZE == 9 or BOARD_SIZE == 15, f"invalid board size: {BOARD_SIZE}"
    assert iteration in [500, 1000, 1500, 2000, 2500,
                         3000], f"invalid iteration number {iteration}"
    policy_value_net = torch.load(
        f"alphazero/board_{BOARD_SIZE}/iter_{iteration}.pth").cuda()
    c_puct = 3
    n_mcts_iters = 500
    mcts = AlphaZeroMCTS(policy_value_net, c_puct=c_puct, n_iters=n_mcts_iters)
    mcts.reset_root()
    chessboard_alpha.clear_board()

print("Gobang Game")
print("Player 1: X, Name: ", player1_name)
print("Player 2: O, Name: ", player2_name)
print()

####################
# init alphazero, not available for self play

if player1_name == "dqn" or player2_name == "dqn":
    assert BOARD_SIZE == 9 or BOARD_SIZE == 15, f"invalid board size: {BOARD_SIZE}"
    assert iteration in [500, 1000, 1500, 2000, 2500,
                         3000], f"invalid iteration number {iteration}"
    model = main.MyChain()
    N=BOARD_SIZE
    serializers.load_npz(f'./DQN/model_{BOARD_SIZE}/{iteration}.model', model)
    dqn_board = np.zeros((N, N), dtype=np.int8)


def Pure_MCTS_Algorithm(original_board):
    MCTS_board = copy.deepcopy(original_board)
    empty_flag = True
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if MCTS_board[i][j] == 'X':
                MCTS_board[i][j] = 1
                empty_flag = False
            elif MCTS_board[i][j] == 'O':
                MCTS_board[i][j] = 2
                empty_flag = False
            else:
                MCTS_board[i][j] = 0
    if empty_flag == True:
        return int(BOARD_SIZE/2), int(BOARD_SIZE/2)

    MCTS_AI = MCTS(MCTS_board,
                   players_in_turn=[1, 2],  # brain is 1
                   n_in_line=5,
                   confidence=1.96,
                   time_limit=10,
                   max_simulation=5,  # should not be too large
                   max_simulation_one_play=50)
    move = MCTS_AI.get_action()
    return move


def GeneticAlgorithm(original_board):
    GA_board = copy.deepcopy(original_board)
    empty_flag = True
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if GA_board[i][j] == 'X':
                GA_board[i][j] = 1
                empty_flag = False
            elif GA_board[i][j] == 'O':
                GA_board[i][j] = 2
                empty_flag = False
            else:
                GA_board[i][j] = 0
    if empty_flag == True:
        return int(BOARD_SIZE/2), int(BOARD_SIZE/2)
    GA_AI = Gobang_GA(GA_board, players_in_turn=[1, 2], n_in_line=5,
                      time_limit=40.0,
                      DNA_length=2, mutate_rate_limit=0.01,
                      start_number=800, number_limit=500, sruvival_rate=0.1)
    move = GA_AI.get_action()
    return move


def MinMaxAlgorithm(original_board):
    MinMax_board = copy.deepcopy(original_board)
    empty_flag = True
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if MinMax_board[i][j] == 'X':
                MinMax_board[i][j] = 1
                empty_flag = False
            elif MinMax_board[i][j] == 'O':
                MinMax_board[i][j] = 2
                empty_flag = False
            else:
                MinMax_board[i][j] = 0
    if empty_flag == True:
        return int(BOARD_SIZE/2), int(BOARD_SIZE/2)
    MinMax_AI = Minmax_AI(MinMax_board)
    move, _ = MinMax_AI.get_move()
    # print('move (row-1, col-1) is  ', move)
    return move

def board_show(ga_board):
    st = '  '
    for i in range(len(ga_board[0])):
        if i > 9:
            st += str(i+1) + ' '
        else:
            st += ' ' + str(i+1) + ' '
    print(st)
    c = 0
    for row in ga_board:
        if c > 9:
            print(c+1, end=' ')
        else:
            print('', c+1, end=' ')
        c += 1
        st = ''
        for ii in row:
            if ii == 1:
                st += '1  '
            elif ii == 2:
                st += '2  '
            else:
                st += '.  '
        print(st)


def save_game(move_history, winner, board_size, player1_name, player2_name):
    game_data = {
        "move_history": move_history,
        "winner": winner,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    filename = f"{save_dir}_{board_size}/p1_X_{player1_name}_p2_O_{player2_name}_size_{board_size}_history.json"

    print('Current time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with open(filename, "a+") as outfile:
        json.dump(game_data, outfile)
        outfile.write("\n")
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


def get_move(current_player_id):
    if current_player_id == 0:
        model_name = argparser.parse_args().player1_name
    else:
        model_name = argparser.parse_args().player2_name

    if model_name == 'genetic':
        action = GeneticAlgorithm(board)
        return action[0], action[1]
    elif model_name == "alphazero":
        action = mcts.get_action(chessboard_alpha)
        x = (action+BOARD_SIZE)//BOARD_SIZE-1
        y = (action+BOARD_SIZE) % BOARD_SIZE
        return int(x), int(y)
    elif model_name == "dqn":
        actions = np.array(np.where(dqn_board == 0))
        r = main.getMove(dqn_board, model, True, 2)
        action = actions[:, r]
        return action[0], action[1]
    elif model_name == "mcts":
        action = Pure_MCTS_Algorithm(board)
        return action[0], action[1]
    elif model_name == "minmax":
        action = MinMaxAlgorithm(board)
        return action[0], action[1]
    else:
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


print_board(board)

current_player = 0
winner = None

while True:
    # add tie condition
    if len(move_history['X']) + len(move_history['O']) == (BOARD_SIZE * BOARD_SIZE) - 1 and winner is None:
        print("Tie!")
        break
    row, col = get_move(current_player)
    # print(row, col, current_player)
    if player1_name == "alphazero" or player2_name == "alphazero":
        loc = row*BOARD_SIZE+col
        chessboard_alpha.do_action(loc)
    if player1_name == "dqn" or player2_name == "dqn":
            dqn_board[row, col] = 1
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

save_game(move_history, winner, BOARD_SIZE, player1_name, player2_name)

print("Move history:", move_history)
