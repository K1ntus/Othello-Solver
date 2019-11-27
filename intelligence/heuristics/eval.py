
import intelligence.heuristics.stability.StableHeuristic as StableStrategy
import intelligence.heuristics.cornerStrategy.cornerGrab as cornerStrategy


# return the score of all heuristic functions
# every heuristic must return a score between -100 and 100
# eval will also return a score between -100 and 100
def getTotal(player, color):
    stabilityScore = StableStrategy.stability(player, color)
    cornerGrabScore = cornerStrategy.cornerGrab(player)

    total = 1.7 * stabilityScore + 2 * cornerGrabScore

    return total