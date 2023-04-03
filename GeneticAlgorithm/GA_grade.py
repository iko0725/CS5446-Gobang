'''遗传算法打分函数'''
import copy

MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
MAX_POINT = 100000
SECOND_MAX = 5000
player1 = 1
player2 = 2


def find_all_connect(current_board,player,move,n_in_line = 5):
    # move as center, find connected points
    x_this, y_this = move
    board = copy.deepcopy(current_board)
    width = len(board[0])
    height = len(board)
    # get the boundaries
    up = min(x_this, n_in_line - 1)
    down = min(height - 1 - x_this, n_in_line - 1)
    left = min(y_this, n_in_line - 1)
    right = min(width - 1 - y_this, n_in_line - 1)
    neighbour = [] # store neighbour points
    neighbour.append(move)
    # --
    for i in range(left):
        position = (x_this,y_this-1-i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(right):
        position = (x_this,y_this+1+i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    # \
    up_left = min(up, left)
    down_right = min(down, right)
    for i in range(up_left):
        position = (x_this-1-i,y_this-1-i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(down_right):
        position = (x_this+1+i,y_this+1+i)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    # |
    for i in range(up):
        position = (x_this -1 - i, y_this)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(down):
        position = (x_this + 1 + i, y_this)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    # /
    up_right = min(up, right)
    down_left = min(down, left)
    for i in range(up_right):
        position = (x_this - 1 - i, y_this + i + 1)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    for i in range(down_left):
        position = (x_this + 1 + i, y_this - i - 1)
        if board[position[0]][position[1]] == player:
            neighbour.append(position)
        else:
            break
    return neighbour


def count_neighbour(current_board,player,vertex,n_in_line = 5):
    # vertex and its connected points
    x_this, y_this = vertex
    board = copy.deepcopy(current_board)
    width = len(board[0])
    height = len(board)
    # get the boundaries
    up = min(x_this, n_in_line - 1)
    down = min(height - 1 - x_this, n_in_line - 1)
    left = min(y_this, n_in_line - 1)
    right = min(width - 1 - y_this, n_in_line - 1)
    count = [] # store possible points
    up_left = min(up, left)
    down_right = min(down, right)
    up_right = min(up, right)
    down_left = min(down, left)
    # left
    tempt = 0
    for i in range(left):
        if board[x_this][y_this-1-i] == 0 :
            tempt = i
            break
        elif board[x_this][y_this-1-i] != player:
            tempt = -i
            break
        elif y_this-1-i == 0:
            tempt = - i - 1
            break
        else: # == player
            tempt = i + 1
    count.append(tempt)
    # up-left
    tempt = 0
    for i in range(up_left):
        if board[x_this - 1 - i][y_this - 1 - i] == 0 :
            tempt = i
            break
        elif board[x_this - 1 - i][y_this - 1 - i] != player:
            tempt = - i
            break
        elif y_this - 1 - i == 0 or x_this - 1 - i == 0:
            tempt = - i - 1
            break
        else:
            tempt = i + 1
    count.append(tempt)
    # up
    tempt = 0
    for i in range(up):
        if board[x_this - 1 - i][y_this] == 0 :
            tempt = i
            break
        elif board[x_this - 1 - i][y_this] != player:
            tempt = -i
            break
        elif x_this - 1 - i == 0:
            tempt = - i - 1
            break
        else:
            tempt = i + 1
    count.append(tempt)
    # up-right
    tempt = 0
    for i in range(up_right):
        if board[x_this - i - 1][y_this + 1 + i] == 0 :
            tempt = i
            break
        elif board[x_this - i - 1][y_this + 1 + i] != player:
            tempt = - i
            break
        elif x_this - 1 - i == 0 or y_this + i + 1 == width - 1:
            tempt = - i - 1
            break
        else:
            tempt = i + 1
    count.append(tempt)
    # right
    tempt = 0
    for i in range(right):
        if board[x_this][y_this +1 + i] == 0 :
            tempt = i
            break
        elif board[x_this][y_this + 1 + i] != player:
            tempt = -i
            break
        elif y_this + 1 + i == width - 1:
            tempt = - i - 1
            break
        else:
            tempt = i + 1
    count.append(tempt)
    # down-right
    tempt = 0
    for i in range(down_right):
        if board[x_this + i + 1][y_this + 1 + i] == 0 :
            tempt = i
            break
        elif board[x_this + i + 1][y_this + 1 + i] != player:
            tempt = -i
            break
        elif y_this + 1 + i == width - 1 or x_this + i + 1 == height - 1:
            tempt = - i - 1
            break
        else:
            tempt = i + 1
    count.append(tempt)
    # down
    tempt = 0
    for i in range(down):
        if board[x_this + i + 1][y_this] == 0 :
            tempt = i
            break
        elif board[x_this + i + 1][y_this] != player:
            tempt = -i
            break
        elif x_this + i + 1 == height - 1:
            tempt = - i - 1
            break
        else:
            tempt = i + 1
    count.append(tempt)
    # down-left
    tempt = 0
    for i in range(down_left):
        if board[x_this + i + 1][y_this - 1 - i] == 0 :
            tempt = i
            break
        elif board[x_this + i + 1][y_this - 1 - i] != player:
            tempt = -i
            break
        elif y_this - 1 - i == 0 or x_this + i + 1 == height - 1:
            tempt = - i - 1
            break
        else:
            tempt = i + 1
    count.append(tempt)
    count_dic = {}
    for i in count:
        if i in count_dic:
            count_dic[i] += 1
        else:
            count_dic[i] = 1
    return count_dic


# def eval_vertex(current_board,player,vertex,n_in_line = 5):
#     board = copy.deepcopy(current_board)
#     N = len(board[0])
#     dx= [1, 0, 1, 1]
#     dy= [0, 1, 1, -1]
#     x,y = vertex
#     num= [[0 for i in range(2*n_in_line)] for j in range(2)] 
#     for i in range(4) : 
#         sum = 1 
#         flag1 = 0 
#         flag2 = 0
#         # pos
#         tx = x + dx[i]
#         ty = y + dy[i]
#         while (tx >= 0 and tx < N
#                 and ty >= 0 and ty < N
#                 and board[tx][ty] == player) :
#             tx += dx[i]
#             ty += dy[i]
#             sum += 1
#         if(tx >= 0 and tx < N # check dead live 
#                 and ty >= 0 and ty < N
#                 and board[tx][ty] == 0):
#             flag1 = 1 #  live 

#         # neg
#         tx = x - dx[i]
#         ty = y - dy[i]
#         while (tx > 0 and tx < N
#                 and ty > 0 and ty < N
#                 and board[tx][ty] == player) :
#             tx -= dx[i]
#             ty -= dy[i]
#             sum += 1
#         if tx > 0 and tx < N and ty > 0 and ty < N and board[tx][ty] == 0:
#             flag2 = 1

#         if flag1 + flag2 > 0:
#             num[flag1 + flag2 - 1][sum] += 1
#     score = 0
#     if(num[0][5] + num[1][5] > 0):
#         score = max(score, 100000)
#     #  live 4 | double dead 4 |  dead4 live 3
#     elif(num[1][4] > 0
#             or num[0][4] > 1
#             or (num[0][4] > 0 and num[1][3] > 0)):
#         score = max(score, 5000)
#     # double live 3
#     elif(num[1][3] > 1):
#         score = max(score, 1000)
#     #  dead3 live 3
#     elif(num[1][3] > 0 and num[0][3] > 0):
#         score = max(score, 500)
#     # single live 3
#     elif(num[1][3] > 0):
#         score = max(score, 200)
#     #  dead4
#     elif (num[0][4] > 0):
#         score = max(score, 100)
#     # double live 2
#     elif(num[1][2] > 1):
#         score = max(score, 50)
#     #  dead3
#     elif(num[0][3] > 0):
#         score = max(score, 10)
#     # single live 2
#     elif(num[1][2] > 0):
#         score = max(score, 5)
#     #  dead2
#     elif(num[0][2] > 0):
#         score = max(score, 3)
#     return score


def eval_vertex(current_board,player,vertex,n_in_line = 5):
    board = copy.deepcopy(current_board)
    N = len(board[0])
    dx= [1, 0, 1, 1]
    dy= [0, 1, 1, -1]
    x,y = vertex
    num= [[0 for i in range(2*n_in_line)] for j in range(2)] 
    for i in range(4) : # four directions
        sum = 1 
        flag1 = 0 
        flag2 = 0
        # pos
        tx = x + dx[i]
        ty = y + dy[i]
        while (tx >= 0 and tx < N
                and ty >= 0 and ty < N
                and board[tx][ty] == player) :
            tx += dx[i]
            ty += dy[i]
            sum += 1
        if(tx >= 0 and tx < N # check
                and ty >= 0 and ty < N
                and board[tx][ty] == 0):
            flag1 = 1 # live

        # neg
        tx = x - dx[i]
        ty = y - dy[i]
        while (tx > 0 and tx < N
                and ty > 0 and ty < N
                and board[tx][ty] == player) :
            tx -= dx[i]
            ty -= dy[i]
            sum += 1
        if tx > 0 and tx < N and ty > 0 and ty < N and board[tx][ty] == 0:
            flag2 = 1

        if flag1 + flag2 > 0:
            num[flag1 + flag2 - 1][sum] += 1

    score = 0
    # five
    if(num[0][5] + num[1][5] > 0):
        score = max(score, 100000)
    # live 4 | double dead 4 | dead4 live 3
    elif(num[1][4] > 0
            or num[0][4] > 1
            or (num[0][4] > 0 and num[1][3] > 0)):
        score = max(score, 511)
    # double live 3
    elif(num[1][3] > 1):
        score = max(score, 255)
    #  dead3 live 3
    elif(num[1][3] > 0 and num[0][3] > 0):
        score = max(score, 127)
    # single live 3
    elif(num[1][3] > 0):
        score = max(score, 63)
    #  dead4
    elif (num[0][4] > 0):
        score = max(score, 31)
    # double live 2
    elif(num[1][2] > 1):
        score = max(score, 15)
    #  dead3
    elif(num[0][3] > 0):
        score = max(score, 7)
    # single live 2
    elif(num[1][2] > 0):
        score = max(score, 3)
    #  dead2
    elif(num[0][2] > 0):
        score = max(score, 1)
    return score



def eval_point(current_board,player,point,n_in_line = 5):
    neighbours = find_all_connect(current_board,player,point,n_in_line = 5)
    board = copy.deepcopy(current_board)
    board[point[0]][point[1]] = player
    maxpoint = 0
    for neighbour in neighbours:
        point = eval_vertex(board,player,neighbour,n_in_line)
        if point == MAX_POINT:
            return MAX_POINT
        elif point > maxpoint:
            maxpoint = point
    return maxpoint

def eval_move(current_board,players,move,n_in_line = 5):
    # consider attack and protect
    assert current_board[move[0]][move[1]] == 0, "There exists one cheese already!!!"
    tempt1 = eval_point(current_board,players[0],move,n_in_line)
    tempt2 = eval_point(current_board,players[1],move,n_in_line)
    return tempt1+tempt2, (tempt1 == MAX_POINT or tempt1 == SECOND_MAX)

def eval_individual(board, players,moves,n_in_line = 5):
    if len(set(moves)) != len(moves):
        return -1
    current_board = copy.deepcopy(board)
    players = list(players)
    value = 0
    sign = 1
    me = players[0]
    me_win = False # Ai win
    opp_win = False # opp win
    for move in moves:
        if me_win:
            value += 2 * MAX_POINT
        elif opp_win:
            value -= 2 * MAX_POINT
        else:
            evaluation = eval_move(current_board,players,move,n_in_line)
            if evaluation[1]: 
                if players[0] == me:
                    me_win = True
                else:
                    opp_win = True
            value += sign * evaluation[0] # evaluate one move
            current_board[move[0]][move[1]] = players[0] # 'put' one chess
            sign = -sign
            players.reverse()
    return value