
import helpers.playerHelper as playerHelper

#  ------------------------------ Corner Grab ---------------------------------#

# measures if the current player can take a corner with its next move, always high score
# positive score if my player is next player else negative
def cornerGrab(player):
    if (player._board._nbBLACK + player._board._nbWHITE) < 10:
        return 0
    myNbGrab = 0
    currentBoard = player._board
    size = currentBoard.get_board_size() - 1
    if currentBoard._nextPlayer == player._mycolor:
        cornerList = [[0, size], [size, size], [size, 0], [0, 0]]
        moves = currentBoard.legal_moves()
        for move in moves:
            pos = [move[1], move[2]]
            if pos in cornerList:
                myNbGrab += 1

    opNbGrab = 0
    if currentBoard._nextPlayer == playerHelper.getOpColor(player):
        cornerList = [[0, size], [size, size], [size, 0], [0, 0]]
        moves = currentBoard.legal_moves()
        for move in moves:
            pos = [move[1], move[2]]
            if pos in cornerList:
                opNbGrab -= 1

    if currentBoard._nextPlayer == player._mycolor:
        return myNbGrab * 25
    else:
        return opNbGrab * 25


def cornerGrabNegaMax(player,color):
    if (player._board._nbBLACK + player._board._nbWHITE) < 12:
        return 0
    myNbGrab = 0
    currentBoard = player._board
    size = currentBoard.get_board_size() - 1
    cornerList = [[0, size], [size, size], [size, 0], [0, 0]]
    if currentBoard._nextPlayer == color:
        moves = currentBoard.legal_moves()
        for move in moves:
            pos = [move[1], move[2]]
            if pos in cornerList:
                myNbGrab += 1

    opNbGrab = 0
    if currentBoard._nextPlayer == playerHelper.getOpColor(color):
        moves = currentBoard.legal_moves()
        for move in moves:
            pos = [move[1], move[2]]
            if pos in cornerList:
                opNbGrab -= 1

    if currentBoard._nextPlayer == color:
        return myNbGrab * 25
    else:
        return opNbGrab * 25