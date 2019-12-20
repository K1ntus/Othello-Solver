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
    def lazyTest_ValidMove(self, player, xstart, ystart):
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
        self.updatePlayerBB(player,move)
        self._stack.append([move, self._successivePass, toflip])
        self._successivePass = 0
        self._board[x][y] = player
        moveBit=0<<100
        for xf, yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
            #Bitboard flip
            moveBit |= self.convertCordToBit(xf,yf)

        #flip white
        if(player==self._BLACK):
            self._bbW ^= moveBit
            self._bbB |= moveBit
        if(player==self._WHITE):
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
        for xf, yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK -= 1 + len(toflip)
            self._nbWHITE += len(toflip)
        else:
            self._nbWHITE -= 1 + len(toflip)
            self._nbBLACK += len(toflip)

    # Est-ce que on peut au moins jouer un coup ?
    # Note: cette info pourrait être codée plus efficacement
    def at_least_one_legal_move(self, player):
        for x in range(0, self._boardsize):
            for y in range(0, self._boardsize):
                if self.lazyTest_ValidMove(player, x, y):
                    return True
        return False

    # Renvoi la liste des coups possibles
    # Note: cette méthode pourrait être codée plus efficacement
    def legal_moves(self):
        moves = []
        for x in range(0, self._boardsize):
            for y in range(0, self._boardsize):
                if self.lazyTest_ValidMove(self._nextPlayer, x, y):
                    moves.append([self._nextPlayer, x, y])
        if len(moves) is 0:
            moves = [[self._nextPlayer, -1, -1]]  # We shall pass
        return moves

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

    def legal_moves_bit(self):
        if self._nextPlayer == self._BLACK:
            bitP = self._bbB
            bitO = self._bbW
        else:
            bitO = self._bbB
            bitP = self._bbW
        moves = 0
        canN = bitO & self.sheftN(bitP)
        while canN != 0:
            moves |= self._empty & self.sheftN(canN)
            canN = bitO & self.sheftN(canN)

        canS = bitO & self.sheftS(bitP)
        while canS != 0:
            moves |= self._empty & self.sheftS(canS)
            canS = bitO & self.sheftS(canS)

        canE = bitO & self.sheftE(bitP)
        while canE != 0:
            moves |= self._empty & self.sheftE(canE)
            canE = bitO & self.sheftE(canE)

        canW = bitO & self.sheftW(bitP)
        while canW != 0:
            moves |= self._empty & self.sheftW(canW)
            canW = bitO & self.sheftW(canW)

        canNE = bitO & self.sheftNE(bitP)
        while canNE != 0:
            moves |= self._empty & self.sheftNE(canNE)
            canNE = bitO & self.sheftNE(canNE)

        canNW = bitO & self.sheftNW(bitP)
        while canNW != 0:
            moves |= self._empty & self.sheftNW(canNW)
            canNW = bitO & self.sheftNW(canNW)

        canSE = bitO & self.sheftSE(bitP)
        while canSE != 0:
            moves |= self._empty & self.sheftSE(canSE)
            canSE = bitO & self.sheftSE(canSE)

        canSW = bitO & self.sheftSW(bitP)
        while canSW != 0:
            moves |= self._empty & self.sheftSW(canSW)
            canSW = bitO & self.sheftSW(canSW)

        arr = []
        for i in range(100, 1, -1):
            j = i - 1
            # if ((moves >> j) & 1) > 0:
            if (moves & (1<< j) ) > 0:
                k = 100- j
                x = k//10
                y = k%10 -1
                if y>=0 and x>=0 :
                    arr.append([self._nextPlayer, x, y])
        return arr
    def generateMoves(self):
        if self._nextPlayer == self._BLACK:
            bitP = self._bbB
            bitO = self._bbW
        else:
            bitO = self._bbB
            bitP = self._bbW
        moves = 0
        open = ~(bitP | bitO)
        captured = 0
        #NORTH
        captured = self.sheftN(bitP) & bitO
        for i in range(7):
            captured |= self.sheftN(captured) & bitO

        moves |= self.sheftN(captured) & open

        #SOUTH
        captured = self.sheftS(bitP) & bitO
        for i in range(7):
            captured |= self.sheftS(captured) & bitO

        moves |= self.sheftS(captured) & open

        #WEST
        captured = self.sheftW(bitP) & bitO
        for i in range(7):
            captured |= self.sheftW(captured) & bitO

        moves |= self.sheftW(captured) & open

        #EAST
        captured = self.sheftE(bitP) & bitO
        for i in range(7):
            captured |= self.sheftE(captured) & bitO

        moves |= self.sheftE(captured) & open


        #NORTHWEST
        captured = self.sheftNW(bitP) & bitO
        for i in range(7):
            captured |= self.sheftNW(captured) & bitO

        moves |= self.sheftNW(captured) & open

        #NORTHEAST
        captured = self.sheftNE(bitP) & bitO
        for i in range(7):
            captured |= self.sheftNE(captured) & bitO

        moves |= self.sheftNE(captured) & open

        #SOUTHWEST
        captured = self.sheftSW(bitP) & bitO
        for i in range(7):
            captured |= self.sheftSW(captured) & bitO

        moves |= self.sheftSW(captured) & open

        #SOUTHEAST
        captured = self.sheftSE(bitP) & bitO
        for i in range(7):
            captured |= self.sheftSE(captured) & bitO

        moves |= self.sheftSE(captured) & open

        arr = []
        for i in range(99,-1,-1):

            # if ((moves >> j) & 1) > 0:
            if (moves & (1 << i)) > 0:
                k = 100 - i
                x = k // 10
                y = k % 10 - 1
                # if y >= 0 and x >= 0:
                if y==-1 :
                    y=9
                    x=x-1
                arr.append([self._nextPlayer, x, y])
        return arr


    def convertCordToBit(self, x, y):
        shift = x * 10 + y +1
        return 1 << (100-shift)


    def updatePlayerBB(self,color,move):

        bitMove = self.convertCordToBit(move[1],move[2])
        if color==self._BLACK:
            self._bbB = self._bbB | bitMove
            # self._bbW = self._bbW ^ bitMove
        elif color ==self._WHITE:
            self._bbW = self._bbW |bitMove
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

    def sheftN(self,bit):
        return  bit<<10
    def sheftS(self,bit):
        return bit>>10
    def sheftE(self,bit):
        return (bit & self._maskE)>>1
        # return bit>>1
    def sheftW(self,bit):
        return (bit & self._maskW)<<1
        # return bit <<1
    def sheftNE(self,bit):
        return self.sheftN(self.sheftE(bit))
    def sheftNW(self,bit):
        return self.sheftN(self.sheftW(bit))
    def sheftSE(self,bit):
        return self.sheftS(self.sheftE(bit))
    def sheftSW(self,bit):
        return self.sheftS(self.sheftW(bit))