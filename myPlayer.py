# -*- coding: utf-8 -*-

import time
import game.board.Reversi as Reversi
from random import randint
from player.playerInterface import *
import intelligence.heuristics.eval as eval
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper
from multiprocessing import Queue, Process, Lock


class myPlayer(PlayerInterface):
    _NotSTABLE=0
    _STABLE=1
    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None


    def getPlayerName(self):
        return "Player 1"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)
        moves = self.ia_NegamaxABSM(depth=2, Parallelization=False)
        print("play1 ai moves : ", moves)
        if(len(moves) > 1):
            move = moves[randint(0, len(moves) - 1)]
        else:
            try:
                move = moves[0]
            except:
                print("Moves list", moves)
                return(0,0)
        self._board.push(move)
        print("I am playing ", move)
        (c, x, y) = move
        assert (c == self._mycolor)
        print("My current board :")
        print(self._board)
        return (x, y)

    def playOpponentMove(self, x, y):
        assert (self._board.is_valid_move(self._opponent, x, y))
        # print("Opponent played ", (x, y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
            
            
    @staticmethod
    def __CopyCurrentBoard__(player):
        res = Reversi.Board(player._board._boardsize)        
        
        for x in range(0,res._boardsize,1):
            for y in range(0,res._boardsize,1):
                res._board[y][x] = player._board._board[y][x]
                
        return res
            
            
            
            
    # negamax alpha beta sorted moves
    def NegamaxABSM(self, depth, moveTested, board, alpha, beta, color):        
        sign = 1 if color == self._mycolor else -1
        op_color = playerHelper.getOpColor(color)
        if depth == 0 or board.is_game_over():
            return  (eval.getTotal(self,self._mycolor),moveTested)
            # return eval.getTotalNegaMAx(self,color)
        sortedMoves = boardHelper.getSortedMoves(board)
        # sortedMoves = self._board.legal_moves()

        # best = -10000
        
        for move in sortedMoves:
            board.push(move)
            (val,_) = (self.NegamaxABSM(depth - 1, moveTested, board, -beta, -alpha, op_color))
            val=-val
            # best = max(best, val)
            board.pop()
            alpha = max(alpha, val)
            if alpha >= beta:
                return (alpha,moveTested)
        return (alpha,moveTested)


    def ia_NegamaxABSM(self, depth = 2, BloomCheckerFirst = False, Parallelization = False):        
        best = -8000
        alpha = -10000
        beta = 10000
        best_shot = None
        
        q = Queue()
        process_list = []
        
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            # v = self.NegamaxABSM(depth, alpha, beta,self._mycolor)
            
                
            if(Parallelization): 
                if(__name__ == '__main__'):           
                    proc = Process(target=self.NegamaxABSM, args=(depth, move, myPlayer.__CopyCurrentBoard__(self), alpha, beta, playerHelper.getOpColor(self._mycolor)))
                    proc.start()
                    process_list.append({proc:move})
                else:
                    (v, _) = self.NegamaxABSM(depth, move, self._board, alpha, beta,playerHelper.getOpColor(self._mycolor))
                    if v > best or best_shot is None:
                        best = v
                        best_shot = move
                        list_of_equal_moves = [move]
                    elif v == best:
                        list_of_equal_moves.append(move)
                    
            else:
                (v, _) = self.NegamaxABSM(depth, move, self._board, alpha, beta,playerHelper.getOpColor(self._mycolor))
                if v > best or best_shot is None:
                    best = v
                    best_shot = move
                    list_of_equal_moves = [move]
                elif v == best:
                    list_of_equal_moves.append(move)
            self._board.pop()
            
            
        
                
        if(Parallelization):
#             tout=.5000
#             tout = .5000/len(process_list)
            for proc in process_list:
                proc.join()
            while q.qsize() > 0:
                (v,move) = q.get()                

                if v > best or best_shot is None:
                    best = v
                    best_shot = move
                    list_of_equal_moves = [move]
                elif v == best:
                    list_of_equal_moves.append(move)
            
        return list_of_equal_moves
    
    
    
    