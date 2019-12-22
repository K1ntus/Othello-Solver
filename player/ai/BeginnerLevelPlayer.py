# -*- coding: utf-8 -*-

import time
from game.board import Reversi
from player.playerInterface import *
from random import randint
from asyncio.tasks import sleep
from intelligence.heuristics import evaluator

WIDTH = 9
HEIGHT = 9

class myPlayer(PlayerInterface):
    '''
    Simple AI player that returns the move with will flip the most
    higher number of token
    '''

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Simple player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = [m for m in self._board.legal_moves()]
#         print("Available move: ", moves)
#         time.sleep(1)
#         move = moves[randint(0,len(moves)-1)]
        move = None
        if(len(moves) < 5):
            move = moves[randint(0,len(moves)-1)]
        else:
            (move, poids) = self.getBestMoveDependOfNumberPoint(moves)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
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
            

        
    
    def calculation(self):
        print("TODO")
#         localGame Beginning
#         Mid-localGame
#         localGame End

    def applyBiais(self, move):
        return 0
        
        
    def getNumberPoints(self, move, nbmove):
        self._board.push(move)
        score = evaluator.getHeuristicValue(self, nbmove)
        self._board.pop()
        print("Returned: ", score)
        
        return score
        


    def getBestMoveDependOfNumberPoint(self, moves):
        best_move = moves[randint(0,len(moves)-1)]
        max_value = + self.applyBiais(best_move)
        for m in moves:
            current = self.getNumberPoints(m, len(moves)) + self.applyBiais(m)
#             self._board.pop()
            if(current > max_value):
                max_value = current
                best_move = m
                
        print("Playing a move with val: ", max_value)
        return (best_move, max_value)
        
      
        