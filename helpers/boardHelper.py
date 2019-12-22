from intelligence.heuristics import eval
import helpers.playerHelper as playerHelper

_NotSTABLE = 0
_STABLE = 1

def getCaseColor(board, x, y):
    return board._board[x][y]


def isOnFrontier(board, x, y):
    size = board.get_board_size()
    if x >= 0 and x < size and (y == 0 or y == size - 1):
        return True
    if y >= 0 and y < size and (x == 0 or x == size - 1):
        return True

def getOpColor(color):
    return 1 if color == 2 else 2

def createNewStableDic(size):
    stable = {}
    for x in range(size):
            for y in range(size):
                key = ""+str(x)+""+str(y)
                stable[key] =_NotSTABLE
    return stable

def legal_moves_for_player(board,player_color):
        size = board.get_board_size()
        moves = []
        for x in range(0,size):
            for y in range(0,size):
                if board.lazyTest_ValidMove(player_color, x, y):
                    moves.append([player_color,x,y])
        if len(moves) is 0:
            moves = [[player_color, -1, -1]] # We shall pass
        return moves

# base on next player on current board
def getSortedMoves(board,player):
    sortedMoves = []
    # moves = legal_moves_for_player(board,player_color)
    tmp_player = board._nextPlayer
    moves = board.legal_moves()
    for m in moves:
        board.push(m)
        sortedMoves.append((m,eval.getTotal2(player,tmp_player)))
        # sortedMoves.append((m,eval.evalBoard(board,player,tmp_player)))
        board.pop()
    sortedMoves = sorted(sortedMoves, key=lambda node: node[1], reverse=True)
    sortedMoves = [node[0] for node in sortedMoves]
    return sortedMoves

