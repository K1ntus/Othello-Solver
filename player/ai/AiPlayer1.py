# -*- coding: utf-8 -*-

import time
import game.board.ReversiBit as Reversi
from random import randint
from player.playerInterface import *
import intelligence.heuristics.eval as eval
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper
import multiprocessing
import threading as Thread
import multiprocessing
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import queue
import copy
import os

# MAX_WOKER = multiprocessing.cpu_count()
MAX_WOKER = 10



class myPlayer(PlayerInterface):
    _NotSTABLE=0
    _STABLE=1
    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "AI MinMax AB"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)
        moves = self._ia_max_min_thread()
        move = moves[randint(0, len(moves) - 1)]
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
        self.cornerList = [[color, 0, 9], [color, 9, 9], [color, 9, 0], [color, 0, 0]]

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def _max_min(self, depth, alpha, beta):
        if depth == 0 or self._board.is_game_over():
            return eval.getTotal(self, self._mycolor)
        # best = alpha
        moves = boardHelper.getSortedMoves(self._board, self)
        for move in moves:
            self._board.push(move)
            alpha = max(alpha, self._min_max(depth - 1, alpha, beta))
            self._board.pop()
            # if val > best:
            #     best = val
            if alpha >= beta:
                return beta
            # if best > alpha:
            #     alpha=best

        return alpha

    def _min_max(self, depth, alpha, beta):
        if depth == 0 or self._board.is_game_over():
            return -eval.getTotal(self, playerHelper.getOpColor(self._mycolor))
            # return eval.getTotal(self, self._mycolor)
        # worst = beta
        moves = boardHelper.getSortedMoves(self._board, self)
        for move in moves:
            self._board.push(move)
            beta = min(beta, self._max_min(depth - 1, alpha, beta))
            self._board.pop()
            # if val < worst:
            #     worst = val
            # if worst <= alpha:
            #     return worst
            if alpha >= beta:
                return alpha
        return beta

    # take in count the best shot
    def _ia_max_min(self):
        nbOccupied = self._board._nbWHITE + self._board._nbBLACK
        if nbOccupied <= 20:
            depth = 6
        if nbOccupied <= 80:
            depth = 3
        else:
            depth = 6

        sign = 1
        if depth % 2 == 0:
            sign = 1
        best = -1000000
        alpha = -1000000
        beta = 1000000
        best_shot = None
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            v = sign * self._min_max(depth, alpha, beta)
            if v > best or best_shot is None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves

    # ===================== min max for concurrent ======================#
    def _max_min_con(self, player, m, depth, alpha, beta):
        if depth == 0 or player._board.is_game_over():
            return eval.getTotal(player, self._mycolor), m
        # best = alpha
        # moves = boardHelper.getSortedMoves(player._board, self)
        moves = player._board.legal_moves()
        for move in moves:
            player._board.push(move)
            val, tmp = self._min_max_con(player, m, depth - 1, alpha, beta)
            alpha = max(alpha, val)
            player._board.pop()
            if alpha >= beta:
                return beta, m

        return alpha, m

    def _min_max_con(self, player, m, depth, alpha, beta):
        # if alpha == -9999999999:
        #     print("Executing our Task on Process {}".format(os.getpid()))

        if depth == 0 or player._board.is_game_over():
            # return eval.getTotal(player, playerHelper.getOpColor(self._mycolor)), m
            return eval.getTotal(player, self._mycolor), m
        # worst = beta
        # moves = boardHelper.getSortedMoves(player._board, self)
        moves = player._board.legal_moves()
        for move in moves:
            player._board.push(move)
            val, tmp = self._max_min_con(player, m, depth - 1, alpha, beta)
            beta = min(beta, val)
            player._board.pop()

            if alpha >= beta:
                return alpha, m
        return beta, m

    # take in count the best shot
    def _ia_max_min_thread(self):
        global MAX_WOKER
        nbOccupied = self._board._nbWHITE + self._board._nbBLACK
        if nbOccupied <= 20:
            depth = 4
        if 20 < nbOccupied <= 45:
            depth = 4
        if 45 < nbOccupied <= 55:
            depth = 4
        if 55 < nbOccupied <= 80:
            depth = 4
        if 80 < nbOccupied:
            depth = 4


        sign = 1
        # if depth % 2 == 0:
        #     sign = 1
        best = -9999999999
        alpha = -9999999999
        beta = 9999999999
        best_shot = None
        list_of_equal_moves = []
        moves = self._board.legal_moves()

        cornerArr = []
        # killer corner moves
        for move in moves:
            if move in self.cornerList:
                cornerArr.append(move)
        if len(cornerArr) > 0:
            return cornerArr

        # if (len(moves) < 6):
        #     return self._ia_max_min()

        # ====================== use concurrent futures =========== #

        futures = []
        with concurrent.futures.ProcessPoolExecutor(MAX_WOKER) as executor:
            for move in moves:
                player = copy.deepcopy(self)
                player._board.push(move)
                # self._board.push(move)
                futures.append(executor.submit(self._min_max_con, player, move, depth, alpha, beta))
                # self._board.pop()

        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data[0] * sign > best or best_shot is None:
                best = data[0]
                best_shot = data[1]
                list_of_equal_moves = [best_shot]
            elif data[0] == best:
                list_of_equal_moves.append(data[1])
        return list_of_equal_moves
        # ========================================================= #
