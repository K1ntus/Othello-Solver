#!/usr/bin/env python

# -*- coding: utf-8 -*-

import time

from bloom import BloomFilter
from bloom import __utils__ as Utils
from game.board import Reversi
from player.playerInterface import *
from intelligence.movemanager.AlphaBeta import AlphaBeta
from intelligence.movemanager.MoveManager import MoveManager
from intelligence.movemanager.OpeningMove import OpeningMove


class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._BoardScore = None
        
        self._bloomTable = None
        
#         self._alphaBetaManager = AlphaBeta.AlphaBeta(self)
#         print(self._board)
        

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        move = self.moveManager()
            
        self._board.push(move)

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
        if(color == self._board._BLACK):
            print("Init Black Player ")
        else:
            print("Init White Player ")
            
        self._openingMover = OpeningMove(self._mycolor)        
        self._opponent = 1 if color == 2 else 2        
        self._bloomTable = BloomFilter(max_elements=5000, error_rate=0.01, filename=None, start_fresh=False)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



    def moveManager(self):
        """ define the way to calculate the next move depending of the number
        of non-free tokens on the board.
        
        For the Early Game, if the sum of pieces is lower than a constant, then we are 
        looking into a bloomtable containing a list of well-known Opening Move.
        If one is find, we are playing this move.
        
        For the Mid-Game, we are doing a simple AlphaBeta Pruning over few depth.
        Two experimental modes has been implemented, One using the parallelization
        (which will create process only for the fist layer of AB) and another one
        is using Bloom Filter. Both of them are currently not used, because we are
        losing a bit of performance regarding the result we will obtain. The parallelization
        will also reduce the pruning because we will not pass the alpha and beta value 
        over process.
        Concerning the BloomCheckerFirst, the goal was to instanciate every board that we saw
        with a pretty high heuristic value while we are looking over the AB tree.
        Unfortunatly, with the current implementation, we will instanciate these board, even
        if it could lead to some wrong path.
        
        The End-Game is used when the number of pieces is greater than another constant. This phase
        of the game currently have a lot less available move than the "mid-game", so we increased
        the depth for the AB-pruning.
        
        
        In case of problem (ie. no moves has been found, then None), We Generate a move using a simple
        heuristic that will return the best move over the number of tokens flipped. This function/way of work
        shall be replaced in the future.
        """
        
        (nb1,nb2) = self._board.get_nb_pieces()   
        val = 0
        
        # Early-Game: Check opening move in a custom bloom filter
        if(nb1+nb2 < MoveManager.__AI_OPENING_MOVE_VALUE__()): 
            print("Check if ", Utils.HashingOperation.BoardToHashCode(self._board), "is present")
            move = self._openingMover.GetMove(self._board)
            
        # End-Game: Special depth alpha-beta
        elif ((nb1+nb2) > MoveManager.__AI_ENDGAME_VALUE__(self._board)):   
#             self._maxDepth = WIDTH*HEIGHT - (nb1+nb2)
            print("Special depth For Prunning: ", nb1+nb2)
            (val, move) = AlphaBeta.__alpha_beta_main_wrapper__(player=self,
                                                                depth=self._board._boardsize * self._board._boardsize - (nb1+nb2), 
                                                                Parallelization=False,
                                                                BloomCheckerFirst=False)
           
        # Mid-Game: Usual Case. Alpha Beta. Can use the parallelization, or chose to check a bloom filter if a good board has already been find 
        else:   
            #Alpha and Beta should be set directly on the AlphaBeta class
            (val, move) = AlphaBeta.__alpha_beta_main_wrapper__(player=self, 
                                                                depth=3,
                                                                Parallelization=False,
                                                                BloomCheckerFirst=False)
            
        # No move has been find, generate one with a simple heuristic
        if move is None:    
            print("")
            print("")
            print("Default value. No move has been found")
            val = -7578748789
#             time.sleep(1)
            (move, _) = MoveManager.MoveForGameBeginning(self, self._board.legal_moves()) 
            
        print("")
        print("")
        print("")
        print("Val is:", val)
#         time.sleep(1)
        return move
        


    #bullshit
    def getNumberPoints(self, move):
        """ Deprecated.
        Used by the MoveManager if no move has been found, we need to keep it while we do not
        have replaced the way to prevent None move.
        """
        (current_point_white, current_point_black) = self._board.get_nb_pieces()
        self._board.push(move)
        (new_point_white, new_point_black) = self._board.get_nb_pieces()
        self._board.pop()
        
        if(self._mycolor == 1): #black
            return (new_point_black-current_point_black) 
        else:
            return (new_point_white-current_point_white) 



