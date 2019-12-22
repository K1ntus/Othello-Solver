
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper
#  ------------------------------ Corner Grab ---------------------------------#

# measures the disc on the corner for player
def cornerGrab(player,color):
    myNbcorner = 0
    opNbcorner = 0
    op_color = playerHelper.getOpColor(color)
    size = player._board.get_board_size()-1
    cornerList = [[0, size], [size, size], [size, 0], [0, 0]]

    for c in cornerList:
        if boardHelper.getCaseColor(player._board,c[0],c[1]) ==color:
            myNbcorner += 1
        if boardHelper.getCaseColor(player._board,c[0],c[1]) ==op_color:
            opNbcorner += 1

    return 100 *(myNbcorner - opNbcorner) /(myNbcorner + opNbcorner + 1)


