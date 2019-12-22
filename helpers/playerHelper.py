
_NotSTABLE = 0
_STABLE = 1

_BLACK = 1
_WHITE = 2
_EMPTY = 0

# mark a copy version of stableBoard
def markStable(stableBoard,x,y):
    key = ""+str(x)+""+str(y)
    stableBoard.add(key)


# return isStable for a copy version of stableBoard
def isStable(stableBoard,x,y):
    key = ""+str(x)+""+str(y)

    return key in stableBoard


def getOpColor(color):
    mycolor = color
    if mycolor == _BLACK:
        return _WHITE
    return _BLACK
