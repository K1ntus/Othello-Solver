import intelligence.heuristics.stability.StableHeuristic as StableStrategy
import intelligence.heuristics.cornerStrategy.cornerGrab as cornerStrategy
import intelligence.heuristics.strategy as strategy
import helpers.boardHelper as boardHelper

from intelligence.heuristics.BoardWeight import BoardStaticWeight

# return the score of all heuristic functions
# every heuristic must return a score between -100 and 100
# eval will also return a score between -100 and 100

# player : the is always myplayer


def getTotal(player, color):
    mobilityScore = strategy.mobility(player)
    parityScore = strategy.parity(player)
    discDiffScore = strategy.discDiff(player)
    staticBoardScore = strategy.boardWeight(player, color)
    cornerGrabScore = cornerStrategy.cornerGrab(player)

    # stabilityScore = StableStrategy.stability(player, color)
    stabilityScore = 0



    nbOccupied = player._board._nbWHITE + player._board._nbBLACK
    # early game
    if nbOccupied <= 31:
        return 5 * mobilityScore + 20 * staticBoardScore + 10000 * cornerGrabScore + 10000 * stabilityScore
    # mid game
    if nbOccupied <= 89:
        return 2 * mobilityScore + 10 * staticBoardScore + 10 * parityScore + 10 * discDiffScore + 10000 * cornerGrabScore + 10000 * stabilityScore
    # late gme
    else:
        return 500 * parityScore + 500 * discDiffScore + 10000 * cornerGrabScore + 10000 * stabilityScore


def evalBoard(board, player_color):
    tot = 0
    size = board.get_board_size()
    for x in range(size):
        for y in range(size):
            if boardHelper.getCaseColor(board,x,y) == player_color:
                tot += BoardStaticWeight.weightTable1[y][x]
    return tot