# -*- coding: utf-8 -*-

import time
import game.board.Reversi as Reversi
from random import randint
from player.playerInterface import *
import intelligence.heuristics.eval as eval
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper

import queue
from threading import Thread
import copy
import sys


class myPlayer(PlayerInterface):
    _NotSTABLE = 0
    _STABLE = 1

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "AI Negamax ABS Scout"

    def getPlayerMove(self):
        if self._board.is_game_over():
            # print("Referee told me to play but the game is over!")
            return (-1, -1)

        #  -------negE scount -------------#
        moves = self.ia_negaC(3)
        move = moves[randint(0, len(moves) - 1)]
        #  ------- end negaABS scount -------------#

        self._board.push(move)
        # print("I am playing ", move)
        (c, x, y) = move
        assert (c == self._mycolor)
        # print("My current board :")
        # print(self._board)
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

    def negE(self, depth, alpha,beta):
        if self._board.is_game_over() or depth==0:
            return eval.getTotal(self,self._mycolor)

        best = -9999999999
        moves = boardHelper.getSortedMoves(self._board)
        for move in moves:
            self._board.push(move)
            val = - self.negE(depth-1,-beta,-alpha)
            self._board.pop()
            if val > best:
                best = val
                if best > alpha:
                    alpha = best
                    if alpha >= beta:
                        return best
        return best


    def negC(self, depth):
        if self._board.is_game_over() or depth==0:
            return eval.getTotal(self,self._mycolor)

        alpha = -99999999999
        beta = 99999999999
        while alpha!=beta:
            v = (alpha+beta)/2
            t = self.negE(depth,v,v+1)
            if t>v:
                alpha= t
            else:
                beta=t
        return alpha


    def ia_negaC(self, depth):
        best = -99999999999
        alpha = -99999999999
        beta = 99999999999
        best_shot = None
        list_of_equal_moves = []
        sortedMoves = boardHelper.getSortedMoves(self._board)
        for move in sortedMoves:
            self._board.push(move)
            v = -self.negE(depth,alpha,beta)
            if v > best or best_shot is None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves


