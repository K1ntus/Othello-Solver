class StableBoard:
    _STABLE = 1
    _NotSTABLE = 0


    # Attention, la taille du plateau est donnée en paramètre
    def __init__(self, boardsize=8):
        self._boardsize = boardsize
        self._board = []
        self._nbStable=0
        for x in range(self._boardsize):
            self._board.append([self._NotSTABLE] * self._boardsize)

    def markStable(self, x, y):
        self._board[x][y] = self._STABLE

    def isStable(self, x, y):
        return self._board[x][y] == self._STABLE