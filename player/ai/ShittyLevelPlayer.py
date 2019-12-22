# -*- coding: utf-8 -*-

import time
from game.board import Reversi
from player.playerInterface import *
from random import randint
from asyncio.tasks import sleep

WIDTH = 9
HEIGHT = 9

class myPlayer(PlayerInterface):
    '''
    An AI that should not be used. It is currently an odd implementation
    of tree search for a good move.
    
    Kinda Deprecated AI, so he will not be commented.
    '''

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "AI Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = [m for m in self._board.legal_moves()]
#         print("Available move: ", moves)
        (move, poids) = self.getBestMoveDependOfNumberPoint(moves)
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
            
            
            
    def pushAndGetNumberPoints(self, move, color):
        (current_point_white, current_point_black) = self._board.get_nb_pieces()
        self._board.push(move)
        (new_point_white, new_point_black) = self._board.get_nb_pieces()
        if(color == 1): #black
            return new_point_black - current_point_black
        else:
            return new_point_white - current_point_white
        
        

        
    def getNumberPoint(self, color):
        (current_point_white, current_point_black) = self._board.get_nb_pieces()
        if(color == 1): #black
            return current_point_black
        else:
            return current_point_white
            
            
            
    def getSumPointGotFromDict(self, dic):
        sum = 0
        for k in dic:
            (move, value) = dic[k]
            sum += value
            sum += self.applyBiais(move)
        return sum   
    
    def maxBetweenTwoDepthDict(self, dic1, dic2):
        if(dic1 == dic2):
            return dic1
        if (self.getSumPointGotFromDict(dic1) > self.getSumPointGotFromDict(dic2)):
            return dic1
        return dic2
            
            
            
            
            
                
            
            
    def setupTree(self, depthValue, depthDic, depthBestMove, cpuTimeOut):
        if (depthValue <= 0 or self._board.is_game_over()):            
            depthBestMove = self.maxBetweenTwoDepthDict(depthDic, depthBestMove)
            return (depthBestMove, depthDic)
        
        for move in self._board.legal_moves():
            val = self.pushAndGetNumberPoints(move, self._mycolor) + self.applyBiais(move)
            if(val <= 0 and depthValue < 2):
                self._board.pop()
                return (depthBestMove, depthDic)
            
            if depthDic.get(depthValue) == None:
                depthDic[depthValue] = (move, val)
            else:
                depthDic[depthValue] = (move, val)
            self.setupTree(depthValue -1, depthDic, depthBestMove, cpuTimeOut)
            self._board.pop()
            
        
        depthBestMove = self.maxBetweenTwoDepthDict(depthDic, depthBestMove)
        return (depthBestMove, depthDic)
    
    def calculation(self):
        print("TODO")
#         localGame Beginning
#         Mid-localGame
#         localGame End

    def applyBiais(self, move):
        (c, x, y) = move
        value = 0
        lr_border = False
        tb_border = False
        
        if(x == 0 or x == WIDTH): #left or right border
            value += 0
            lr_border = True
            
        if(y == 0 or y == HEIGHT): #top or bottom border
            value += 0
            tb_border = True
        
        if(tb_border and lr_border):
            value += 0
        
        
        return value
    
            
            
    def evalBoard(self):
        score = 0
        valPieces = {'corner':15, 'border':5, 'casual':1}
        #TODO
        return score
            
            
            

        

    def getBestMoveDependOfNumberPoint(self, moves):
        best_move = moves[randint(0,len(moves)-1)]
        
        max_value = 0 + self.applyBiais(best_move)
        depthDic = {}
        depthBestMove = {}
        (depthBestMove, depthDic) = self.setupTree(3, depthDic, depthBestMove, 500)        
        bestMove = depthBestMove.get(5, best_move)
                
                
        return (best_move, max_value)
        
        