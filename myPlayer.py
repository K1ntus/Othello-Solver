#!/usr/bin/env python

# -*- coding: utf-8 -*-


# The MAIN AI TO DEVELOP

import time
import Reversi
from random import randint
from playerInterface import *
from multiprocessing import Process, Lock, Queue
import sys

alpha_beta_maxDepth = 8
lock = Lock()
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
#         move = None
#         if(len(moves) < 5): #minmax
#             move = moves[randint(0,len(moves)-1)]
#         else:
        (_, move) = self.MaxAlphaBeta(0, 100, 0, True)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
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


    def applyBiais(self, move):
        (_, x, y) = move
        value = 0
        lr_border = False
        tb_border = False
        
        if(x == 0 or x == 9): #left or right border
            value += 0
            lr_border = True
            
        if(y == 0 or y == 9): #top or bottom border
            value += 0
            tb_border = True
        
        if(tb_border and lr_border):
            value += 1
        
        
        return value
    
#https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
    def MaxAlphaBeta(self, alpha, beta, depth, parallelization = False):
        global alpha_beta_maxDepth
        # 10  : win
        # 0   : draw
        # -10 : lose
        maxValue = 0
        moves = self._board.legal_moves()
        move = None
        processPool = None
        
#         if(parallelization):
#             processPool = Pool(processes=2)
        
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
                    proc = Process(target=self.MinAlphaBeta_wrapper,  args=(alpha, beta, depth +1, q))
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
                    
                    print("GOT :",value)
                else:
                    value = self.MinAlphaBeta(alpha, beta, depth+1)
                if(value > maxValue + self.applyBiais(m)):
                    maxValue = value + self.applyBiais(m)#self.getNumberPoints(m)
                    move = m
            lock.acquire()
            self._board.pop()
            lock.release()
            
            
            
            if (maxValue >= beta):
                return (maxValue, move)
            
            if(maxValue > alpha):
                alpha = maxValue
                
        return (maxValue, move)

    def MinAlphaBeta_wrapper(self, a,b,c,q):
        q.put(self.MinAlphaBeta_pool(a,b,c))

    def MinAlphaBeta_pool(self, alpha, beta, depth):
        global alpha_beta_maxDepth
        
#         print("Args: ", args, flush=True)
#         print("TODO")
#         time.sleep(5)
        # 10  : win
        # 0   : draw
        # -10 : lose
        minValue = 100
        move = None
#         a = args[0]
#         a = args[0]
        print("Args: ", alpha, beta, depth, flush=True)
#         time.sleep(1)
          
        for m in self._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._board.push(m)
            lock.release()
              
            if(depth < alpha_beta_maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth+1)
                if(value > minValue + self.applyBiais(m)):
                    minValue = value + self.applyBiais(m)#self.getNumberPoints(m)
                    move = m 
            lock.acquire()
            self._board.pop()
            lock.release()
              
              
            if (minValue <= alpha):
                return (minValue, move)
              
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
        minValue = 100
        move = None
        
        
        for m in self._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._board.push(m)
            lock.release()
            
            if(depth < alpha_beta_maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth+1)
                if(value > minValue + self.applyBiais(m)):
                    minValue = value + self.applyBiais(m)#self.getNumberPoints(m)
                    move = m 
            lock.acquire()
            self._board.pop()
            lock.release()
            
            
            if (minValue <= alpha):
                return (minValue, move)
            
            if(minValue < beta):
                beta = minValue
        return minValue









