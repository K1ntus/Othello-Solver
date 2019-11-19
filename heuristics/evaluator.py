from BoardWeight import BoardStaticWeight


# count the corner score on the board of the player
def get_corner_score(board, my_player):
    my_score = 0
    enemy_score = 0
    enemy = board._flip(my_player)
    last_index = board.get_board_size() - 1;
    if board[0][last_index] == my_player:
        my_score += BoardStaticWeight.weightTable[0][last_index]
    if board[last_index][0] == my_player:
        my_score += BoardStaticWeight.weightTable[last_index][0]
    if board[0][0] == my_player:
        my_score += BoardStaticWeight.weightTable[0][0]
    if board[last_index][last_index] == my_player:
        my_score += BoardStaticWeight.weightTable[last_index][last_index]

    if board[0][last_index] == enemy:
        enemy_score += BoardStaticWeight.weightTable[0][last_index]
    if board[last_index][0] == enemy:
        enemy_score += BoardStaticWeight.weightTable[last_index][0]
    if board[0][0] == enemy:
        enemy_score += BoardStaticWeight.weightTable[0][0]
    if board[last_index][last_index] == enemy:
        enemy_score += BoardStaticWeight.weightTable[last_index][last_index]

    return 100 * (my_score - enemy_score) / (my_score + enemy_score)


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

# mobility : score is according to the number of moves the player can make on the current state of the game
# The objective is to mobilize my player and restrict enemy
def get_mobility_score(board,my_player):
    my_legal_moves = 0
    enemy_legal_moves = 0
    enemy = board._flip(my_player)

    #     TODO calculate score
