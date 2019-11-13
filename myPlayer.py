# -*- coding: utf-8 -*-


# The MAIN AI TO DEVELOP

import time
import Reversi
from random import randint
from playerInterface import *

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
#         moves = [m for m in self._board.legal_moves()]
#         move = moves[randint(0,len(moves)-1)]
        print("AAA", flush=True)
        (value, move) = self.MaxAlphaBeta(-10, 10)
        self._board.push(move)
        print("I am playing ", move)
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



#begin         game = 
#middle        game = minimax
#middle+end    game = alphabeta



    def getNumberPoints(self, move):
        (current_point_white, current_point_black) = self._board.get_nb_pieces()
        self._board.push(move)
        (new_point_white, new_point_black) = self._board.get_nb_pieces()
        
        if(self._mycolor == 1): #black
            return new_point_black-current_point_black
        else:
            return new_point_white-current_point_white

#https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
    def MaxAlphaBeta(self, alpha, beta):
        # 10  : win
        # 0   : draw
        # -10 : lose
        maxValue = -10
        move = None
        
        for m in self._board.legal_moves():
            print("Alpha:",alpha, flush=True)
            print("Beta:",beta, flush=True)
            self._board.push(m)
            
            (m, move) = self.MinAlphaBeta(alpha, beta)
            if(m > maxValue):
                maxValue = self.getNumberPoints(m)
                move = m
                
            self._board.pop()
            
            
            if (maxValue >= beta):
                return (maxValue, move)
            
            if(maxValue > alpha):
                alpha = maxValue
        return (maxValue, move)


    def MinAlphaBeta(self, alpha, beta):
        print("TODO")
        # 10  : win
        # 0   : draw
        # -10 : lose
        minValue = 10
        move = None
        
        for m in self._board.legal_moves():
            print("Alpha:",alpha)
            print("Beta:",beta)
            time.sleep(0.5)
            self._board.push(m)
            (m, move) = self.MaxAlphaBeta(alpha, beta)
            if(m > minValue):
                maxValue = self.getNumberPoints(m)
                move = m
            self._board.pop()
            
            
            if (minValue <= alpha):
                return (maxValue, move)
            
            if(minValue < beta):
                beta = minValue
        return (maxValue, move)









