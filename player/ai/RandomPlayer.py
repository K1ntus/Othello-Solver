# -*- coding: utf-8 -*-

import time
from game.board import Reversi
from player.playerInterface import *
from random import randint

"""
just a simple AI that is returning a random move over all the available
"""
class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = [m for m in self._board.legal_moves()]
        move = moves[randint(0,len(moves)-1)]
        self._board.push(move)
        # print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
#         print("My current board :")
#         print(self._board)
        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
#         print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



