'''
Created on 20 nov. 2019
 
@author: jordane
'''
from multiprocessing import Queue, Process, Lock

from bloom import __utils__ as Utils
from game.board import Reversi
from intelligence.heuristics import eval
from ase.calculators.emt import beta


class AlphaBeta:
 
    def __init__(self, player):
        self._player = player
        self._board = player._board
        self._mycolor = player._mycolor
         
        self._bloomTable = player._bloomTable
         
    def __update__(self, player):
        self._player = player
        self._board = player._board
        self._mycolor = player._mycolor
         
        self._bloomTable = player._bloomTable
        
        
        
        


    @staticmethod
    def __alpha__():
        return -float('Inf')
    
    @staticmethod
    def __beta__():
        return float('Inf')
    
    @classmethod
    def __minValueForInstanciation__(self):
        return 99.95

    
#     def AlphaBetaWrapper(player, InitDepth = 0, MaxDepth = 8, Parallelization = False):
#         player._maxDepth = MaxDepth
#         return player.MaxAlphaBeta(InitDepth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), Parallelization)
        
    @staticmethod
    def __CopyCurrentBoard__(player):
        res = Reversi.Board(player._board._boardsize)        
        
        for x in range(0,res._boardsize,1):
            for y in range(0,res._boardsize,1):
                res._board[y][x] = player._board._board[y][x]
                
        return res
        
    @staticmethod
    def __alpha_beta_main_wrapper__(
            player, 
            depth = 3, #nb pair svp
            BloomCheckerFirst = False, 
            Parallelization   = False
        ):
        moves = player._board.legal_moves()


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
                    proc = Process(target=AlphaBeta.alphaBetaParallelizationWrapper,  args=(player, depth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), m, q, BloomCheckerFirst))
                    proc.start()
                    process_list.append(proc)
            else:

                (score)  = AlphaBeta.alphaBetaNoParallelizationWrapper(player, depth, bestscore, AlphaBeta.__beta__(), m, BloomCheckerFirst)
    
                if score > bestscore:
                    bestscore = score
                    return_move = move
                if bestscore >= AlphaBeta.__minValueForInstanciation__() and BloomCheckerFirst: #instanciate
                    player._board.push(m)
#                     print("Instanciate a table with the score", score)  
                    player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(player._board))
                    player._board.pop() 

                
        if(Parallelization):
            tout=5
#             tout = .5000/len(process_list)
            for proc in process_list:
                proc.join(timeout=tout)
            while q.qsize() > 0:
                (score,move) = q.get(block=False, timeout=.100)
                 
                if score > bestscore:
                    bestscore = score
                    return_move = move
                if bestscore >= AlphaBeta.__beta__():
                    return (bestscore, return_move)
            
        print("---------------------")
        return (bestscore,return_move)



    @classmethod
    def alphaBetaNoParallelizationWrapper(self, player, depth, alpha, beta, move, BloomCheckerFirst):
        player._board.push(move)
        score = AlphaBeta.max_score_alpha_beta(player, player._board, depth, alpha, beta, BloomCheckerFirst)
        if score > alpha:            
            alpha = score
        player._board.pop()
        return (alpha)
    
    
    @classmethod
    def alphaBetaParallelizationWrapper(self, player, depth, alpha, beta, move, queue, BloomCheckerFirst):
        copiedBoard = AlphaBeta.__CopyCurrentBoard__(player)
        score = AlphaBeta.max_score_alpha_beta(player, copiedBoard, depth, alpha, beta, BloomCheckerFirst)
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
            
        if depth == 0 or board.is_game_over():  # leaves of alpha-beta pruning          
            score =  eval.getTotal(player,player._mycolor)
            return score
             
            if(BloomCheckerFirst):
                hashValue = Utils.HashingOperation.BoardToHashCode(board)
                res_contain = player._bloomTable.__contains__(key=hashValue)
                if(not res_contain and score > AlphaBeta.__minValueForInstanciation__()):
                    player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
            return score
        
        maxVal = alpha
        
        
        for move in moves:       
            board.push(move)
            score = AlphaBeta.min_score_alpha_beta(player, board, depth-1, alpha, beta, BloomCheckerFirst)
            board.pop()
            
            if score > maxVal:
                maxVal = score
            if maxVal >= beta:
                return maxVal
        
            if maxVal > alpha:
                alpha = maxVal
                 
            
        return maxVal


    @classmethod
    def min_score_alpha_beta(self, player, board, depth, alpha, beta, BloomCheckerFirst):
        moves = board.legal_moves()
        
                
        if depth == 0 or board.is_game_over():
            return eval.getTotal(player,player._mycolor)
        
        minVal = beta
        
        for move in moves:         
            board.push(move)
            score = AlphaBeta.max_score_alpha_beta(player, board, depth-1, alpha, beta, BloomCheckerFirst)
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
                    
                    
            
        return minVal
      
      

