# -*- coding: utf-8 -*-

''' Fichier de règles du Reversi pour le tournoi Masters Info 2019 en IA.
    Certaines parties de ce code sont fortement inspirée de 
    https://inventwithpython.com/chapter15.html

    '''


class Board:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0
    _maskE = 0b1111111110111111111011111111101111111110111111111011111111101111111110111111111011111111101111111110
    _maskW = 0b0111111111011111111101111111110111111111011111111101111111110111111111011111111101111111110111111111

    # Attention, la taille du plateau est donnée en paramètre
    def __init__(self, boardsize=8):
        self._nbWHITE = 2
        self._nbBLACK = 2
        self._nextPlayer = self._BLACK
        self._boardsize = boardsize
        self._board = []
        for x in range(self._boardsize):
            self._board.append([self._EMPTY] * self._boardsize)
        _middle = int(self._boardsize / 2)
        self._board[_middle - 1][_middle - 1] = self._BLACK
        self._board[_middle - 1][_middle] = self._WHITE
        self._board[_middle][_middle - 1] = self._WHITE
        self._board[_middle][_middle] = self._BLACK

        self._stack = []
        self._successivePass = 0

        self._bbW = (1 << 45) | (1 << 54)
        self._bbB = (1 << 44) | (1 << 55)
        self._empty = ~(self._bbB & self._bbW)

    def reset(self):
        self.__init__()

    # Donne la taille du plateau 
    def get_board_size(self):
        return self._boardsize

    # Donne le nombre de pieces de blanc et noir sur le plateau
    # sous forme de tuple (blancs, noirs) 
    # Peut être utilisé si le jeu est terminé pour déterminer le vainqueur
    def get_nb_pieces(self):
        return (self._nbWHITE, self._nbBLACK)

    # Vérifie si player a le droit de jouer en (x,y)
    def is_valid_move(self, player, x, y):
        if x == -1 and y == -1:
            return not self.at_least_one_legal_move(player)
        return self.lazyTest_ValidMove(player, x, y)

    def _isOnBoard(self, x, y):
        return x >= 0 and x < self._boardsize and y >= 0 and y < self._boardsize

    # Renvoie la liste des pieces a retourner si le coup est valide
    # Sinon renvoie False
    # Ce code est très fortement inspiré de https://inventwithpython.com/chapter15.html
    # y faire référence dans tous les cas
    def testAndBuild_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False

        self._board[xstart][ystart] = player  # On pourra remettre _EMPTY ensuite

        otherPlayer = self._flip(player)

        tilesToFlip = []  # Si au moins un coup est valide, on collecte ici toutes les pieces a retourner
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y):  # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y):
                    continue
                if self._board[x][y] == player:  # We are sure we can at least build this move. Let's collect
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        self._board[xstart][ystart] = self._EMPTY  # restore the empty space
        if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    # Pareil que ci-dessus mais ne revoie que vrai / faux (permet de tester plus rapidement)
    # Bitboard Version
    def lazyTest_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False

        move = self.convertCordToBit(xstart, ystart)
        if player == self._BLACK:
            bitP = self._bbB
            bitO = self._bbW
        elif player == self._WHITE:
            bitP = self._bbW
            bitO = self._bbB

        # EAST
        captured = self.shiftE(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftE(captured)
        if captured & bitP > 0 and count != 0:
            return True

        # SOUTHWEST
        captured = self.shiftSW(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftSW(captured)
        if captured & bitP > 0 and count != 0:
            return True
        # SOUTH
        captured = self.shiftS(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftS(captured)
        if captured & bitP > 0 and count != 0:
            return True

        # SOUTHEAST
        captured = self.shiftSE(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftSE(captured)
        if captured & bitP > 0 and count != 0:
            return True

        # WEST
        captured = self.shiftW(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftW(captured)
        if captured & bitP > 0 and count != 0:
            return True

        # NORTHEAST
        captured = self.shiftNE(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftNE(captured)
        if captured & bitP > 0 and count != 0:
            return True

        # NORTH
        captured = self.shiftN(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftN(captured)
        if captured & bitP > 0 and count != 0:
            return True

        # NORTHWEST
        captured = self.shiftNW(move)
        count = 0
        while captured & bitO > 0:
            count += 1
            captured = self.shiftNW(captured)
        if captured & bitP > 0 and count != 0:
            return True

        return False

    def _flip(self, player):
        if player == self._BLACK:
            return self._WHITE
        return self._BLACK

    def is_game_over(self):
        if self.at_least_one_legal_move(self._nextPlayer):
            return False
        if self.at_least_one_legal_move(self._flip(self._nextPlayer)):
            return False

        return True

    def push(self, move):
        [player, x, y] = move
        assert player == self._nextPlayer
        if x == -1 and y == -1:  # pass
            self._nextPlayer = self._flip(player)
            self._stack.append([move, self._successivePass, []])
            self._successivePass += 1
            return
        toflip = self.testAndBuild_ValidMove(player, x, y)
        # print(toflip)

        # update bitboard
        self.updatePlayerBB(player, move)

        self._stack.append([move, self._successivePass, toflip])
        self._successivePass = 0
        self._board[x][y] = player

        # flipping
        moveBit = 0 << 100
        for xf, yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
            # Bitboard flip
            moveBit |= self.convertCordToBit(xf, yf)
        # flip opponent
        if (player == self._BLACK):
            self._bbW ^= moveBit
            self._bbB |= moveBit
        if (player == self._WHITE):
            self._bbB ^= moveBit
            self._bbW |= moveBit

        if player == self._BLACK:
            self._nbBLACK += 1 + len(toflip)
            self._nbWHITE -= len(toflip)
            self._nextPlayer = self._WHITE
        else:
            self._nbWHITE += 1 + len(toflip)
            self._nbBLACK -= len(toflip)
            self._nextPlayer = self._BLACK

    def pop(self):
        [move, self._successivePass, toflip] = self._stack.pop()
        [player, x, y] = move
        self._nextPlayer = player
        if len(toflip) == 0:  # pass
            assert x == -1 and y == -1
            return
        self._board[x][y] = self._EMPTY
        # flipping
        # update bitboard
        self.undoPlayerMove(player,move)

        moveBit = 0 << 100
        for xf, yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
            # Bitboard flip
            moveBit |= self.convertCordToBit(xf, yf)

        # flip myPlayer
        if (player == self._BLACK):
            self._bbB ^= moveBit
            self._bbW |= moveBit
        if (player == self._WHITE):
            self._bbW ^= moveBit
            self._bbB |= moveBit

        if player == self._BLACK:
            self._nbBLACK -= 1 + len(toflip)
            self._nbWHITE += len(toflip)
        else:
            self._nbWHITE -= 1 + len(toflip)
            self._nbBLACK += len(toflip)

    # Est-ce que on peut au moins jouer un coup ?
    # Note: this is bitboard version
    def at_least_one_legal_move(self, player):
        for x in range(0, self._boardsize):
            for y in range(0, self._boardsize):
                if self.lazyTest_ValidMove(player, x, y):
                    return True
        return False

    # Renvoi la liste des coups possibles
    # Note: bitboard version
    def legal_moves(self):
        if self._nextPlayer == self._BLACK:
            bitP = self._bbB
            bitO = self._bbW
        else:
            bitO = self._bbB
            bitP = self._bbW
        moves = 0
        open = ~(bitP | bitO)
        captured = 0
        # NORTH
        captured = self.shiftN(bitP) & bitO
        for i in range(7):
            captured |= self.shiftN(captured) & bitO

        moves |= self.shiftN(captured) & open

        # SOUTH
        captured = self.shiftS(bitP) & bitO
        for i in range(7):
            captured |= self.shiftS(captured) & bitO

        moves |= self.shiftS(captured) & open

        # WEST
        captured = self.shiftW(bitP) & bitO
        for i in range(7):
            captured |= self.shiftW(captured) & bitO

        moves |= self.shiftW(captured) & open

        # EAST
        captured = self.shiftE(bitP) & bitO
        for i in range(7):
            captured |= self.shiftE(captured) & bitO

        moves |= self.shiftE(captured) & open

        # NORTHWEST
        captured = self.shiftNW(bitP) & bitO
        for i in range(7):
            captured |= self.shiftNW(captured) & bitO

        moves |= self.shiftNW(captured) & open

        # NORTHEAST
        captured = self.shiftNE(bitP) & bitO
        for i in range(7):
            captured |= self.shiftNE(captured) & bitO

        moves |= self.shiftNE(captured) & open

        # SOUTHWEST
        captured = self.shiftSW(bitP) & bitO
        for i in range(7):
            captured |= self.shiftSW(captured) & bitO

        moves |= self.shiftSW(captured) & open

        # SOUTHEAST
        captured = self.shiftSE(bitP) & bitO
        for i in range(7):
            captured |= self.shiftSE(captured) & bitO

        moves |= self.shiftSE(captured) & open

        arr = []
        for i in range(99, -1, -1):

            # if ((moves >> j) & 1) > 0:
            if (moves & (1 << i)) > 0:
                k = 100 - i
                x = k // 10
                y = k % 10 - 1
                # if y >= 0 and x >= 0:
                if y == -1:
                    y = 9
                    x = x - 1
                arr.append([self._nextPlayer, x, y])
        if len(arr) is 0:
            return [[self._nextPlayer, -1, -1]]
        return arr

    # Exemple d'heuristique tres simple : compte simplement les pieces
    def heuristique(self, player=None):
        if player is None:
            player = self._nextPlayer
        if player is self._WHITE:
            return self._nbWHITE - self._nbBLACK
        return self._nbBLACK - self._nbWHITE

    def _piece2str(self, c):
        if c == self._WHITE:
            return 'O'
        elif c == self._BLACK:
            return 'X'
        else:
            return '.'

    def bbPrint(self):
        sb = ""
        for i in range(100, 0, -1):
            j = i - 1
            if ((self._bbB >> j) & 1 > 0):
                sb = sb + "B "
            elif ((self._bbW >> j) & 1):
                sb = sb + "W "
            else:
                sb = sb + "- "
            if j % 10 == 0:
                print(sb)
                sb = ""

    def convertCordToBit(self, x, y):
        shift = x * 10 + y + 1
        return 1 << (100 - shift)

    def convertBitBoardtoCordArr(self, bitBoard):
        arr = []
        for i in range(99, -1, -1):
            if (bitBoard & (1 << i)) > 0:
                k = 100 - i
                x = k // 10
                y = k % 10 - 1
                if y == -1:
                    y = 9
                    x = x - 1
                arr.append([x, y])
        return arr

    def updatePlayerBB(self, color, move):

        bitMove = self.convertCordToBit(move[1], move[2])
        if color == self._BLACK:
            self._bbB = self._bbB | bitMove
            # self._bbW = self._bbW ^ bitMove
        elif color == self._WHITE:
            self._bbW = self._bbW | bitMove
            # self._bbB = self._bbB ^ bitMove
        self._empty = ~(self._bbB | self._bbW)

    def undoPlayerMove(self,color,move):
        bitMove = ~self.convertCordToBit(move[1], move[2])
        if color == self._BLACK:
            self._bbB = self._bbB & bitMove
            # self._bbW = self._bbW ^ bitMove
        elif color == self._WHITE:
            self._bbW = self._bbW & bitMove
            # self._bbB = self._bbB ^ bitMove
        self._empty = ~(self._bbB | self._bbW)


    def __str__(self):
        toreturn = "ABCDEFGHIJ\n"
        for l in self._board:
            for c in l:
                toreturn += self._piece2str(c)
            toreturn += "\n"
        toreturn += "ABCDEFGHIJ\n"
        toreturn += "Next player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + "\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        toreturn += "(successive pass: " + str(self._successivePass) + " )"
        return toreturn

    __repr__ = __str__

    def shiftN(self, bit):
        return bit << 10

    def shiftS(self, bit):
        return bit >> 10

    def shiftE(self, bit):
        return (bit & self._maskE) >> 1
        # return bit>>1

    def shiftW(self, bit):
        return (bit & self._maskW) << 1
        # return bit <<1

    def shiftNE(self, bit):
        return self.shiftN(self.shiftE(bit))

    def shiftNW(self, bit):
        return self.shiftN(self.shiftW(bit))

    def shiftSE(self, bit):
        return self.shiftS(self.shiftE(bit))

    def shiftSW(self, bit):
        return self.shiftS(self.shiftW(bit))

    def old_legal_moves(self):
        moves = []
        for x in range(0, self._boardsize):
            for y in range(0, self._boardsize):
                if self.old_lazyTest_ValidMove(self._nextPlayer, x, y):
                    moves.append([self._nextPlayer, x, y])
        if len(moves) is 0:
            moves = [[self._nextPlayer, -1, -1]]  # We shall pass
        return moves

    def old_at_least_one_legal_move(self, player):
        for x in range(0, self._boardsize):
            for y in range(0, self._boardsize):
                if self.old_lazyTest_ValidMove(player, x, y):
                    return True
        return False

    def old_lazyTest_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False

        self._board[xstart][ystart] = player  # On pourra remettre _EMPTY ensuite

        otherPlayer = self._flip(player)

        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y):  # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y):  # On a au moins
                    continue
                if self._board[x][y] == player:  # We are sure we can at least build this move.
                    self._board[xstart][ystart] = self._EMPTY
                    return True

        self._board[xstart][ystart] = self._EMPTY  # restore the empty space
        return False
    # actually slower than normal one wtf?
    # return an array of (x,y)
    # def testAndBuild_ValidMove(self, player, xstart, ystart):
    #     if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
    #         return False
    #
    #     move = self.convertCordToBit(xstart, ystart)
    #     if player == self._BLACK:
    #         bitP = self._bbB
    #         bitO = self._bbW
    #     elif player == self._WHITE:
    #         bitP = self._bbW
    #         bitO = self._bbB
    #
    #     tiles = 0
    #
    #     # EAST
    #     captured = self.shiftE(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftE(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #
    #     # SOUTHWEST
    #     captured = self.shiftSW(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftSW(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #
    #     # SOUTH
    #     captured = self.shiftS(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftS(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #
    #     # SOUTHEAST
    #     captured = self.shiftSE(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftSE(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #
    #     # WEST
    #     captured = self.shiftW(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftW(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #
    #     # NORTHEAST
    #     captured = self.shiftNE(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftNE(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #
    #     # NORTH
    #     captured = self.shiftN(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftN(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #
    #     # NORTHWEST
    #     captured = self.shiftNW(move)
    #     tmp = 0
    #     while captured & bitO > 0:
    #         tmp |= captured & bitO
    #         captured = self.shiftNW(captured)
    #     if captured & bitP > 0:
    #         tiles |= tmp
    #     tilesToFlip = self.convertBitBoardtoCordArr(tiles)
    #     if len(tilesToFlip) is 0:
    #         return False
    #     return tilesToFlip
