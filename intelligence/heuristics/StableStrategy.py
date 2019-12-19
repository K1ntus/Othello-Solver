
from threading import Thread

import helpers.boardHelper as boardHelper
import helpers.playerHelper as playerHelper
import copy

#  ------------------------------ Stability -----------------------------------#
class StableThread(Thread):
    def __init__(self, player, color):
        Thread.__init__(self)
        self._nbStable = 0
        self._player = player
        self._color = color
        # Can setup other things before the thread starts

    def run(self):
        self._nbStable = stabilityForPlayer(self._player, self._color)


def stability(player, color):
    if (player._board._nbBLACK + player._board._nbWHITE) < 12:
        return 0
    my_color = color
    # TODO to be update
    op_color = boardHelper.getOpColor(my_color)
    myStable = 20 * stabilityForPlayer(player, my_color)
    opStable = 20 * stabilityForPlayer(player, op_color)

    return myStable - opStable



def stabilityThread(player, color):
    if (player._board._nbBLACK + player._board._nbWHITE) < 12:
        return 0
    op = boardHelper.getOpColor(color)

    # use thread
    player_thread = StableThread(player, color)
    op_thread = StableThread(player, op)
    player_thread.start()
    op_thread.start()

    player_thread.join()
    op_thread.join()

    myStable = 20 * player_thread._nbStable
    opStable = 20 * op_thread._nbStable

    if (myStable + opStable) != 0:
        return 100 * (myStable - opStable) / (myStable + opStable)
    else:
        return 0


# stability score for player
# player act just like color
def stabilityForPlayer(player, color):
    left = right = top = down = False
    currentBoard = player._board
    stableBoard = set()
    nbStable = 0

    (nbTop, nbRight) = fromTopRight(player, color, stableBoard)
    if nbTop == currentBoard.get_board_size() or nbTop == 0:
        top = True
    if nbRight == currentBoard.get_board_size() or nbRight == 0:
        right = True
    (nbDown, nbLeft) = fromDownLeft(player, color, stableBoard)
    if nbDown == currentBoard.get_board_size() or nbDown == 0:
        down = True
    if nbLeft == currentBoard.get_board_size() or nbLeft == 0:
        left = True

    (restNbTop, restNbLeft) = fromTopLeft(player, color, stableBoard, top, left)
    (restNbDown, restNbRight) = fromDownRight(player, color, stableBoard, down, right)
    nbStable += (nbTop + nbRight + nbDown + nbLeft + restNbTop + restNbDown + restNbRight + restNbLeft)

    nbStableCompletelyFilled = markStableCompletelyFilled(player, color, stableBoard)
    nbStableSurround = markStableSurroundByStable(player, color, stableBoard)
    nbStable += (nbStableCompletelyFilled + nbStableSurround)
    return nbStable


def fromTopRight(player, color, stableBoard):
    currentBoard = player._board
    size = currentBoard.get_board_size() - 1
    nbTop = 0
    nbRight = 0
    # check horizontal
    for y in range(size, -1, -1):
        if boardHelper.getCaseColor(currentBoard, 0, y) == color:
            playerHelper.markStable(stableBoard, 0, y)
            nbTop += 1
        else:
            break
    # check vertical
    for x in range(0, size + 1):
        if boardHelper.getCaseColor(currentBoard, x, size) == color:
            playerHelper.markStable(stableBoard, x, size)
            nbRight += 1
        else:
            break
    return (nbTop, nbRight)


def fromTopLeft(player, color, stableBoard, top, left):
    currentBoard = player._board
    size = currentBoard.get_board_size()
    nbTop = nbLeft = 0
    if not top:
        for y in range(0, size):
            if boardHelper.getCaseColor(currentBoard, 0, y) == color:
                playerHelper.markStable(stableBoard, 0, y)
                nbTop += 1
            else:
                break
    if not left:
        for x in range(0, size):
            if boardHelper.getCaseColor(currentBoard, x, 0) == color:
                playerHelper.markStable(stableBoard, x, 0)
                nbLeft += 1
            else:
                break
    return (nbTop, nbLeft)


def fromDownLeft(player, color, stableBoard):
    currentBoard = player._board
    size = currentBoard.get_board_size()
    nbDown = nbLeft = 0
    for y in range(0, size):
        if boardHelper.getCaseColor(currentBoard, size - 1, y) == color:
            playerHelper.markStable(stableBoard, size - 1, y)
            nbDown += 1
        else:
            break
    for x in range(size - 1, -1, -1):
        if boardHelper.getCaseColor(currentBoard, x, 0) == color:
            playerHelper.markStable(stableBoard, x, 0)
            nbLeft += 1
        else:
            break
    return (nbDown, nbLeft)


def fromDownRight(player, color, stableBoard, down, right):
    currentBoard = player._board
    size = currentBoard.get_board_size()
    nbDown = nbRight = 0
    if not down:
        for y in range(size - 1, -1, -1):
            if boardHelper.getCaseColor(currentBoard, size - 1, y) == color:
                playerHelper.markStable(stableBoard, size - 1, y)
                nbDown += 1
            else:
                break
    if not right:
        for x in range(size - 1, -1, -1):
            if boardHelper.getCaseColor(currentBoard, x, size - 1) == color:
                playerHelper.markStable(stableBoard, x, size - 1)
                nbRight += 1
            else:
                break
    return (nbDown, nbRight)


# make a piece of player as stable is it's in rows that are completely filled in all directions
# start from dimension board size  -1
def markStableCompletelyFilled(player, color, stableBoard):
    currentBoard = player._board
    size = currentBoard.get_board_size() - 1
    nbStable = 0
    for x in range(1, size):
        for y in range(1, size):
            if not playerHelper.isStable(stableBoard, x, y) and boardHelper.getCaseColor(currentBoard, x, y) == color:
                if testFilled(currentBoard, stableBoard, x, y):
                    playerHelper.markStable(stableBoard, x, y)
                    nbStable += 1
    return nbStable


def testFilled(currentBoard, stableBoard, xstart, ystart):
    empty = currentBoard._EMPTY
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        while not boardHelper.isOnFrontier(currentBoard, x, y):
            # break and change direction
            if playerHelper.isStable(stableBoard, x, y):
                break
            if boardHelper.getCaseColor(currentBoard, x, y) == empty:
                return False
            x += xdirection
            y += ydirection
        if boardHelper.getCaseColor(currentBoard, x, y) == empty:
            return False
    return True


# make a piece of play in which it's surrounded at least in 4 directions consecutive
# start from dimension board size  -1
def markStableSurroundByStable(player, color, stableBoard):
    currentBoard = player._board
    size = currentBoard.get_board_size() - 1
    nbStable = 0
    for x in range(1, size):
        for y in range(1, size):
            if playerHelper.isStable(stableBoard, x, y) or boardHelper.getCaseColor(currentBoard, x, y) != color:
                continue
            if testSurrondStable(stableBoard, x, y):
                playerHelper.markStable(stableBoard, x, y)
                nbStable += 1
    return nbStable


def testSurrondStable(stableBoard, xstart, ystart):
    left = right = top = down = True

    # test right line
    for xdirection, ydirection in [[1, 1], [0, 1], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not playerHelper.isStable(stableBoard, x, y):
            right = False
            break

    # test top line
    for xdirection, ydirection in [[-1, 1], [-1, 0], [-1, -1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not playerHelper.isStable(stableBoard, x, y):
            top = False
            break

    # test left line
    for xdirection, ydirection in [[-1, -1], [0, -1], [1, -1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not playerHelper.isStable(stableBoard, x, y):
            left = False
            break

    # test down line
    for xdirection, ydirection in [[1, -1], [1, 0], [1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if not playerHelper.isStable(stableBoard, x, y):
            down = False
            break
    res1 = res2 = False
    # if left line or right line is stable then check upper case and lower case
    if left or right:
        for xdirection, ydirection in [[-1, 0], [1, 0]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if playerHelper.isStable(stableBoard, x, y):
                res1 = True
                break

    # if top line or down line is stable then check left case and right case
    if top or down:
        for xdirection, ydirection in [[0, -1], [0, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if playerHelper.isStable(stableBoard, x, y):
                res2 = True
                break
    return res1 or res2
