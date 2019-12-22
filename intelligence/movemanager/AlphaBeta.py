'''
Created on 20 nov. 2019
 
@author: jordane
'''

from multiprocessing import Queue, Process, Lock
import time

from bloom import __utils__ as Utils
from game.board import Reversi
from intelligence.heuristics import eval

__MaxAllowedTimeInSeconds__ = 7


class AlphaBeta:
 
    
    '''Class Implementing an AB-Pruning for reversi with 2 experimental options.
            Both of them are currently not used, because we are
                    losing a bit of performance regarding the result we will obtain. The parallelization
                    will also reduce the pruning because we will not pass the alpha and beta value 
                    over process.
                    Concerning the BloomCheckerFirst, the goal was to instanciate every board that we saw
                    with a pretty high heuristic value while we are looking over the AB tree.
                    Unfortunatly, with the current implementation, we will instanciate these board, even
                    if it could lead to some wrong path.
        '''
    def __init__(self):
        self.startTime = 0
        
        self.synch_alpha = AlphaBeta.__alpha__()
        self.synch_alpha_locker = Lock()
        self.synch_beta = AlphaBeta.__beta__()
        self.synch_beta_locker = Lock()
         
    def __reset__(self):
        self.startTime = 0
        
        
        self.synch_alpha = AlphaBeta.__alpha__()
        self.synch_alpha_locker = Lock()
        self.synch_beta = AlphaBeta.__beta__()
        self.synch_beta_locker = Lock()
        
        
    @classmethod
    def __synch_update_alpha__(self, newVal):
        self.synch_alpha_locker.acquire()
        if(newVal < self.synch_alpha):
            self.synch_alpha = newVal
        self.synch_alpha_locker.release()
        return self.synch_alpha
        
    @classmethod
    def __synch_update_beta__(self, newVal):
        self.synch_beta_locker.acquire()
        if(newVal > self.synch_beta):
            self.synch_beta = newVal
        self.synch_beta_locker.release()
        return self.synch_beta
    
    def __get_synch_beta__(self):
        return self.synch_beta
    
    def __get_synch_alpha__(self):
        return self.synch_alpha

    @staticmethod
    def __alpha__():
        return -float('Inf')
    
    @staticmethod
    def __beta__():
        return float('Inf')
    
    @classmethod
    def __minValueForInstanciation__(self):
        """Deprecated.
            The heuristic score required to instanciate a board in the bloom filter"""
        return 99.95

    
#     def AlphaBetaWrapper(player, InitDepth = 0, MaxDepth = 8, Parallelization = False):
#         player._maxDepth = MaxDepth
#         return player.MaxAlphaBeta(InitDepth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), Parallelization)
        
    @staticmethod
    def __CopyCurrentBoard__(player):
        """Function used to copy the current Reversi board and work over a 
        copy. Mainly used for multithreading"""
        res = Reversi.Board(player._board._boardsize)        
        
        for x in range(0,res._boardsize,1):
            for y in range(0,res._boardsize,1):
                res._board[y][x] = player._board._board[y][x]
                
        return res
        
        
    def __alpha_beta_main_wrapper__(self,
            player, 
            depth = 3, #nb pair svp
            BloomCheckerFirst = False, 
            Parallelization   = False
        ):
        """function that will organize the AB-pruning depending of the options enabled"""
        moves = player._board.legal_moves()

        startTime = time.time()
        return_move = None
        bestscore = AlphaBeta.__alpha__()
        q = Queue()
        process_list = []


        for m in moves:
            move = m   
            
            if(BloomCheckerFirst):
                player._board.push(m)
                hashValue = Utils.HashingOperation.BoardToHashCode(player._board)
                player._board.pop() 
                res_contain = player._bloomTable.__contains__(key=hashValue)
                if(res_contain):
                    bestscore = AlphaBeta.__minValueForInstanciation__()
                    print("Find a table with the corresponding move, returning it", bestscore)  
                    return_move = m
                    return (AlphaBeta.__minValueForInstanciation__(), m)
                    #remove the element from the bloom filter
                    #auto return move ?
                    
                
            if(Parallelization): 
#                 if __name__ == '__main__':
#                     freeze_support()                
                    proc = Process(target=self.alphaBetaParallelizationWrapper,  args=(player, depth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), m, q, BloomCheckerFirst))
                    proc.start()
                    process_list.append(proc)
            else:

                (score)  = self.alphaBetaNoParallelizationWrapper(player, depth, bestscore, AlphaBeta.__beta__(), m, BloomCheckerFirst)
    
                if score > bestscore:
                    bestscore = score
                    return_move = move
                if bestscore >= AlphaBeta.__minValueForInstanciation__() and BloomCheckerFirst: #instanciate
                    player._board.push(m)
#                     print("Instanciate a table with the score", score)  
                    player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(player._board))
                    player._board.pop() 
                if (time.time() - startTime > __MaxAllowedTimeInSeconds__):
                    break

                
        if(Parallelization):
#             tout=5
#             tout = .5000/len(process_list)
            for proc in process_list:
                proc.join()#timeout=tout)
            while q.qsize() > 0:
                (score,move) = q.get(block=True)
                 
                if score > bestscore:
                    bestscore = score
                    return_move = move
                if bestscore >= AlphaBeta.__beta__():
                    return (bestscore, return_move)
            
        print("---------------------")
        return (bestscore,return_move)



    @classmethod
    def alphaBetaNoParallelizationWrapper(self, player, depth, alpha, beta, move, BloomCheckerFirst):
        """wrapper used only for the sequential AB-pruning."""
        player._board.push(move)
        self.startTime = time.time()
        score = self.min_score_alpha_beta(player, player._board, depth, alpha, beta, BloomCheckerFirst)
        if score > alpha:            
            alpha = score
        player._board.pop()
        return (alpha)
    
    
    @classmethod
    def alphaBetaParallelizationWrapper(self, player, depth, alpha, beta, move, queue, BloomCheckerFirst):
        """wrapper used only for the multiprocessing AB-pruning, to organize the parameters, set up the Queue
        or create a copy of the board"""
        copiedBoard = AlphaBeta.__CopyCurrentBoard__(player)
        self.startTime = time.time()
        player._board.push(move)
        score = self.min_score_alpha_beta(player, copiedBoard, depth, alpha, beta, BloomCheckerFirst)
        player._board.pop()
        if score > alpha:            
            alpha = score
        queue.put( (alpha, move) )
        copiedBoard = None
        return alpha
        
        
        
        
        
        
    # Also the max and min value function:
    @classmethod
    def max_score_alpha_beta(self, player, board, depth, alpha, beta, BloomCheckerFirst):
        moves = board.legal_moves()
        
         
        if board.is_game_over():
            (nbB, nbW) = board.get_nb_pieces()
            if player._mycolor is Reversi.Board._BLACK:
                if nbB > nbW:                
                    if(BloomCheckerFirst):   #win board
                        hashValue = Utils.HashingOperation.BoardToHashCode(board)
                        res_contain = player._bloomTable.__contains__(key=hashValue)
                        if(not res_contain): 
                            player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
                    return AlphaBeta.__beta__()
                 
                else:   #lose board
                    return AlphaBeta.__alpha__()
            else:       #win board
                if nbW > nbB:                
                    if(BloomCheckerFirst):
                        hashValue = Utils.HashingOperation.BoardToHashCode(board)
                        res_contain = player._bloomTable.__contains__(key=hashValue)
                        if(not res_contain):
                            player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
                    return AlphaBeta.__beta__()
                 
                else:   #lose board
                    return AlphaBeta.__alpha__()
            
        if depth == 0 or board.is_game_over() or time.time() - self.startTime > __MaxAllowedTimeInSeconds__:  # leaves of alpha-beta pruning          
            score =  eval.getTotal(player,player._mycolor)
            return score
             
            if(BloomCheckerFirst):
                hashValue = Utils.HashingOperation.BoardToHashCode(board)
                res_contain = player._bloomTable.__contains__(key=hashValue)
                if(not res_contain and score > AlphaBeta.__minValueForInstanciation__()):
                    player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
            return score
        
        
#         maxVal = self.synch_alpha  
        maxVal = alpha
        
        
        for move in moves:       
            board.push(move)
            score = self.min_score_alpha_beta(player, board, depth-1, alpha, beta, BloomCheckerFirst)
            board.pop()
            
            if score > maxVal:
                maxVal = score
            if maxVal >= beta:
                return maxVal
        
            if maxVal > alpha:
#                 alpha = self.__synch_update_alpha__(maxVal)
                alpha = maxVal
                 
                
            if (time.time() - self.startTime > __MaxAllowedTimeInSeconds__):
                break
            
        return maxVal


    @classmethod
    def min_score_alpha_beta(self, player, board, depth, alpha, beta, BloomCheckerFirst):
        moves = board.legal_moves()
        
                
        if depth == 0 or board.is_game_over() or time.time() - self.startTime > __MaxAllowedTimeInSeconds__:
            return eval.getTotal(player,player._mycolor)
        
#         minVal = self.synch_beta
        minVal = beta
        
        for move in moves:
                 
            board.push(move)
            score = self.max_score_alpha_beta(player, board, depth-1, alpha, beta, BloomCheckerFirst)
            board.pop()
            
            
            
            if score < minVal:
                minVal = score
            if minVal <= alpha:
                return minVal
            else:
                if(BloomCheckerFirst):
                    hashValue = Utils.HashingOperation.BoardToHashCode(board)
                    res_contain = player._bloomTable.__contains__(key=hashValue)
                    if(not res_contain and beta >= AlphaBeta.__minValueForInstanciation__()):
#                        print("Instanciate a table with the score", score)  
                        player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
                 
        
            if minVal > beta:
                beta = minVal
#                 beta = self.__synch_update_beta__(minVal)
                    
            if (time.time() - self.startTime > __MaxAllowedTimeInSeconds__):
                break
                    
            
        return minVal
      
      

