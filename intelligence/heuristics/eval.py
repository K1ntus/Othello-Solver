
import time

from game.board import Reversi
from helpers import boardHelper as boardHelper
from helpers import playerHelper as playerHelper
from intelligence.heuristics import StableStrategy, CornerStrategy
from intelligence.heuristics.BoardWeight import BoardStaticWeight as BoardStaticWeight
import intelligence.heuristics.strategy as strategy
import intelligence.heuristics.CornerStrategy as CornerStrategy
import helpers.boardHelper as boardHelper

from intelligence.heuristics.BoardWeight import BoardStaticWeight

# return the score of all heuristic functions
# every heuristic must return a score between -100 and 100
# eval will also return a score between -100 and 100
# player : the is always myplayer


def getTotal(player, color):
    nbOccupied = player._board._nbWHITE + player._board._nbBLACK
    # mobilityScore = 0
    # mobilityScore = 0
    # parityScore = 0
    discDiffScore = 0
    # staticBoardScore = 0
    # cornerGrabScore = 0
    stabilityScore = 0
    # if nbOccupied <= 20:
    mobilityScore = strategy.mobility(player)
    if nbOccupied>89:
         discDiffScore = strategy.discDiff(player)
    parityScore = strategy.parity(player,color)
    # discDiffScore = strategy.discDiff(player)
    staticBoardScore = strategy.boardWeight(player, color)
    cornerGrabScore = CornerStrategy.cornerGrab(player)
    staticBoardScore = StableStrategy.stability(player, color)




    # stabilityScore = 0


    # early game
    if nbOccupied <= 20:
        return 8 * mobilityScore + 20 * staticBoardScore + 10000 * cornerGrabScore + 10000 * stabilityScore
    # mid game
    elif nbOccupied <= 80:
        return 5 * mobilityScore + 10 * staticBoardScore + 10 * parityScore + 10 * discDiffScore + 10000 * cornerGrabScore + 10000 * stabilityScore
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