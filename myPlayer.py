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
        
        self._bloomTable = None
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
        
        self._bloomTable = BloomFilter(max_elements=3000, error_rate=0.1, filename=None, start_fresh=False)

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
#             (move,val) = MoveManager.MoveForGameBeginning(self, self._board.legal_moves())
            if(move is not None):
                val  = -666
        elif (WIDTH*HEIGHT - (nb1+nb2) < 15):   #special depth alpha-beta
            self._maxDepth = WIDTH*HEIGHT - (nb1+nb2)
            print("Special depth For Prunning: ", self._maxDepth)
#             self._alphaBetaManager.__update__(self)
#             (val,move) = self._alphaBetaManager.AlphaBetaWrapper(InitDepth = 0, MaxDepth=6, Parallelization = False)
            (val, move) = self._minmax_with_alpha_beta(Parallelization=False, BloomCheckerFirst=False)
        else:   #alphabeta
            (val, move) = self._minmax_with_alpha_beta(Parallelization=False)
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
        return -99.99
    
    def __beta__(self):
        return 101

    
#     def AlphaBetaWrapper(self, InitDepth = 0, MaxDepth = 8, Parallelization = False):
#         self._maxDepth = MaxDepth
#         return self.MaxAlphaBeta(InitDepth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), Parallelization)
        
        
        
    def _minmax_with_alpha_beta(self, alphaInit = 0, betaInit = 0, depth = 6, BloomCheckerFirst=True, Parallelization = False):
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
            
            if(BloomCheckerFirst):
                self._board.push(m)
                hashValue = Utils.HashingOperation.BoardToHashCode(self._board)
                self._board.pop() 
                res_contain = self._bloomTable.__contains__(key=hashValue)
                if(res_contain):
                    print("Find a table with the corresponding move, returning it", score)  
                    bestscore = 0.99
                    return_move = m
                    break
                    #remove the element from the bloom filter

#                 return (bestscore, return_move)

                
            if(Parallelization):
                q = Queue()
                 
                proc = Process(target=self.alphaBetaParallelizationWrapper,  args=(depth, bestscore, self.__beta__(), m, BloomCheckerFirst))
                proc.start()
                proc.join()
                
                (score, _) = q.get()      
            else:

                (score)  = self.alphaBetaNoParallelizationWrapper(depth, bestscore, self.__beta__(), m, BloomCheckerFirst)

            if score > bestscore:
                bestscore = score
                return_move = move
                if bestscore > 0.99 and BloomCheckerFirst: #instanciate
                    self._board.push(m)
                    print("Instanciate a table with the score", score)  
                    self._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(self._board))
                    self._board.pop() 

                


        return (bestscore,return_move)

    def alphaBetaNoParallelizationWrapper(self, depth, alpha, beta, move, BloomCheckerFirst):
        score = self.max_score_alpha_beta(depth, alpha, beta, BloomCheckerFirst)
        if score > alpha:            
            alpha = score
            #print "return move" + str(return_move) + "best score" + str(bestscore)
        return (alpha)
    
    
    def alphaBetaParallelizationWrapper(self, depth, alpha, beta, move, BloomCheckerFirst):
        score = self.max_score_alpha_beta(depth, alpha, beta, BloomCheckerFirst)
        if score > alpha:            
            alpha = score
            #print "return move" + str(return_move) + "best score" + str(bestscore)
        return (alpha)
        
    # Also the max and min value function:
    def max_score_alpha_beta(self, depth, alpha, beta, BloomCheckerFirst):
        moves = self._board.legal_moves()
        if depth == 0:
            score = (evaluator.getHeuristicValue(self, len(moves)))
            
            if(BloomCheckerFirst):
                hashValue = Utils.HashingOperation.BoardToHashCode(self._board)
                res_contain = self._bloomTable.__contains__(key=hashValue)
                if(not res_contain and score > 0.99):
#                     print("Instanciate a table with the score", score)  
                    self._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(self._board))
    #             print("Reached bottom of the tree with score:", score)                      
            return score
        
        maxVal = self.__alpha__()
        
        for move in moves:          
            self._board.push(move)
            score = self.min_score_alpha_beta(depth-1, alpha, beta, BloomCheckerFirst)
            self._board.pop()
            
            if score > maxVal:
                maxVal = score
                    
                if maxVal >= beta:
                    return maxVal
            
                if(maxVal > alpha):
                    alpha = maxVal
                    
                    
                    
            
        return alpha

    def min_score_alpha_beta(self, depth, alpha, beta, BloomCheckerFirst):
        moves = self._board.legal_moves()
        if depth == 0:
            score = (evaluator.getHeuristicValue(self, len(moves)))
                             
            return score
        
        
        minVal = self.__beta__()
        
        for move in moves:         
            self._board.push(move)
            score = self.max_score_alpha_beta( depth-1, alpha, beta, BloomCheckerFirst)
            self._board.pop()
            
            if score < minVal:
                minVal = score
                
                if(minVal < beta):
                    beta = minVal
                    if(BloomCheckerFirst):
                        hashValue = Utils.HashingOperation.BoardToHashCode(self._board)
                        res_contain = self._bloomTable.__contains__(key=hashValue)
                        if(not res_contain and minVal >= 0.99):
                            self._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(self._board))
                    
                    
                    
                if minVal <= alpha:
                    return minVal
                
            
        return beta
      
      
