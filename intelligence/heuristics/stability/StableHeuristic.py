from intelligence.heuristics import boardHelper
from intelligence.heuristics.stability import stable


def stability(currentBoard, player):
    op = currentBoard._flip(player)

    myStable = 20 * stabilityForPlayer(currentBoard, player)
    opStable = 20 * stabilityForPlayer(currentBoard, op)
    if (myStable + opStable) !=0 :
        return 100 * (myStable - opStable) / (myStable + opStable)
    else:
        return 0


# stability score for player
# player act just like color
def stabilityForPlayer(currentBoard, player):
    left = right = top = down = False
    stableBoard = stable.StableBoard(currentBoard.get_board_size())
    (nbTop, nbRight) = fromTopRight(currentBoard, player, stableBoard)
    if (nbTop == currentBoard.get_board_size()):
        top = True
    if (nbRight == currentBoard.get_board_size()):
        right = True
    (nbDown, nbLeft) = fromDownLeft(currentBoard, player, stableBoard)
    if (nbDown == currentBoard.get_board_size()):
        down = True
    if (nbLeft == currentBoard.get_board_size()):
        left = True

    (restNbTop, restNbLeft) = fromTopLeft(currentBoard, player, stableBoard, top, left)
    (restNbDown, restNbRight) = fromDownRight(currentBoard, player, stableBoard, down, right)
    stableBoard._nbStable = (nbTop + nbRight + nbDown + nbLeft + restNbTop + restNbDown + restNbRight + restNbLeft)

    markStableCompletelyFilled(currentBoard, player, stableBoard)
    markStableSurrondByStable(currentBoard, player, stableBoard)

    return stableBoard._nbStable


def fromTopRight(currentBoard, player, stableBoard):
    size = currentBoard.get_board_size() - 1
    nbTop = 0
    nbRight = 0

    for x in range(size, -1, -1):
        if boardHelper.getCaseColor(currentBoard, x, 0) == player:
            stableBoard.markStable(x, 0)
            nbTop += 1
        else:
            break
    for y in range(0, size + 1):
        if boardHelper.getCaseColor(currentBoard, size, y) == player:
            stableBoard.markStable(size, y)
            nbRight += 1
        else:
            break
    return (nbTop, nbRight)


def fromTopLeft(currentBoard, player, stableBoard, top, left):
    size = currentBoard.get_board_size()
    nbTop = nbLeft = 0
    if top == False:
        for x in range(0, size):
            if boardHelper.getCaseColor(currentBoard, x, 0) == player:
                stableBoard.markStable(x, 0)
                nbTop += 1
            else:
                break
    if left == False:
        for y in range(0, size):
            if boardHelper.getCaseColor(currentBoard, 0, y) == player:
                stableBoard.markStable(0, y)
                nbLeft += 1
            else:
                break
    return (nbTop, nbLeft)


def fromDownLeft(currentBoard, player, stableBoard):
    size = currentBoard.get_board_size()
    nbDown = nbLeft = 0
    for x in range(0, size):
        if boardHelper.getCaseColor(currentBoard, x, size - 1) == player:
            stableBoard.markStable(x, size - 1)
            nbDown += 1
        else:
            break
    for y in range(size - 1, -1, -1):
        if boardHelper.getCaseColor(currentBoard, 0, y) == player:
            stableBoard.markStable(0, y)
            nbLeft += 1
        else:
            break
    return (nbDown, nbLeft)


def fromDownRight(currentBoard, player, stableBoard, down, right):
    size = currentBoard.get_board_size()
    nbDown = nbRight = 0
    if down == False:
        for x in range(size - 1, -1, -1):
            if boardHelper.getCaseColor(currentBoard, x, size - 1) == player:
                stableBoard.markStable(x, size - 1)
                nbDown += 1
            else:
                break
    if right == False:
        for y in range(size - 1, -1, -1):
            if boardHelper.getCaseColor(currentBoard, size - 1, y) == player:
                stableBoard.markStable(size - 1, y)
                nbRight += 1
            else:
                break
    return (nbDown, nbRight)


# make a piece of player as stable is it's in rows that are completely filled in all directions
# start from dimension board size  -1
def markStableCompletelyFilled(currentBoard, player, stableBoard):
    size = currentBoard.get_board_size() - 1
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            if boardHelper.getCaseColor(currentBoard, x, y) == player:
                if testFilled(currentBoard, x, y):
                    stableBoard.markStable(x, y)
                    stableBoard._nbStable += 1


def testFilled(currentBoard, xstart, ystart):
    empty = currentBoard._EMPTY
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        while not boardHelper.isOnCorner(currentBoard, x, y):
            if boardHelper.getCaseColor(currentBoard, x, y) == empty:
                return False
            x += xdirection
            y += ydirection
        if boardHelper.getCaseColor(currentBoard, x, y) == empty:
            return False
    return True


# make a piece of play in which it's surrounded at least in 4 directions consecutive
# start from dimension board size  -1
def markStableSurrondByStable(currentBoard, player, stableBoard):
    size = currentBoard.get_board_size() - 1
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            if stableBoard.isStable(x, y) or boardHelper.getCaseColor(currentBoard, x, y) != player:
                break
            if testSurrondStable(stableBoard, x, y):
                stableBoard.markStable(x, y)
                stableBoard._nbStable += 1


def testSurrondStable(stableBoard, xstart, ystart):
    left = right = top = down = True

    # test right line
    for xdirection, ydirection in [[1, 1], [1, 0], [1, -1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not stableBoard.isStable(x, y):
            right = False
            break

    # test top line
    for xdirection, ydirection in [[1, -1], [0, -1], [-1, -1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not stableBoard.isStable(x, y):
            top = False
            break

    # test left line
    for xdirection, ydirection in [[-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not stableBoard.isStable(x, y):
            left = False
            break

    # test down line
    for xdirection, ydirection in [[-1, 1], [0, 1], [1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not stableBoard.isStable(x, y):
            down = False
            break
    res = False
    # if left line or right line is stable then check upper case and lower case
    if left or right:
        for xdirection, ydirection in [[0, 1], [0, -1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if stableBoard.isStable(x, y):
                res = True
                break

    # if top line or down line is stable then check left case and right case
    if left or right:
        for xdirection, ydirection in [[-1, 0], [1, 0]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if stableBoard.isStable(x, y):
                res = True
                break
    return res