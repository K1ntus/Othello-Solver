import helpers.boardHelper as boardHelper
import helpers.playerHelper as playerHelper
from intelligence.heuristics import BoardWeight


# mobility heuristic
# try to limit opponent player's legal moves
def mobility(player, color):
    currentBoard = player._board
    opcolor = playerHelper.getOpColor(color)
    myMobility = len(boardHelper.legal_moves_for_player(currentBoard, color))
    opMobility = len(boardHelper.legal_moves_for_player(currentBoard, opcolor))

    return 100 * (myMobility - opMobility) / (myMobility + opMobility + 1)


# 1 if my player is expected to make the last move
# -1 if other player is expected to make the last move
def parity(player, color):
    opcolor = playerHelper.getOpColor(color)
    currentBoard = player._board
    size = currentBoard.get_board_size() * currentBoard.get_board_size()
    remain = size - currentBoard._nbWHITE - currentBoard._nbBLACK
    if remain % 2 == 0:
        if opcolor == currentBoard._nextPlayer:
            return 1
        else:
            return -1
    else:
        if opcolor == currentBoard._nextPlayer:
            return -1
        else:
            return 1


# number of discs on the board between (color) as my player and other player
def discDiff(player, color):
    currentBoard = player._board
    nbBlack = currentBoard._nbBLACK
    nbWhite = currentBoard._nbWHITE
    if color == player._board._BLACK:
        return 100 * (nbBlack - nbWhite) / (nbBlack + nbWhite + 1)
    else:
        return 100 * (nbWhite - nbBlack) / (nbBlack + nbWhite + 1)


# ignore 1/4 zone according to occupied corner
# calculate the board score according to color as my player
def boardWeight(player, color):
    board = player._board
    # weightTable = [
    #     [200,    -100,    100,       8,      8,      8,      8,       100,      -100,     200],
    #     [-100,   -200,    100,     -50,    -50,    -50,    -50,       100,      -200,    -100],
    #     [100,     100,    150,      50,     25,     25,     50,       150,       100,     100],
    #     [50,      -50,     50,    -100,      0,      0,   -100,        50,       -50,      50],
    #     [50,      -50,     25,       0,      0,      0,      0,        25,       -50,      50],
    #     [50,      -50,     25,       0,      0,      0,      0,        25,       -50,      50],
    #     [50,      -50,     50,    -100,      0,      0,   -100,        50,       -50,      50],
    #     [100,     100,    150,      50,     25,     25,     50,       150,       100,     100],
    #     [-100,   -200,    100,     -50,    -50,    -50,    -50,       100,      -200,    -100],
    #     [200,    -100,    100,      50,     50,     50,     50,       100,      -100,     200],
    # ]

    weightTable = BoardWeight.BoardStaticWeight.weightTable3
#     weightTable = [
#         [200, -100, 100, 8, 8, 8, 8, 100, -100, 200],
#         [-100, -200, -50, -50, -50, -50, -50, -50, -200, -100],
#         [100, -50, 100, 50, 25, 25, 50, 100, -50, 100],
#         [50, -50, 50, -100, 0, 0, -100, 50, -50, 50],
#         [50, -50, 25, 0, 0, 0, 0, 25, -50, 50],
#         [50, -50, 25, 0, 0, 0, 0, 25, -50, 50],
#         [50, -50, 50, -100, 0, 0, -100, 50, -50, 50],
#         [100, -50, 100, 50, 25, 25, 50, 100, -50, 100],
#         [-100, -200, -50, -50, -50, -50, -50, -50, -200, -100],
#         [200, -100, 100, 50, 50, 50, 50, 100, -100, 200],
#     ]
#     weightTable = BoardWeight.BoardStaticWeight.weightTable2 + BoardWeight.BoardStaticWeight.weightPreventKillerMove * 2
# >>>>>>> f669021384ef8a5ee707f0b77f8c0665c324c49a
    empty = board._EMPTY

    size = board.get_board_size() - 1
    # if top left corner is occupied then ignore top left zone
    if boardHelper.getCaseColor(board, 0, 0) != empty:
        for y in range(1, 5):
            weightTable[0][y] = 0
        for x in range(1, 3):
            for y in range(5):
                weightTable[x][y] = 0
        for y in range(4):
            weightTable[3][y] = 0
        for y in range(3):
            weightTable[4][y] = 0
    # bottom left
    if boardHelper.getCaseColor(board, size, 0) != empty:
        for y in range(3):
            weightTable[5][y] = 0
        for y in range(4):
            weightTable[6][y] = 0
        for x in range(7, size):
            for y in range(5):
                weightTable[x][y] = 0
        for y in range(1, 5):
            weightTable[size][y] = 0

    # top right
    if boardHelper.getCaseColor(board, 0, size) != empty:
        for y in range(5, size):
            weightTable[0][y] = 0
        for x in range(1, 3):
            for y in range(5, size + 1):
                weightTable[x][y] = 0
        for y in range(6, size + 1):
            weightTable[3][y] = 0
        for y in range(7, size + 1):
            weightTable[4][y] = 0

    # bottom right
    if boardHelper.getCaseColor(board, size, size) != empty:
        for y in range(7, size + 1):
            weightTable[5][y] = 0
        for y in range(6, size + 1):
            weightTable[6][y] = 0
        for x in range(7, size):
            for y in range(5, size + 1):
                weightTable[x][y] = 0
        for y in range(5, size):
            weightTable[size][y] = 0

    my_weight = 0
    op_weight = 0
    for x in range(size + 1):
        for y in range(size + 1):
            if boardHelper.getCaseColor(board, x, y) == color:
                my_weight += weightTable[x][y]
            elif boardHelper.getCaseColor(board, x, y) == playerHelper.getOpColor(color):
                op_weight += weightTable[x][y]

    # if color == player._mycolor :
    #     return my_weight
    # else :
    #     return -op_weight
    return my_weight
