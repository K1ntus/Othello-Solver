# -*- coding: utf-8 -*-

import time
import game.board.ReversiBit as Reversi
# import game.board.Reversi as Reversi
from random import randint
from player.playerInterface import *
import intelligence.heuristics.eval as eval
import helpers.playerHelper as playerHelper
import helpers.boardHelper as boardHelper
import copy

cornerList = [[1, 0, 9], [1, 9, 9], [1, 9, 0], [1, 0, 0]]


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
        moves = self.ia_naga()
        move = moves[randint(0, len(moves) - 1)]
        # score, move = self.pvs(3,-1000000,1000000,self._mycolor,None)
        # score, move = self.negaScoutAB(3, -1000000, 1000000)
        # score, move = self.negascout(3, self._mycolor)
        # print(score, move)
        # score,move = self.abNegaMax(self._board,3, -9999999999, 9999999999)
        self._board.push(move)
        # print("I am playing ", move)
        (c, x, y) = move
        assert (c == self._mycolor)
        print("My current board :")
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

    def negaScout(self, depth, alpha, beta):
        if depth == 0 or self._board.is_game_over():
            # return eval.getTotal(self, self._mycolor)
            return eval.getTotal(self, playerHelper.getOpColor(self._mycolor))

        n = beta
        moves = boardHelper.getSortedMoves(self._board, self)
        count = 0
        for move in moves:
            self._board.push(move)
            count += 1
            cur = - self.negaScout(depth - 1, -n, -alpha)
            if (alpha < cur < beta) and count > 1 and depth > 1:
                alpha = -self.negaScout(depth - 1, -beta, -cur)
            alpha = max(alpha, cur)
            self._board.pop()
            if alpha >= beta:
                return alpha
            n = alpha + 1

        return alpha

    def negaMaxAB(self, depth, alpha, beta, color):
        if depth == 0 or self._board.is_game_over():
            if color == self._mycolor:
                return eval.getTotal(self, self._mycolor), [self._mycolor, -1, -1]
            else:
                return eval.getTotal(self, playerHelper.getOpColor(self._mycolor)), [self._mycolor, -1, -1]

        bestMove = [self._mycolor, -1, -1]
        bestScore = -1000000
        moves = boardHelper.getSortedMoves(self._board, self)
        for move in moves:
            self._board.push(move)
            recursedScore, currentMove = self.negaMaxAB(depth - 1, -beta, -max(alpha, bestScore),
                                                        playerHelper.getOpColor(color))
            currentScore = -recursedScore
            self._board.pop()

            if currentScore > bestScore:
                bestScore = currentScore
                bestMove = move

                if bestScore >= beta:
                    return bestScore, bestMove
        return bestScore, bestMove

    def negaScoutAB(self, depth, alpha, beta):

        if depth == 0 or self._board.is_game_over():
            return eval.getTotal(self, self._mycolor), [self._mycolor, -1, -1]

        bestMove = [self._mycolor, -1, -1]
        bestScore = -1000000
        adaptiveBeta = beta
        moves = boardHelper.getSortedMoves(self._board, self)
        for move in moves:
            self._board.push(move)
            recursedScore, currentMove = self.negaMaxAB(depth - 1, -adaptiveBeta, -max(alpha, bestScore), self._mycolor)
            currentScore = - recursedScore
            self._board.pop()

            # we are in ‘narrow-mode’ then widen
            if currentScore > bestScore:

                if adaptiveBeta == beta or depth - 2 < 0:
                    bestScore = currentScore
                    bestMove = move
                # Otherwise we can do a Test
                else:
                    # self._board.push(move)
                    negativeBestScore, bestMove = self.negaScoutAB(depth, -beta, -currentScore)
                    bestScore = - negativeBestScore
                    # self._board.pop()

            if bestScore >= beta:
                return bestScore, bestMove

            adaptiveBeta = max(alpha, bestScore) + 1
        return bestScore, bestMove

    def pvs(self, depth, alpha, beta, color, m):
        # moves = boardHelper.getSortedMoves(self._board, color)
        moves = self._board.legal_moves()
        if len(moves) == 1 and moves[0] == [color, -1, -1]:
            return moves[0]
        # print("hello")
        if depth == 0 or self._board.is_game_over():
            if color == self._mycolor:
                return -eval.getTotal(self, color), m
            else:
                return -eval.getTotal(self, playerHelper.getOpColor(color)), m
        index = 0
        bestshot = None
        for move in moves:
            self._board.push(move)
            if index == 0:
                val, m = self.pvs(depth - 1, -beta, -alpha, playerHelper.getOpColor(color), move)
                score = -val
            else:
                index += 1
                val, m = self.pvs(depth - 1, -alpha - 1, -alpha, playerHelper.getOpColor(color), move)
                score = -val
                if alpha < score < beta:
                    val, m = self.pvs(depth - 1, -beta, -alpha, playerHelper.getOpColor(color), move)
                    score = -val
            self._board.pop()
            bestshot = move
            if score >= alpha:
                alpha = score
            if alpha >= beta:
                # bestshot = m
                break
        return alpha, bestshot

    # take in count the best shot
    def _ia_pvs(self, alpha, beta, depth=3):
        worst = 1000000
        best_shot = None
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            v = self.negaScout(depth, alpha, beta)
            if v < worst or best_shot is None:
                worst = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == worst:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves

    # take in count the best shot
    def _ia_pvss(self, alpha, beta, depth=3):
        best = -1000000
        best_shot = None
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            v = -self.negaC(depth)
            if v > best or best_shot is None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves

    def negaMax(self, depth, alpha, beta, color):
        if depth == 0 or self._board.is_game_over():
            return eval.getTotal(self, color), [color, -1, -1]

        moves = boardHelper.getSortedMoves(self._board, self)
        worst = -10000000000
        self._board.push(moves[0])
        score, bestMove = self.negaMin(depth - 1, alpha, beta, playerHelper.getOpColor(color))
        score = max(worst, score)
        bestMove = moves[0]
        self._board.pop()

        if score < beta:
            for i in range(1, len(moves)):
                self._board.push(moves[i])
                value, currentMove = self.negaMin(depth - 1, score, score + 1, playerHelper.getOpColor(color))
                self._board.pop()

                if value > score:
                    if value >= beta:
                        score = value
                        bestMove = moves[i]
                    else:
                        self._board.push(moves[i])
                        score, currentMove = self.negaMin(depth - 1, value, beta, playerHelper.getOpColor(color))
                        self._board.pop()
                    if score >= beta:
                        bestMove = moves[i]
                        break
        return score, bestMove

    def negaMin(self, depth, alpha, beta, color):
        if depth == 0 or self._board.is_game_over():
            return -eval.getTotal(self, playerHelper.getOpColor(color)), [color, -1, -1]

        moves = boardHelper.getSortedMoves(self._board, self)
        best = 10000000000
        self._board.push(moves[0])
        score, bestMove = self.negaMax(depth - 1, alpha, beta, playerHelper.getOpColor(color))
        bestMove = moves[0]
        score = min(best, score)
        self._board.pop()

        if score > alpha:
            for i in range(1, len(moves)):
                self._board.push(moves[i])
                value, currentMove = self.negaMax(depth - 1, score, score + 1, playerHelper.getOpColor(color))
                self._board.pop()

                if value <= score:
                    if value <= alpha:
                        score = value
                        bestMove = moves[i]
                    else:
                        self._board.push(moves[i])
                        score, currentMove = self.negaMax(depth - 1, alpha, value, playerHelper.getOpColor(color))
                        self._board.pop()
                    if score <= alpha:
                        bestMove = moves[i]
                        break
        return score, bestMove

    def negascout(self, depth, color):
        if color == self._mycolor:
            return self.negaMax(depth, -1000000000, 1000000000, color)
        else:
            return self.negaMin(depth, -1000000000, 1000000000, color)

    def ia_naga(self):
        depth = 3
        best = -1000000
        alpha = -1000000
        beta = 1000000
        best_shot = None
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            v, m = self.negaMin(depth, -1000000000, 1000000000, playerHelper.getOpColor(self._mycolor))
            if v > best or best_shot is None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return list_of_equal_moves
