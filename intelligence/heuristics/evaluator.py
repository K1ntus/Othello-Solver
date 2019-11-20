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

    return score

def eval(player, nb_move):
    res = 0
    res += get_corner_score(player)
    (b,w) = evaluateBoard(player._board)
    if(player._mycolor is Reversi.Board._BLACK):
        res += b
    else:
        res += w
    
    
    res += get_disc_parity_score(player)
    
    res += get_next_corner_score(player._board)    
    
    res += get_mobility_score(player, nb_move)
    
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
                nbWhite += BoardStaticWeight.weightTableStable[y][x]
            elif c is board._BLACK:
                nbBlack += BoardStaticWeight.weightTableStable[y][x]
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
    if player._mycolor == board._BLACK :
        return 100 * (nb_black-nb_white)/(nb_black+nb_white)
    elif player._mycolor == board._WHITE:
        return 100 * (nb_white-nb_black)/(nb_black+nb_white)
