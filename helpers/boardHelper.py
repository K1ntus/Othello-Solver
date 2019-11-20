def get_nb_legal_moves(board, player):
    moves = 0
    for x in range(0, board.get_board_size()):
        for y in range(0, board.get_board_size()):
            if board.lazyTest_ValidMove(player, x, y):
                moves += 1
    return moves
