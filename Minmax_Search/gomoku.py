from ai import AI
from config import Config
from score import score
import time
import argparse
from datetime import datetime
import json

parser = argparse.ArgumentParser(description='DC-GAN on PyTorch')
parser.add_argument('--board-size', default=9,
                    help='board size, assuming the board is a square', type=int)
parser.add_argument('--first', default='me', type=str,
                    help="who first? 'me' for player, 'ai' for AI")
parser.add_argument('--player1_name', default='minmax',
                    type=str, help='player1 name')
parser.add_argument('--player2_name', default='minmax',
                    type=str, help='player2 name')


args = parser.parse_args()

MAX_BOARD = args.board_size
player1_name = args.player1_name
player2_name = args.player2_name
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
actions = {player1_name: [], player2_name: []}
config = Config()
myAI = None


def save_game(move_history, player1_name, player2_name, winner, first_player):
    timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    game_data = {
        "move_history": move_history,
        'winner': winner,
        "first player": first_player,
        "timestamp": timestamp
    }

    filename = f"p1_{player1_name}_p2_{player2_name}_move_history.json"

    print('Current time: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with open(filename, "a+") as outfile:
        # add a new line before each new game
        json.dump(game_data, outfile)
        outfile.write('\n')
    print(f"Game saved to {filename}")


class PP:
    # zs: to simulate the pisqpipe package
    def __init__(self):
        self.height = MAX_BOARD
        self.width = MAX_BOARD
        self.terminateAI = None

    def pipeOut(self, what):
        print(what)

    def do_mymove(self, x, y):
        brain_my(x, y)
        self.pipeOut("{},{}".format(x, y))

    def do_oppmove(self, x, y):
        brain_opponents(x, y)
        self.pipeOut("{},{}".format(x, y))
        # print('opponent move: {}, {}'.format(x, y))


def brain_turn():
    if pp.terminateAI:
        return

    global myAI
    opp_move = None
    if myAI.turnChecked:
        opp_move = myAI.get_opponent_move(board)
        myAI.set(opp_move, 2)
    else:
        myAI = AI(board)
        if myAI.white_or_black():
            myAI.searchDeep = config.searchDeep_black
        else:
            myAI.searchDeep = config.searchDeep_white
        myAI.searchDeep_ = myAI.searchDeep
        myAI.turnChecked = True

    if myAI.turnChecked and len(myAI.theBoard.allSteps) <= 4:
        myAI.searchDeep = myAI.searchDeep_ - 2
    else:
        myAI.searchDeep = myAI.searchDeep_

    myAI.theBoard.startTime = time.time()
    winner = None

    if_only = False
    if not myAI.if_found_vcx:
        # 如果之前已经找到，之后就不需要再搜了
        move, if_only = myAI.get_move()
    # print(time.time() - myAI.theBoard.startTime)
    if not if_only:
        move_vcx = myAI.get_move_vcx()
        if move_vcx:
            myAI.if_found_vcx = True
            print('HHHHHHH, you are DEAD!!!')
            winner = 'opponent: ai'
            move = move_vcx
    print("time used: %.2f s" % (time.time() - myAI.theBoard.startTime))
    # not the same as the board index
    print('AI move: {}, {}'.format(move[0]+1, move[1]+1))
    myAI.set(move, 1)
    x, y = move
    pp.do_mymove(x, y)

    return opp_move, move, winner


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return

    global myAI
    myAI = AI(board)

    pp.pipeOut("OK")


def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0

    global myAI
    myAI = AI(board)

    pp.pipeOut("OK")


def isFree(x, y):
    """whether (x, y) is available"""
    return 0 <= x < pp.width and 0 <= y < pp.height and board[x][y] == 0


def brain_my(x, y):
    """my turn: take the step on (x,y)"""
    if isFree(x, y):
        # print('my move: {}, {}'.format(x, y))
        board[x][y] = 1
        actions[player1_name].append((x+1, y+1))
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x+1, y+1))


def brain_opponents(x, y):
    """oppoent's turn: take the step on (x,y)"""
    # print('opponent move: {}, {}'.format(x, y))
    if isFree(x, y):
        # print('opponent move: {}, {}'.format(x, y))
        board[x][y] = 2
        actions[player2_name].append((x+1, y+1))
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x+1, y+1))


def brain_block(x, y):
    """???"""
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    """take back the chess on (x,y)"""
    if 0 <= x < pp.width and 0 <= y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_end(x, y):
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


def brain_show():
    st = '  '
    for i in range(len(board[0])):
        if i > 9:
            st += str(i+1) + ' '
        else:
            st += ' ' + str(i+1) + ' '
    print(st)
    # print('start')
    c = 0
    for row in board:
        if c > 9:
            print(c+1, end=' ')
        else:
            print('', c+1, end=' ')
        c += 1
        st = ''
        for ii in row:
            if ii == 1:
                st += 'O  '
            elif ii == 2:
                st += 'X  '
            else:
                st += '-  '
        print(st)


def brain_play():
    # actions = []
    while 1:
        print('(if you want to quit, ENTER quit)')
        x = input("Your turn, please give a coordinate 'x y':")
        print()
        if x == 'quit':
            print('You quit.')
            return None
        x = x.split()
        try:
            x_coord = int(x[0])-1
            y_coord = int(x[1])-1
            # print('x_coord: ', x_coord+1)
            # print('y_coord: ', y_coord+1)
        except ValueError or IndexError:
            print('Invalid input!')
            continue

        try:
            brain_opponents(x_coord, y_coord)
        except ValueError or IndexError:
            print('Invalid input!')
            continue

        break
    # brain_show()
    return 0


def brain_play_auto(moves):
    # actions = []
    while 1:
        # print('(if you want to quit, ENTER quit)')
        # x = input("Your turn, please give a coordinate 'x y':")
        # print()
        x = moves
        # if x == 'quit':
        #     print('You quit.')
        #     return None
        # x = x.split()
        try:
            x_coord = int(x[0])-1
            y_coord = int(x[1])-1

            # x_coord = int(x[0])-2
            # y_coord = int(x[1])-2
            # print('x_coord: ', x_coord+1)
            # print('y_coord: ', y_coord+1)
        except ValueError or IndexError:
            print('Invalid input!')
            continue

        try:
            # print('x_coord: ', x_coord+1)
            brain_my(x_coord, y_coord)
        except ValueError or IndexError:
            print('Invalid input!')
            continue

        break
    # brain_show()
    return 0


def main():
    brain_init()
    print('You are X, Minmax is O')
    # player 1 is another algorithm, player 2 is Minmax
    print('You are player 1: ', player1_name)
    print('Your opponent player 2: ', player2_name)

    oppo_move = None
    move = None
    winner = None
    final_winner = None
    first_player = None

    if args.first == 'ai':
        print('Minmax goes first')
        oppo_move, move, winner = brain_turn()
        first_player = 'minmax'
        # actions[player2_name].append((move[0]+1, move[1]+1))
    elif args.first == 'me':
        print('You go first')
        first_player = 'another algorithm'
        pass
    else:
        raise ValueError("Argument 'first' should be either 'me' or 'ai'!")
    brain_show()

    # print('actions: ', actions)

    while brain_play() is not None:
        oppo_move, move, winner = brain_turn()

        if winner is not None:
            final_winner = winner
            print('winner', winner)

        # if oppo_move is not None:
        #     actions[player1_name].append((oppo_move[0]+1, oppo_move[1]+1))
        # if move is not None:
        #     actions[player2_name].append((move[0]+1, move[1]+1))
        brain_show()

    save_game(actions, player1_name, player2_name, final_winner, first_player)


def minmax_gobang(player1_name, player2_name,):
    brain_init()
    oppo_move = None
    move = None
    winner = None
    final_winner = None
    first_player = None

    if player1_name == 'minmax':
        print('Minmax goes first')
        oppo_move, move, winner = brain_turn()
        minmax_actions = actions['minmax']
        minmax_move = minmax_actions[-1]
        print('minmax_actions', minmax_actions)
        print('minmax_move', minmax_move)
        brain_play_auto(minmax_move)
        # oppo_move, move, winner = brain_turn()
        # first_player = 'Minmax'
        # actions[player2_name].append((move[0]+1, move[1]+1))

    elif player2_name == 'minmax':
        print(f'{player2_name} goes first')
        # first_player = 'another algorithm'

    else:
        raise ValueError(
            "You need to indicate minmax if you want to play against it!")
    brain_show()
    print('actions: ', actions)
    minmax_actions = actions['minmax']
    minmax_move = minmax_actions.pop(0)
    print('minmax_move', minmax_move)

    while brain_play_auto(minmax_move) is not None:
        oppo_move, move, winner = brain_turn()

        if winner is not None:
            final_winner = winner
            print('winner', winner)

        # if oppo_move is not None:
        #     actions[player1_name].append((oppo_move[0]+1, oppo_move[1]+1))
        # if move is not None:
        #     actions[player2_name].append((move[0]+1, move[1]+1))
        brain_show()
        print('actions: ', actions)
        minmax_actions = actions['minmax']
        minmax_move = minmax_actions.pop(0)


if __name__ == "__main__":
    pp = PP()
    # minmax_gobang('minmax', 'another algorithm')
    main()
