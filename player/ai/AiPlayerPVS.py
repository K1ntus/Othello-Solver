# -*- coding: utf-8 -*-

import time
import game.board.Reversi as Reversi
from random import randint
from player.playerInterface import *
import intelligence.heuristics.eval as eval
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper
import copy

class myPlayer(PlayerInterface):
    _NotSTABLE = 0
    _STABLE = 1

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "AI PVS"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)
        moves = self._ia_pvs(-9999999999, 9999999999, 3)
        move = moves[randint(0, len(moves) - 1)]
        # score,move = self.abNegaMax(self._board,3, -9999999999, 9999999999)
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

    # def pvs(self, alpha, beta, depth):
    #     if depth == 0 or self._board.is_game_over():
    #         return eval.getTotal(self, playerHelper.getOpColor(self._mycolor))
    #     moves = boardHelper.getSortedMoves(self._board,self)
    #     bSearcjPv = True
    #     for move in moves:
    #         self._board.push(move)
    #         if bSearcjPv:
    #             value = -self.pvs(-beta, -alpha, depth - 1)
    #         else:
    #             value = -self.pvs(-alpha - 1, -alpha, depth - 1)
    #             if value > alpha:
    #                 value = -self.pvs(-beta, -alpha, depth - 1)
    #         self._board.pop()
    #
    #         if value >= beta:
    #             return beta
    #         if value > alpha:
    #             alpha = value
    #             bSearcjPv = False
    #     return alpha

    def abNegaMax(self,board,depth,alpha,beta):
        if depth == 0 or self._board.is_game_over():
            if self._mycolor == self._board._nextPlayer:
                return eval.getTotal(self,self._mycolor), None
            else:
                return eval.getTotal(self, self._mycolor), None

        bestMove = None
        bestScore = -9999999999

        moves = board.legal_moves()
        for move in moves:
            board.push(move)
            newBoard = copy.deepcopy(self._board)
            board.pop()
            recursedScore, currentMove = self.abNegaMax(newBoard,depth-1,-beta,-max(alpha,bestScore))
            currentScore = -recursedScore

            if currentScore > bestScore:
                bestScore = currentScore
                bestMove = move
                if bestScore >= beta:
                    return bestScore, bestMove
        return bestScore, bestMove




    def pvss(self,board, depth, alpha, beta):
        if depth == 0 or self._board.is_game_over():
            # return eval.getTotal(self, playerHelper.getOpColor(self._mycolor)), None
            return eval.getTotal(self, self._mycolor), None
        moves = boardHelper.getSortedMoves(board,self)
        bestMove = None
        bestScore = -9999999999
        adaptiveBeta = beta
        for move in moves:
            board.push(move)
            newBoard = copy.deepcopy(self._board)
            board.pop()
            (recursedScore, currentMove) = self.abNegaMax(newBoard, depth-1, -adaptiveBeta, -max(alpha,bestScore))
            currentScore =  -recursedScore
            # Update the best score
            if currentScore > bestScore:
                if adaptiveBeta == beta or depth - 2 <= 0:
                    bestScore = currentScore
                    bestMove = move
                else:

                    (negativeBestScore, bestMove) = self.pvss(newBoard,depth, -beta, -currentScore)
                    bestScore = -negativeBestScore

            if bestScore >= beta:
                return bestScore, bestMove
            adaptiveBeta = max(alpha, bestScore) + 1

        return (bestScore, bestMove)

    def negaScout(self,depth,alpha,beta):
        if depth == 0 or self._board.is_game_over():
            return eval.getTotal(self, self._mycolor)

        score = -9999999999
        n = beta
        moves = boardHelper.getSortedMoves(self._board,self)
        for move in moves:
            self._board.push(move)
            cur = - self.negaScout(depth-1,-n, -alpha)
            if(cur > score):
                if n== beta or depth<=2:
                    score =cur
                else:
                    score = - self.negaScout(depth-1,-beta,-cur)
            if(score>alpha):
                alpha=score
            self._board.pop()
            if alpha>= beta:
                return alpha
            n=alpha+1

        return score





    # take in count the best shot
    def _ia_pvs(self, alpha, beta, depth=3):
        best = -9999999999
        best_shot = None
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            v = - self.negaScout(depth, alpha, beta)
            if v > best or best_shot is None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves
