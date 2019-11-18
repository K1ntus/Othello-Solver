#!/usr/bin/env python

# -*- coding: utf-8 -*-


# The MAIN AI TO DEVELOP

from multiprocessing import Process, Lock, Queue
from random import randint

import Reversi
from data import BloomFilter
from data import __utils__ as Utils
from heuristics.BeginnerLevelPlayer import WIDTH, HEIGHT
from intelligence import move as mover
from intelligence.move import OpeningMove
from playerInterface import *


# import sys
# import time
alpha_beta_maxDepth = 6
lock = Lock()
# __initAlpha__ = 18
# __initBeta__ = 10000000

class myPlayer(PlayerInterface):
    @classmethod
    def __alpha__(self):
        return 0
    
    @classmethod
    def __beta__(self):
        return 10000000

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        
        self._bloomTable = BloomFilter(max_elements=10000, error_rate=0.1, filename=None, start_fresh=False)
        self._openingMover = OpeningMove()
        self._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(self._board))
        print(self._board)
        

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        move = self.moveManager()
        val = -1
            
        if(move == None):
            (move, val) = mover.MoveManager.MoveForGameBeginning(self, [m for m in self._board.legal_moves()])
        self._board.push(move)
        print("Move Value:", val)
        print("I am playing ", move)

        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
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



#begin         game = ~random
#middle        game = minimax
#middle+end    game = alphabeta
    def moveManager(self):
        moves = [m for m in self._board.legal_moves()]
        move = moves[randint(0,len(moves)-1)]
        (nb1,nb2) = self._board.get_nb_pieces()    
        val = 0  
        
        
        if(nb1+nb2 < 8): #kind of random
            move = self._openingMover.GetMove(self._board)
            (move, _) = mover.MoveManager.MoveForGameBeginning(self, moves)
        elif (WIDTH*HEIGHT - (nb1+nb2) < 25):   #minmax
            alpha_beta_maxDepth = WIDTH*HEIGHT - (nb1+nb2)
            (_, move) = self.MaxAlphaBeta(0, self.__beta__(), self.__alpha__(), True)
        else:   #alphabeta
            (_, move) = self.MaxAlphaBeta(0, self.__beta__(), self.__alpha__(), True)
            
        print("Val is:", val)
        return move
        



    def getNumberPoints(self, move):
        (current_point_white, current_point_black) = self._board.get_nb_pieces()
        self._board.push(move)
        (new_point_white, new_point_black) = self._board.get_nb_pieces()
        self._board.pop()
        
        if(self._mycolor == 1): #black
            return (new_point_black-current_point_black) 
        else:
            return (new_point_white-current_point_white) 


    def applyBiais(self, move):
        (_, x, y) = move
        value = 8
        lr_border = False
        tb_border = False
          
        if(x == 0 or x == 9): #left or right border
            value += 1
            lr_border = True
              
        if(y == 0 or y == 9): #top or bottom border
            value += 1
            tb_border = True
              
              
        if(x == 1 or x == 8): #left or right border
            value -= 2
            lr_border = False
              
        if(y == 1 or y == 8): #top or bottom border
            value -= 2
            tb_border = False
          
        if(tb_border and lr_border):
            value += 10
         
        if(self._board.is_game_over()):
            
            (nbwhites, nbblacks) = self._board.get_nb_pieces()
                
            if(self._mycolor == 1 and nbblacks > nbwhites): #black
                value +=100
            else:
                return -5

        
        return value
    
#https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
    def MaxAlphaBeta(self, alpha, beta, depth, parallelization = False):
        global alpha_beta_maxDepth
        # 10  : win
        # 0   : draw
        # -10 : lose
        maxValue =  self.__beta__()
        moves = self._board.legal_moves()
        move = None

        self._bloomTable.__iadd__(key=Utils.HashingOperation.BoardToHashCode(self._board))

        for m in moves:
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
            
            lock.acquire()
            self._board.push(m)
            lock.release()
            if(depth < alpha_beta_maxDepth):
                value = 0
                if(parallelization):
#                     p_args = [alpha, beta, depth]
                    
#                     processPool.map(self.MinAlphaBeta_wrapper,  ([alpha, beta, depth +1 ]))
                    q = Queue()
                    proc = Process(target=self.MinAlphaBeta_wrapper,  args=(alpha, beta, depth + 1, q))
                    proc.start()
                    value = q.get()
                    proc.join(15000)
#                     value = processPool.map_async(self.MinAlphaBeta_wrapper,  [(alpha, beta, depth +1)])
#                     value = value.get()
#                     print("Launched Pool.", flush=True)
#                     sys.stdout.flush()
#                     time.sleep(10)
#                     value = self.MinAlphaBeta(alpha, beta, depth+1)
#                     sys.stdout.flush()
                    
                else:
                    value = self.MinAlphaBeta(alpha, beta, depth + 1)
                    
                lock.acquire()
                if(depth == alpha_beta_maxDepth):
                    value += self.applyBiais(m)
                    
                if(value > maxValue):
                    maxValue = value#self.getNumberPoints(m)
                    move = m
                    
                lock.release()
                    
            lock.acquire()
            self._board.pop()
            lock.release()
            
            
            
            if (maxValue >= beta):
                return (maxValue, move)
            
            if(maxValue > alpha):
                alpha = maxValue
                
        return (maxValue, move)

    def MinAlphaBeta_wrapper(self, a,b,d,q):
        q.put(self.MinAlphaBeta_pool(a,b,d))

    def MinAlphaBeta_pool(self, alpha, beta, depth):
        global alpha_beta_maxDepth
        
#         print("Args: ", args, flush=True)
#         print("TODO")
#         time.sleep(5)
        # 10  : win
        # 0   : draw
        # -10 : lose
        minValue = self.__alpha__()
        
#         a = args[0]
#         a = args[0]
#         print("Args: ", alpha, beta, depth, flush=True)
#         time.sleep(1)
          
        for m in self._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._board.push(m)
            lock.release()
              
            if(depth < alpha_beta_maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1, parallelization=False)
                if(depth == alpha_beta_maxDepth):
                    value += self.applyBiais(m)
                if(value > minValue):
                    minValue = value#self.getNumberPoints(m)
            lock.acquire()
            self._board.pop()
            lock.release()
              
              
            if (minValue <= alpha):
                return minValue
              
            if(minValue < beta):
                beta = minValue
        return minValue

#         moves = [m for m in self._board.legal_moves()]
#         
#         return 1
    
    def MinAlphaBeta(self, alpha, beta, depth):
        global alpha_beta_maxDepth
#         print("TODO")
        # 10  : win
        # 0   : draw
        # -10 : lose
        minValue =  self.__alpha__()
        
        
        for m in self._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._board.push(m)
            lock.release()
            
            if(depth < alpha_beta_maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1)
                if(depth == alpha_beta_maxDepth):
                    value += self.applyBiais(m)
                if(value > minValue ):
                    minValue = value#self.getNumberPoints(m)
            lock.acquire()
            self._board.pop()
            lock.release()
            
            
            if (minValue <= alpha):
                return minValue
            
            if(minValue < beta):
                beta = minValue
        return minValue









