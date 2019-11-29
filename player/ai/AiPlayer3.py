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


class AiPlayer3(PlayerInterface):
    _NotSTABLE = 0
    _STABLE = 1

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "AI Negamax ABS Scout"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)

        #  -------negaABS scount -------------#
        moves = self.ia_negaMax_ABS_scout(2)
        move = moves[randint(0, len(moves) - 1)]
        #  ------- end negaABS scount -------------#

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

    # nega max with alpha beta pruning with sorted moves with scout
    def negaMax_ABS_scout(self, depth, alpha, beta, color):
        # if we reach the end of game or maximum depth
        if depth == 0 or self._board.is_game_over():
            return eval.getTotal(self, self._mycolor)
            # if color == self._mycolor:
            #     return eval.getTotal(self, color)
            # else:
            #     return -eval.getTotal(self, color)

        score = -8000

        n = beta

        sortedMoves = boardHelper.getSortedMoves(self._board)
        for move in sortedMoves:
            self._board.push(move)
            cur = - self.negaMax_ABS_scout(depth - 1, -n, -alpha, playerHelper.getOpColor(color))

            if cur > score:
                if n == beta or (depth <= 2):
                    score = cur
                else:
                    score = - self.negaMax_ABS_scout(depth - 1, -beta, -cur, playerHelper.getOpColor(color))

            if score > alpha:
                alpha = score
            self._board.pop()
            if alpha >= beta:
                return alpha
            n = alpha + 1
        return score

    def ia_negaMax_ABS_scout(self, depth):
        best = -8000
        alpha = -10000
        beta = 10000
        best_shot = None
        list_of_equal_moves = []
        sortedMoves = boardHelper.getSortedMoves(self._board)
        for move in sortedMoves:
            self._board.push(move)
            v = self.negaMax_ABS_scout(depth, alpha, beta, playerHelper.getOpColor(self._mycolor))
            if v > best or best_shot is None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves

    def ia_negaMax_ABS_scout_thread(self, depth):
        alpha = -10000
        beta = 10000
        sortedMoves = boardHelper.getSortedMoves(self._board)
        que = queue.Queue()
        for move in sortedMoves:
            clonedPlayer = copy.deepcopy(self)
            clonedPlayer._board.push(move)
            worker = Thread(target=lambda q, cp, d, A, B, c, m: q.put((self.negaMax_ABS_scout(d, A, B, c), m)),
                            args=(que, clonedPlayer, depth, alpha, beta, playerHelper.getOpColor(self._mycolor)))
            worker.start()

        data = []
        for w in range(len(sortedMoves)):
            data.append(que.get())

        tmp = sorted(data, key=lambda d: d[0], reverse=True)
        best = tmp[0][0]
        bestMoves = []
        for i in tmp:
            if tmp[i][0] == best:
                bestMoves.append(tmp[i][1])

        return bestMoves
