import time

from game.board import Reversi
from intelligence.heuristics.BoardWeight import BoardStaticWeight


# count the corner score on the board of the player
def get_corner_score( my_player):
    board = my_player._board
    board_arr = board._board
    my_score = 0
    enemy_score = 0
    enemy = board._flip(my_player)
    last_index = board.get_board_size() - 1
    if board_arr[0][last_index] == my_player:
        my_score += BoardStaticWeight.weightTable1[0][last_index]
    if board_arr[last_index][0] == my_player:
        my_score += BoardStaticWeight.weightTable1[last_index][0]
    if board_arr[0][0] == my_player:
        my_score += BoardStaticWeight.weightTable1[0][0]
    if board_arr[last_index][last_index] == my_player:
        my_score += BoardStaticWeight.weightTable1[last_index][last_index]

    if board_arr[0][last_index] == enemy:
        enemy_score += BoardStaticWeight.weightTable1[0][last_index]
    if board_arr[last_index][0] == enemy:
        enemy_score += BoardStaticWeight.weightTable1[last_index][0]
    if board_arr[0][0] == enemy:
        enemy_score += BoardStaticWeight.weightTable1[0][0]
    if board_arr[last_index][last_index] == enemy:
        enemy_score += BoardStaticWeight.weightTable1[last_index][last_index]
        

    try:
        score = 100 * (my_score - enemy_score) / (my_score + enemy_score)
    except ZeroDivisionError:
        score =  100 * (my_score - enemy_score) / (my_score + 1 + enemy_score)

    return (my_score, enemy_score)

def getHeuristicValue(player, nb_move):
    (w,b) = evaluateBoard(player._board)
#     (vb1,vw1) =  get_corner_score(player)
#     vb1 = vb1 * 0.5
#     vw1 = vw1 * 0.5
# #     (vb2,vw2) = get_next_corner_score(player._board)
#     (vb3,vw3) = (0,0)#get_disc_parity_score(player._board)
#     vb3 = vb3 * 0.2
#     vw3 = vw3 * 0.2
    me = 0
    enemy = 0
    
    
    
    if(player._mycolor is Reversi.Board._BLACK):
        me += w
        enemy += b
#         me += vb1
# #         me += vb2
#         me += vb3
#            
#         enemy += vw1
# #         enemy += vw2
#         enemy += vw3
    else:
        enemy += w
        me += b
#         enemy += vb1
# #         enemy += vb2
#         enemy += vb3
#           
#         me += vw1
# #         me += vw2
#         me += vw3
#     enemy += 1
    
    try :
        res = 100 * ((me - enemy) / (me+enemy))
    except ZeroDivisionError :
        res = 100 * ((me - enemy) / (me+enemy +1))
    
        
#     res = 0
#     res += get_corner_score(player)
#     (b,w) = evaluateBoard(player._board)
#     
#     if(player._mycolor is Reversi.Board._BLACK):
#         res += b
#     else:
#         res += w
# #     if(player._mycolor is Reversi.Board._BLACK):
# #         w = 1
# #         res += 100 * ((b - w)/(b+w))
# #     else:
# #         b = 1
# #         res += 100 * ((w - b)/(b+w))
#     
#     
#     res += get_disc_parity_score(player)
#     
#     res += get_next_corner_score(player._board)    
#     
# #     res += get_mobility_score(player, nb_move)
#     

#     print("Value found: ", res)
    return res

def evaluateBoard(board):
    nbBlack = 0
    nbWhite = 0
    empty_cells = 0
    y = 0
    for l in board._board:
        x = 0
        for c in l:
            if c is board._WHITE:
                nbWhite += BoardStaticWeight.weightTable1[y][x]
            elif c is board._BLACK:
                nbBlack += BoardStaticWeight.weightTable1[y][x]
            else:
                empty_cells += 1
            x += 1
        y += 1
    
    return (nbBlack, nbWhite)

# count the score if the player can place make a legal move on the corners
def get_next_corner_score(board):
    #     get all legal moves
    last_index = board.get_board_size() - 1
    moves = board.legal_moves()
    score = 100
    for m in moves:
        if m[1] == 0 and m[2] == 0:
            return score
        if m[1] == 0 and m[2] == last_index:
            return score
        if m[1] == last_index and m[2] == last_index:
            return score
        if m[1] == last_index and m[2] == 0:
            return score
    return 0

# mobility : score is according to the number of moves the player can make on the current state of the game
# The objective is to mobilize my player and restrict enemy
# my_mobility_score : should be evaluated before push move
def get_mobility_score(player,my_mobility_moves):
    board = player._board
    # get legal moves for next player (enemy)
    enemy_legal_moves = board.legal_moves()
    try :
        return 100 * (my_mobility_moves - enemy_legal_moves) / (my_mobility_moves + enemy_legal_moves)
    except ZeroDivisionError :
        return 100 * (my_mobility_moves - enemy_legal_moves) / (my_mobility_moves + enemy_legal_moves + 1)

# Disc parity : the score is according to the number of discs on the board
def get_disc_parity_score(player):
    board = player._board
    nb_black = board._nbBLACK
    nb_white = board._nbWHITE
#     if player._mycolor == board._BLACK :
#         return 100 * (nb_black-nb_white)/(nb_black+nb_white)
#     elif player._mycolor == board._WHITE:
#         return 100 * (nb_white-nb_black)/(nb_black+nb_white)
    return (nb_black, nb_white)
