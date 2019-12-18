import time

from game.board import Reversi
from helpers import boardHelper as boardHelper
from helpers import playerHelper as playerHelper
from intelligence.heuristics import StableStrategy, CornerStrategy
from intelligence.heuristics.BoardWeight import BoardStaticWeight as BoardStaticWeight
import intelligence.heuristics.strategy as strategy


# return the score of all heuristic functions
# every heuristic must return a score between -100 and 100
# eval will also return a score between -100 and 100

# player : the is always myplayer
def getTotal(player, color):
    mobilityScore = strategy.mobility(player)
    parityScore = strategy.parity(player)
    discDiffScore = strategy.discDiff(player)
    staticBoardScore = strategy.boardWeight(player._board, player._mycolor)
    cornerGrabScore = CornerStrategy.cornerGrab(player)
    stabilityScore = StableStrategy.stability(player, color)
    
    
    stabilityScore = 0
    parityScore = 0
    discDiffScore = 0

    nbOccupied = player._board._nbWHITE + player._board._nbBLACK
    # early game
    if nbOccupied <= 31:
        return 5 * mobilityScore + 20 * staticBoardScore + 10000 * cornerGrabScore + 10000 * stabilityScore
    # mid game
    elif nbOccupied <= 89:
        return 2 * mobilityScore + 10 * staticBoardScore + 10 * parityScore + 10 * discDiffScore + 10000 * cornerGrabScore + 10000 * stabilityScore
    # late gme
    else:
        return 500 * parityScore + 500 * discDiffScore + 10000 * cornerGrabScore + 10000 * stabilityScore
