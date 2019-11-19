#!/usr/bin/env python

# -*- coding: utf-8 -*-


# The MAIN AI TO DEVELOP

from multiprocessing import Process, Lock, Queue
from random import randint
import time

from bloom import BloomFilter
from bloom import __utils__ as Utils
from game.board import Reversi
from game.board.playerInterface import *
from intelligence.heuristics import evaluator
from intelligence.movemanager.MoveManager import MoveManager
from intelligence.movemanager.OpeningMove import OpeningMove
from player.ai.BeginnerLevelPlayer import WIDTH, HEIGHT


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
        return 50

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._BoardScore = None
        
        self._bloomTable = BloomFilter(max_elements=10000, error_rate=0.1, filename=None, start_fresh=False)
        self._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(self._board))
#         print(self._board)
        

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        move = self.moveManager()
            
        if(move == None):
            (move, _) = MoveManager.MoveForGameBeginning(self, [m for m in self._board.legal_moves()])
        self._board.push(move)
#         print("I am playing ", move)

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
#         self._BoardScore = 
        if(color == self._board._BLACK):
            print("Init Black Player ")
        else:
            print("Init White Player ")
            
        self._openingMover = OpeningMove(self._mycolor)
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
        move = None
        (nb1,nb2) = self._board.get_nb_pieces()    
        val = -1 
        
        
        if(nb1+nb2 < 12): #kind of random
            print("Check if ", Utils.HashingOperation.BoardToHashCode(self._board), "is present")
            
            move = self._openingMover.GetMove(self._board)
        elif (WIDTH*HEIGHT - (nb1+nb2) < 25):   #minmax
            alpha_beta_maxDepth = WIDTH*HEIGHT - (nb1+nb2)
            (val, move) = self.MaxAlphaBeta(0, self.__beta__(), self.__alpha__(), False)
        else:   #alphabeta
            (val, move) = self.MaxAlphaBeta(0, self.__beta__(), self.__alpha__(), False)
            
        print("Val is:", val)
#         time.sleep(1)
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




    def evalBoard(self):
        return 0
    
#https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
    def MaxAlphaBeta(self, alpha, beta, depth, parallelization = False):
        global alpha_beta_maxDepth
        # 10  : win
        # 0   : draw
        # -10 : lose
        maxValue =  alpha
        moves = self._board.legal_moves()
        if depth == alpha_beta_maxDepth or len(moves) == 0:
            (val) = (evaluator.get_corner_score(self))
#             print("Move: with val:", val)
            return (val, None)
        
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
#                 if(depth == alpha_beta_maxDepth):
#                     value += self.applyBiais(m)
                    
                if(value > maxValue):
                    maxValue = value
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
        
        # 10  : win
        # 0   : draw
        # -10 : lose
        minValue = beta
        
        moves = self._board.legal_moves()
        if depth == alpha_beta_maxDepth or len(moves) == 0:
            (val) = (evaluator.get_corner_score(self))
            print("Move: with val:", val)
            return (val)
        
        for m in self._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._board.push(m)
            lock.release()
              
            if(depth < alpha_beta_maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1, parallelization=False)
#                 if(depth == alpha_beta_maxDepth):
#                     value += self.applyBiais(m)
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
        minValue =  beta
        
        moves = self._board.legal_moves()
        if depth == alpha_beta_maxDepth or len(moves) == 0:
            (val) = (evaluator.get_corner_score(self))
            print("Move: with val:", val)
            return (val)
        
        for m in self._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._board.push(m)
            lock.release()
            
            if(depth < alpha_beta_maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1)
#                 if(depth == alpha_beta_maxDepth):
#                     value += self.applyBiais(m)
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









