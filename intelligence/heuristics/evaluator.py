import time

from game.board import Reversi
from intelligence.heuristics.BoardWeight import BoardStaticWeight


# count the corner score on the board of the player
def get_corner_score(user):
    board = user._board
 
    (w,b) = evaluateBoard(board)
    enemy_score = w
    my_score = b
    if user._mycolor is Reversi.Board._WHITE:
        enemy_score = b
        my_score = w
        
        
    
        
#     enemy = player._board._flip(player)
#     last_index = board.get_board_size() - 1;
#     if board._board[0][last_index] == player:
#         my_score += BoardStaticWeight.weightTable[0][last_index]
#     if board._board[last_index][0] == player:
#         my_score += BoardStaticWeight.weightTable[last_index][0]
#     if board._board[0][0] == player:
#         my_score += BoardStaticWeight.weightTable[0][0]
#     if board._board[last_index][last_index] == player:
#         my_score += BoardStaticWeight.weightTable[last_index][last_index]
# 
#     if board._board[0][last_index] == enemy:
#         enemy_score += BoardStaticWeight.weightTable[0][last_index]
#     if board._board[last_index][0] == enemy:
#         enemy_score += BoardStaticWeight.weightTable[last_index][0]
#     if board._board[0][0] == enemy:
#         enemy_score += BoardStaticWeight.weightTable[0][0]
#     if board._board[last_index][last_index] == enemy:
#         enemy_score += BoardStaticWeight.weightTable[last_index][last_index]

    try:
        score = 100 * (my_score - enemy_score) / (my_score + enemy_score)
    except ZeroDivisionError:
        score = 100 * (my_score - enemy_score) / (my_score + 1 + enemy_score)
        
#     score = (my_score - enemy_score)
    print("Score Enemy:", enemy_score, "My Score:", my_score)
    if(score >= 0):
        print("POS SCORE: ", score)
    else:
        print("NEG SCORE:", score)
#     time.sleep(1)
    return score



def evaluateBoard(board):
    nbBlack = 0
    nbWhite = 0
    empty_cells = 0
    y = 0
    for l in board._board:
        x = 0
        for c in l:
            if c is board._WHITE:
                nbWhite += BoardStaticWeight.weightTable[y][x]
            elif c is board._BLACK:
                nbBlack += BoardStaticWeight.weightTable[y][x]
            else:
                empty_cells += 1
            x += 1
        y += 1
    
    
    return (nbBlack, nbWhite)

# count the score if the player can place make a legal move on the corners
def get_next_corner_score(board):
    #     get all legal moves
    last_index = board.get_board_size() - 1;
    moves = board.legal_moves();
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

# mobility : score is according to the number of moves the player can make
def get_mobility_score(board,player):
    my_score = 0
    enemy_score = 0
    enemy = board._flip(player)
    #     TODO calculate score
