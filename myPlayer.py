#!/usr/bin/env python

# -*- coding: utf-8 -*-


# The MAIN AI TO DEVELOP

from multiprocessing import Process, Lock, Queue
from random import randint
import sys
import time

from bloom import BloomFilter
from bloom import __utils__ as Utils
from game.board import Reversi
from game.board.playerInterface import *
from intelligence.heuristics import evaluator
from intelligence.movemanager.MoveManager import MoveManager
from intelligence.movemanager.OpeningMove import OpeningMove
from player.ai.BeginnerLevelPlayer import WIDTH, HEIGHT
from h5py.h5f import flush


# from intelligence.movemanager import AlphaBeta
lock = Lock()
class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._BoardScore = None
        
        self._bloomTable = BloomFilter(max_elements=10000, error_rate=0.1, filename=None, start_fresh=False)
        self._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(self._board))
        self._maxDepth = 4
        
#         self._alphaBetaManager = AlphaBeta.AlphaBeta(self)
#         print(self._board)
        

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        move = self.moveManager()
            
        if(move == None):
            (move, _) = MoveManager.MoveForGameBeginning(self, self._board.legal_moves())
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
        val = 0
        
        
        if(nb1+nb2 < 12): #kind of random
            print("Check if ", Utils.HashingOperation.BoardToHashCode(self._board), "is present")
            move = self._openingMover.GetMove(self._board)
            if(move is not None):
                val  = -666
#         elif (WIDTH*HEIGHT - (nb1+nb2) < 25):   #minmax
#             self._maxDepth = WIDTH*HEIGHT - (nb1+nb2)
# #             self._alphaBetaManager.__update__(self)
# #             (val,move) = self._alphaBetaManager.AlphaBetaWrapper(InitDepth = 0, MaxDepth=6, Parallelization = False)
#             (val, move) = self.MaxAlphaBeta(self.__alpha__(), self.__beta__(), 0, True)
        else:   #alphabeta
#             self._alphaBetaManager.__update__(self)
#             (val,move) = self._alphaBetaManager.AlphaBetaWrapper(InitDepth = 0, MaxDepth=6, Parallelization = False)

            (val, move) = self._minmax_with_alpha_beta(Parallelization=True)
        print("")
        print("")
        print("")
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

























    def __alpha__(self):
        return 0#-10000000
    
    def __beta__(self):
        return 10000000

    
#     def AlphaBetaWrapper(self, InitDepth = 0, MaxDepth = 8, Parallelization = False):
#         self._maxDepth = MaxDepth
#         return self.MaxAlphaBeta(InitDepth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), Parallelization)
        
        
        
    def _minmax_with_alpha_beta(self, alphaInit = 0, betaInit = 0, depth = 4, Parallelization = False):
        moves = self._board.legal_moves()
        #print "leagal move" + str(moves)
#         if not isinstance(moves, list):
#             score = self._board.count()
#             (scoreW, scoreB) = self._board.get_nb_pieces()
#             if(self._mycolor is Reversi.Board._BLACK):
#                 return scoreW, None
#             return scoreB, None

        #print ply
        return_move = None
        bestscore = self.__alpha__()
        #print "using alpha_beta best score:"+ str(bestscore)
        #ply = 4
        #will define ply later;
        for m in moves:
            score = bestscore
            move = m   
            if(Parallelization):
                q = Queue()
                 
                proc = Process(target=self.alphaBetaParallelizationWrapper,  args=(depth, bestscore, self.__beta__(), m))
                proc.start()
                proc.join()
                
                (score, _) = q.get()      
            else:

                (score)  = self.alphaBetaNoParallelizationWrapper(depth, bestscore, self.__beta__(), m)

            if score > bestscore:
                bestscore = score
                return_move = move

        return (bestscore,return_move)

    def alphaBetaNoParallelizationWrapper(self, depth, alpha, beta, move):
        score = self.min_score_alpha_beta(depth, alpha, self.__beta__())
        if score > alpha:            
            alpha = score
            #print "return move" + str(return_move) + "best score" + str(bestscore)
        return (alpha)
    
    
    def alphaBetaParallelizationWrapper(self, depth, alpha, beta, move):
        score = self.min_score_alpha_beta(depth, alpha, self.__beta__())
        if score > alpha:            
            alpha = score
            #print "return move" + str(return_move) + "best score" + str(bestscore)
        return (alpha)
        
    # Also the max and min value function:
    def max_score_alpha_beta(self, depth, alpha, beta):
        moves = self._board.legal_moves()
        if depth == 0:
            return (evaluator.getHeuristicValue(self, len(moves)))
        
        bestscore = alpha
        
        
        for move in moves:          
            lock.acquire()
            self._board.push(move)
            lock.release()
            score = self.min_score_alpha_beta(depth-1, alpha, beta)
            lock.acquire()
            self._board.pop()
            lock.release()
            
            if score > bestscore:
                bestscore = score
            if bestscore >= beta:
                return bestscore
            
            alpha = max (alpha,bestscore)
        return bestscore

    def min_score_alpha_beta(self, depth, alpha, beta):
        moves = self._board.legal_moves()
        if depth == 0:
            return (evaluator.getHeuristicValue(self, len(moves)))
        
        bestscore = beta
        
        
        for move in moves:         
            lock.acquire()
            self._board.push(move)
            lock.release()
            score = self.max_score_alpha_beta( depth-1, alpha, beta)
            lock.acquire()
            self._board.pop()
            lock.release()
            
            if score < bestscore:
                bestscore = score
            if bestscore <= alpha:
                return bestscore
            
            beta = min(beta,bestscore)
        return bestscore
      
      
