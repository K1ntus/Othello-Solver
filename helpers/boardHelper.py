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