
_NotSTABLE = 0
_STABLE = 1

_BLACK = 1
_WHITE = 2
_EMPTY = 0

# mark a copy version of stableBaord
def markStable(stableBaord,x,y):
    key = ""+str(x)+""+str(y)
    stableBaord.add(key)


# return isStable for a copy version of stableBoard
def isStable(stableBaord,x,y):
    key = ""+str(x)+""+str(y)

    return key in stableBaord


def getOpColor(color):
    mycolor = color
    if mycolor == _BLACK:
        return _WHITE
    return _BLACK
