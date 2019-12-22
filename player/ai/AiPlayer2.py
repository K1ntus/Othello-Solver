# -*- coding: utf-8 -*-

import time
from game.board import ReversiBit
from player.playerInterface import *
from random import randint

import intelligence.heuristics.eval as eval
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper

'''AI Implementing a Negamax ABS'''
class myPlayer(PlayerInterface):
    _NotSTABLE=0
    _STABLE=1
    def __init__(self):
        self._board = ReversiBit.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = [m for m in self._board.legal_moves()]
        print("legal moves ----------------------------")
        print(self._board.old_legal_moves())
        print("BIT legal moves")
        print(self._board.legal_moves())
        # print(self._board)
        # self._board.bbPrint()
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
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



