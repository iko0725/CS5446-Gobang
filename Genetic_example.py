'''遗传算法AI'''
import sys 
sys.path.append('/home/zhanxin/Course/CS5446/Project/Final-Artificial-Intelligence-Project/pisqpipe')
import pdb
# import pisqpipe as pp
# from pisqpipe import DEBUG_EVAL
from GeneticAlgorithm import Gobang_GA


MAX_BOARD = 9
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


def isFree(x, y):
    """whether (x, y) is available"""
    return 0 <= x < width and 0 <= y < height and board[x][y] == 0


def brain_my(x, y):
    """my turn: take the step on (x,y)"""
    if isFree(x, y):
        board[x][y] = 1
    else:
        print("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    """oppoent's turn: take the step on (x,y)"""
    if isFree(x, y):
        board[x][y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    """???"""
    if isFree(x, y):
        board[x][y] = 3
    else:
        print("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    """take back the chess on (x,y)"""
    if 0 <= x < width and 0 <= y < height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    GA_AI = Gobang_GA(board,players_in_turn = [1,2],n_in_line=5,
                 time_limit = 40.0,
                 DNA_length=2,mutate_rate_limit = 0.01,
                 start_number=800,number_limit=500,sruvival_rate=0.1)
    i = 0
    move = GA_AI.get_action()
    x, y = move
    board[x][y] = 2
    print("AI action: ", x+1, y+1)
    if i > 1:
        # zs: maybe useful to debug
        print("DEBUG {} coordinates didn't hit an empty field".format(i))
    return (x,y)
    

def board_show():
    st = '  '
    for i in range(len(board[0])):
        if i > 9:
            st += str(i+1) + ' '
        else:
            st += ' ' + str(i+1) + ' '
    print(st)
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
                st += '.  '
        print(st)


# 判断 player 下了这个点之后有没有成 5
def isFive(board, p, player):
    size = MAX_BOARD
    count = 1
    # --
    i = p[1] + 1
    while True:
        if i >= size:
            break
        t = board[p[0]][i]
        if t != player:
            break
        count += 1
        i += 1
    i = p[1] - 1
    while True:
        if i < 0:
            break
        t = board[p[0]][i]
        if t != player:
            break
        count += 1
        i -= 1

    if count >= 5:
        # pdb.set_trace()
        return True

    # |
    count = 1
    i = p[0] + 1
    while True:
        if i >= size:
            break
        t = board[i][p[1]]
        if t != player:
            break
        count += 1
        i += 1
    i = p[0] - 1
    while True:
        if i < 0:
            break
        t = board[i][p[1]]
        if t != player:
            break
        count += 1
        i -= 1

    if count >= 5:
        # pdb.set_trace()
        return True

    # \
    count = 1

    i = 1
    while 1:
        x, y = p[0] + i, p[1] + i
        if x >= size or y >= size:
            break
        t = board[x][y]
        if t != player:
            break
        count += 1
        i += 1
    i = 1
    while 1:
        x, y = p[0] - i, p[1] - i
        if x < 0 or y < 0:
            break
        t = board[x][y]
        if t != player:
            break
        count += 1
        i += 1

    if count >= 5:
        # pdb.set_trace()
        return True

    # /
    count = 1
    i = 1
    while 1:
        x, y = p[0] + i, p[1] - i
        if x >= size or y < 0:
            break
        t = board[x][y]
        if t != player:
            break
        count += 1
        i += 1
    i = 1
    while 1:
        x, y = p[0] - i, p[1] + i
        if x < 0 or y >= size:
            break
        t = board[x][y]
        if t != player:
            break
        count += 1
        i += 1

    if count >= 5:
        return True

    return False


if __name__ == "__main__":
    index = 0
    board_show()
    action_seq_file =  open("./action_sequence.txt", "a")

    while index < 200:
        userinput = input('Your turn: ').split(",")
        x = int(userinput[0])-1
        y = int(userinput[1])-1

        while board[x][y] == 1 or board[x][y] == 2:
            userinput = input('Please enter valid action: ').split(",")
            x = int(userinput[0])-1
            y = int(userinput[1])-1 
        board[x][y] = 1
        action_seq_file.write(f"Player1: {x+1},{y+1}\n")
        board_show()
        if isFive(board,(x,y), 1):
            action_seq_file.write(f"Player 1 win the game\n")
            print('Player 1 win the game !!!')
            action_seq_file.close()
            break

        AI_action = brain_turn()
        action_seq_file.write(f"Player2: {AI_action[0]+1},{AI_action[1]+1}\n")
        board_show()
        if isFive(board,AI_action, 2):
            action_seq_file.write(f"Player 2 win the game\n")
            print('Player 2 win the game !!!')
            action_seq_file.close()
            break

        index +=1
# 10,10 9,10 11,8 9,9 8,7 10,8 8,9 7,9