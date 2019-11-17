# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *
from asyncio.tasks import sleep

WIDTH = 9
HEIGHT = 9

#bit better than the first beginner player

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
        print("Available move: ", moves)
#         time.sleep(1)
#         move = moves[randint(0,len(moves)-1)]
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
#         Game Beginning
#         Mid-Game
#         Game End

    def applyBiais(self, move):
        (c, x, y) = move
        value = 0
        lr_border = False
        tb_border = False
        
        if(x == 0 or x == WIDTH): #left or right border
            value += 1
            lr_border = True
            
        if(y == 0 or y == HEIGHT): #top or bottom border
            value += 1
            tb_border = True
        
        if(tb_border and lr_border):
            value += 3
        
        
        return value
        
        
    def getNumberPoints(self, move):
        (current_point_white, current_point_black) = self._board.get_nb_pieces()
        self._board.push(move)
        (new_point_white, new_point_black) = self._board.get_nb_pieces()
        
        if(self._mycolor == 1): #black
            return new_point_black-current_point_black
        else:
            return new_point_white-current_point_white


    def getBestMoveDependOfNumberPoint(self, moves):
        best_move = moves[randint(0,len(moves)-1)]
        max_value = + self.applyBiais(best_move)
        for m in moves:
            current = self.getNumberPoints(m) + self.applyBiais(m)
            self._board.pop()
            if(current > max_value):
                max_value = current
                best_move = m
                
        return (best_move, max_value)
        
      
        