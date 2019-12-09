import intelligence.heuristics.stability.StableHeuristic as StableStrategy
import intelligence.heuristics.cornerStrategy.cornerGrab as cornerStrategy
from intelligence.heuristics.BoardWeight import BoardStaticWeight as BoardStaticWeight
from helpers import boardHelper as boardHelper
from helpers import playerHelper as playerHelper


# return the score of all heuristic functions
# every heuristic must return a score between -100 and 100
# eval will also return a score between -100 and 100
def getTotal(player, color):
    stabilityScore = StableStrategy.stability(player, color)
    cornerGrabScore = cornerStrategy.cornerGrab(player)
    staticBoardScore = evalBoard(player._board, player._mycolor)
    total = 1.2*staticBoardScore + 100 * stabilityScore + 397 * cornerGrabScore
#     print("Score:", total)

    return total

def getTotalNegaMAx(player, color):
    stabilityScore = StableStrategy.stabilityNegaMax(player, color)
    cornerGrabScore = cornerStrategy.cornerGrabNegaMax(player,color)
    staticBoardScore = evalBoard(player._board,color)

    total = 1.2*staticBoardScore + 100 * stabilityScore + 397 * cornerGrabScore


    return total

def evalBoard(board, player_color):
    tot = 0
    size = board.get_board_size()
    for x in range(size):
        for y in range(size):
            if boardHelper.getCaseColor(board,x,y) == player_color:
                tot += BoardStaticWeight.weightTable1[y][x]
    return tot
