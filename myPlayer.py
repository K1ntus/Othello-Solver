# -*- coding: utf-8 -*-

from multiprocessing import Queue, Process, Lock
from random import randint
import time

from bloom import __utils__ as Utils
from game.board import Reversi
from helpers import boardHelper as boardHelper
from helpers import playerHelper as playerHelper
import intelligence.heuristics.eval as eval
from intelligence.movemanager.MoveManager import MoveManager
from intelligence.movemanager.OpeningMove import OpeningMove
from player.playerInterface import PlayerInterface


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
        move = self.moveManager()
#         print("play1 ai moves : ", moves)
#         if(move is not None):
#             move = moves[randint(0, len(moves) - 1)]
#         else:
#             try:
#                 move = moves[0]
#             except:
#                 print("Moves list", moves)
#                 return(0,0)
        self._board.push(move)
        print("I am playing ", move)
        (c, x, y) = move
        assert (c == self._mycolor)
        print("My current board :")
        print(self._board)
        return (x, y)
    
    
    

    def moveManager(self):
        (nb1,nb2) = self._board.get_nb_pieces()   
        val = 0
        move = None
        
#         # Early-Game: Check opening move in a custom bloom filter
        if(nb1+nb2 < MoveManager.__AI_OPENING_MOVE_VALUE__()): 
            print("Check if ", Utils.HashingOperation.BoardToHashCode(self._board), "is present")
            move = self._openingMover.GetMove(self._board)
        # End-Game: Special depth alpha-beta
        elif ((nb1+nb2) > MoveManager.__AI_ENDGAME_VALUE__(self._board)):   
            print("Special depth For Prunning: ", nb1+nb2)
            (move) = self.ia_NegamaxABSM(depth=3, BloomCheckerFirst=True, Parallelization=True)
            
        # Mid-Game: Usual Case. Alpha Beta. Can use the parallelization, or chose to check a bloom filter if a good board has already been find 
        else:   
            #Alpha and Beta should be set directly on the AlphaBeta class
            (move) = self.ia_NegamaxABSM(depth=3, Parallelization=True)
             
             
#         time.sleep(5)
        # No move has been find, generate one with a simple heuristic
        if move is None:    
            print("")
            print("")
            print("Default value. No move has been found")
            val = -7578748789
            (move, _) = MoveManager.MoveForGameBeginning(self, self._board.legal_moves()) 
            
        print("")
        print("")
        print("")
        print("Val is:", val)
        return move
        

    def playOpponentMove(self, x, y):
        assert (self._board.is_valid_move(self._opponent, x, y))
        # print("Opponent played ", (x, y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._openingMover = OpeningMove(self._mycolor)  
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
    def NegamaxABSM(self, depth, moveTested, board, alpha, beta, color, BloomCheckerFirst=False):        
        sign = 1 if color == self._mycolor else -1
        maximising = True
        op_color = playerHelper.getOpColor(color)
        if op_color is not self._mycolor:
            maximising = False
            
        if depth == 0 or board.is_game_over():
            return  (eval.getTotal(self,self._mycolor), moveTested)
            # return eval.getTotalNegaMAx(self,color)
        sortedMoves = boardHelper.getSortedMoves(board)
        # sortedMoves = self._board.legal_moves()

        # best = -10000
        
        for move in sortedMoves:
            board.push(move)
            (val, moveTested) = (self.NegamaxABSM(depth - 1, moveTested, board, -beta, -alpha, op_color))
            val=-val
            # best = max(best, val)
            board.pop()
            if maximising:
                if(val > alpha):
                    alpha = val
                if(beta <= alpha):
                    break
            else:
                if(val < beta):
                    alpha = val
                if(beta <= alpha):
                    break
                
        return (alpha, moveTested)


    def ia_NegamaxABSM(self, depth = 2, BloomCheckerFirst = False, Parallelization = False):        
        alpha = 20
        best = -10000
        beta = 10000
        best_shot = None
        
        q = Queue()
        process_list = []
        
        list_of_equal_moves = []
        moves = self._board.legal_moves()
        for move in moves:
            if(BloomCheckerFirst):
                self._board.push(move)
                hashValue = Utils.HashingOperation.BoardToHashCode(self._board)
                self._board.pop() 
                res_contain = self._bloomTable.__contains__(key=hashValue)
                if(res_contain):
                    bestscore = (eval.getTotal(self,self._mycolor),move)
                    print("Find a table with the corresponding move, returning it", bestscore)  
                    return [move]
                    #remove the element from the bloom filter
                    #auto return move ?
            self._board.push(move)
            # v = self.NegamaxABSM(depth, alpha, beta,self._mycolor)
            
            
                
            if(Parallelization): 
                if(__name__ == '__main__'):           
                    proc = Process(target=self.NegamaxABSM, args=(depth, move, myPlayer.__CopyCurrentBoard__(self), alpha, beta, playerHelper.getOpColor(self._mycolor), BloomCheckerFirst))
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
                (v, _) = self.NegamaxABSM(depth, move, self._board, alpha, beta,playerHelper.getOpColor(self._mycolor), BloomCheckerFirst=BloomCheckerFirst)
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
            
            
        return list_of_equal_moves[randint(0, len(list_of_equal_moves) - 1)]
#         return list_of_equal_moves
    
    
    #bullshit
    def getNumberPoints(self, move):
        (current_point_white, current_point_black) = self._board.get_nb_pieces()
        self._board.push(move)
        (new_point_white, new_point_black) = self._board.get_nb_pieces()
        self._board.pop()
        
        if(self._mycolor == 1): #black
            return (new_point_black-current_point_black) 
        else:
            return (new_point_white-current_point_white) 




    
    