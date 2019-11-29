# -*- coding: utf-8 -*-

import time
import game.board.Reversi as Reversi
from random import randint
from player.playerInterface import *
import intelligence.heuristics.eval as eval
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper


class AiPlayer2(PlayerInterface):
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
        moves = self.ia_NegamaxABSM(2)
        print("play1 ai moves : ", moves)
        move = moves[randint(0, len(moves) - 1)]
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
    # negamax alpha beta sorted moves
    def NegamaxABSM(self,depth, alpha, beta, color):
        sign = 1 if color == self._mycolor else -1
        op_color = playerHelper.getOpColor(color)
        if depth == 0 or self._board.is_game_over():
            return  eval.getTotal(self,self._mycolor)
            # return eval.getTotalNegaMAx(self,color)
        sortedMoves = boardHelper.getSortedMoves(self._board)
        # sortedMoves = self._board.legal_moves()

        # best = -10000
        for move in sortedMoves:
            self._board.push(move)
            val = -(self.NegamaxABSM(depth - 1, -beta, -alpha, op_color))
            # best = max(best, val)
            self._board.pop()
            alpha = max(alpha, val)
            if alpha >= beta:
                return alpha
        return alpha


    def ia_NegamaxABSM(self,depth):
        best = -8000
        alpha = -10000
        beta = 10000
        best_shot = None
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            # v = self.NegamaxABSM(depth, alpha, beta,self._mycolor)
            v = self.NegamaxABSM(depth, alpha, beta,playerHelper.getOpColor(self._mycolor))
            if v > best or best_shot is None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves