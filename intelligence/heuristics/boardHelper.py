def getCaseColor(board, x, y):
    return board._board[x][y]


def isOnCorner(board, x, y):
    size = board.get_board_size()
    if x >= 0 and x < size and (y == 0 or y == size - 1):
        return True
    if y >= 0 and y < size and (x == 0 or x == size - 1):
        return True