'''
Created on 20 nov. 2019
 
@author: jordane
'''
from multiprocessing import Queue, Process, Lock

from bloom import __utils__ as Utils
from game.board import Reversi
from intelligence.heuristics.stability import StableHeuristic as heuristic


lock = Lock()
 
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
        return 0
    
    @staticmethod
    def __beta__():
        return 100
    
    @classmethod
    def __minValueForInstanciation__(self):
        return 99.98

    
#     def AlphaBetaWrapper(player, InitDepth = 0, MaxDepth = 8, Parallelization = False):
#         player._maxDepth = MaxDepth
#         return player.MaxAlphaBeta(InitDepth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), Parallelization)
        
    @classmethod
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
            score = bestscore
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
                    #remove the element from the bloom filter
                    #auto return move ?
                    
                
            if(Parallelization):                 
                proc = Process(target=player.alphaBetaParallelizationWrapper,  args=(player, depth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), m, q, BloomCheckerFirst))
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
            tout=.5000
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
            

        return (bestscore,return_move)



    @classmethod
    def alphaBetaNoParallelizationWrapper(self, player, depth, alpha, beta, move, BloomCheckerFirst):
        score = AlphaBeta.max_score_alpha_beta(player, player._board, depth, alpha, beta, BloomCheckerFirst)
        if score > alpha:            
            alpha = score
        return (alpha)
    
    
    @classmethod
    def alphaBetaParallelizationWrapper(self, player, depth, alpha, beta, move, queue, BloomCheckerFirst):
        copiedBoard = AlphaBeta.__CopyCurrentBoard__()
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
                    return 100
                
                else:   #lose board
                    return -101
            else:       #win board
                if nbW > nbB:                
                    if(BloomCheckerFirst):
                        hashValue = Utils.HashingOperation.BoardToHashCode(board)
                        res_contain = player._bloomTable.__contains__(key=hashValue)
                        if(not res_contain):
                            player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
                    return 100
                
                else:   #lose board
                    return -101
            
        if depth == 0:  # leaves of alpha-beta pruning         
            op = player._board._flip(player._mycolor)
            score =  heuristic.stability(player._board, op)
#             score = (evaluator.getHeuristicValue(player, len(moves)))


            
            if(BloomCheckerFirst):
                hashValue = Utils.HashingOperation.BoardToHashCode(board)
                res_contain = player._bloomTable.__contains__(key=hashValue)
                if(not res_contain and score > AlphaBeta.__minValueForInstanciation__()):
                    player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
            return score
        
        maxVal = AlphaBeta.__alpha__()
        
        
        for move in moves:          
            board.push(move)
            score = AlphaBeta.min_score_alpha_beta(player, board, depth-1, alpha, beta, BloomCheckerFirst)
            board.pop()
            
            maxVal = max(maxVal, score)
            alpha = max(alpha, maxVal)
            if alpha >= beta:
                return maxVal                    
            
        return alpha


    @classmethod
    def min_score_alpha_beta(self, player, board, depth, alpha, beta, BloomCheckerFirst):
        moves = board.legal_moves()
        
        if board.is_game_over():
            (nbB, nbW) = board.get_nb_pieces()
            if player._mycolor is Reversi.Board._BLACK:
                if nbB > nbW:
                    return 100
                else:
                    return -100
            else:
                if nbW > nbB:
                    return 100
                else:
                    return -100
                
        if depth == 0:
            op = player._board._flip(player._mycolor)
            return heuristic.stability(player._board, op)
        
        
        minVal = AlphaBeta.__beta__()
        
        for move in moves:         
            board.push(move)
            score = AlphaBeta.max_score_alpha_beta(player, board, depth-1, alpha, beta, BloomCheckerFirst)
            board.pop()
            
                    
                    
            minVal = min(minVal, score)
            beta = min(beta, minVal)
            if beta <= alpha:
                return minVal
            else:
                if(BloomCheckerFirst):
                    hashValue = Utils.HashingOperation.BoardToHashCode(board)
                    res_contain = player._bloomTable.__contains__(key=hashValue)
                    if(not res_contain and beta >= player.__minValueForInstanciation__()):
#                        print("Instanciate a table with the score", score)  
                        player._bloomTable.add(key=Utils.HashingOperation.BoardToHashCode(board))
                
            
        return beta
      
      
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        ''' bullshit code sorry not sorry
#         
# 
#     @staticmethod
#     def __alpha__(self):
#         return -1000000
#     
#     @staticmethod
#     def __beta__(self):
#         return 10000000
# 
#     
#     def AlphaBetaWrapper(self, InitDepth = 0, MaxDepth = 8, Parallelization = False):
#         self._maxDepth = MaxDepth
#         return self.MaxAlphaBeta(InitDepth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), Parallelization)
#         
#         
# #https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
#     @classmethod
#     def MaxAlphaBeta(self, alpha, beta, depth, parallelization = False):
# #         global alpha_beta_maxDepth
# #         time.sleep(1)
#         # 10  : win
#         # 0   : draw
#         # -10 : lose
#         maxValue =  self.__alpha__()
#         moves = self._player._board.legal_moves()
#         if depth == self._maxDepth or len(moves) == 0:
#             (val) = (evaluator.get_corner_score(self))
#             print("Reached End MaxAlpha with val:", val)
# #             time.sleep(1)
# #             print("Move: with val:", val)
#             return (val, None)
#         
#         move = None
# 
#         self._bloomTable.__iadd__(key=Utils.HashingOperation.BoardToHashCode(self._player._board))
# 
#         for m in moves:
# #             print("Alpha:",alpha, flush=True)
# #             print("Beta:",beta, flush=True)
#             
#             lock.acquire()
#             self._player._board.push(m)
#             lock.release()
#             if(depth < self._maxDepth):
#                 if(parallelization):
# #                     p_args = [alpha, beta, depth]
#                     
# #                     processPool.map(self.MinAlphaBeta_wrapper,  ([alpha, beta, depth +1 ]))
#                     q = Queue()
#                     proc = Process(target=self.MinAlphaBeta_wrapper,  args=(alpha, beta, depth + 1, q))
#                     proc.start()
#                     value = q.get()
#                     proc.join(15000)
# #                     value = processPool.map_async(self.MinAlphaBeta_wrapper,  [(alpha, beta, depth +1)])
# #                     value = value.get()
# #                     print("Launched Pool.", flush=True)
# #                     sys.stdout.flush()
# #                     time.sleep(10)
# #                     value = self.MinAlphaBeta(alpha, beta, depth+1)
# #                     sys.stdout.flush()
#                     
#                     lock.acquire()
#     #                 if(depth == alpha_beta_maxDepth):
#     #                     value += self.applyBiais(m)
#                         
#                     if(value > maxValue):
#                         maxValue = value
#                         move = m
#                         
#                     lock.release()
#                     
#                 else:
#                     value = self.MinAlphaBeta(alpha, beta, depth + 1)
#     #                 if(depth == alpha_beta_maxDepth):
#     #                     value += self.applyBiais(m)
#                         
#                     if(value > maxValue):
#                         maxValue = value
#                         move = m
#                         
#                     
#             lock.acquire()
#             self._player._board.pop()
#             lock.release()
#             
#             
#             
#             if (maxValue >= beta):
#                 print("Nop at depth:", depth)
#                 return (maxValue, move)
#             
#             if(maxValue > alpha):
#                 alpha = maxValue
#                 
#         return (maxValue, move)
# 
#     @classmethod
#     def MinAlphaBeta_wrapper(self, a,b,d,q):
#         q.put(self.MinAlphaBeta_pool(a,b,d))
# 
#     @classmethod
#     def MinAlphaBeta_pool(self, alpha, beta, depth):
# #         global self._maxDepth
#         
#         # 10  : win
#         # 0   : draw
#         # -10 : lose
#         minValue = self.__beta__()
#         
#         moves = self._player._board.legal_moves()
#         if depth == self._maxDepth or len(moves) == 0:
#             (val) = (evaluator.get_corner_score(self))
#             print("Reached End MinAlpha with val:", val)
# #             time.sleep(1)
#             return (val)
#         
#         for m in self._player._board.legal_moves():
# #             print("Alpha:",alpha, flush=True)
# #             print("Beta:",beta, flush=True)
# #             time.sleep(0.5)
#             lock.acquire()
#             self._player._board.push(m)
#             lock.release()
#               
#             if(depth <= self._maxDepth):
#                 (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1, parallelization=False)
# #                 if(depth == alpha_beta_maxDepth):
# #                     value += self.applyBiais(m)
#                 if(value < minValue):
#                     minValue = value#self.getNumberPoints(m)
#             lock.acquire()
#             self._player._board.pop()
#             lock.release()
#               
#               
#             if (minValue <= alpha):
#                 print("Nop at min depth:", depth)
#                 return minValue
#               
#             if(minValue < beta):
#                 beta = minValue
#         return minValue
# 
# #         moves = [m for m in self._board.legal_moves()]
# #         
# #         return 1
#     @classmethod
#     def MinAlphaBeta(self, alpha, beta, depth):
# #         global self._maxDepth
# #         print("TODO")
#         # 10  : win
#         # 0   : draw
#         # -10 : lose
#         minValue =  self.__beta__()
#         
#         moves = self._player._board.legal_moves()
#         if depth == self._maxDepth or len(moves) == 0:
#             (val) = (evaluator.get_corner_score(self))
#             print("Reached End MinAlpha with val:", val)
# #             time.sleep(1)
#             return (val)
#         
#         for m in self._player._board.legal_moves():
# #             print("Alpha:",alpha, flush=True)
# #             print("Beta:",beta, flush=True)
# #             time.sleep(0.5)
#             lock.acquire()
#             self._player._board.push(m)
#             lock.release()
#             
#             if(depth < self._maxDepth):
#                 (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1)
# #                 if(depth == alpha_beta_maxDepth):
# #                     value += self.applyBiais(m)
#                 if(value < minValue ):
#                     minValue = value#self.getNumberPoints(m)
#             lock.acquire()
#             self._player._board.pop()
#             lock.release()
#             
#             
#             if (minValue <= alpha):
#                 print("Nop at min depth:", depth)
#                 return minValue
#             
#             if(minValue < beta):
#                 beta = minValue
#         return minValue
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
# #     
# # #https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
# #     def MaxAlphaBeta(self, alpha, beta, depth, parallelization = False):
# # #         global alpha_beta_maxDepth
# # #         time.sleep(1)
# #         # 10  : win
# #         # 0   : draw
# #         # -10 : lose
# #         maxValue =  alpha
# #         moves = self._board.legal_moves()
# #         move = None
# #         
# #         if depth == self._maxDepth:# or len(moves) == 0:
# #             (val) = (evaluator.getHeuristicValue(self, len(moves)))
# #             return (val, move)
# #         
# # 
# # #         self._bloomTable.__iadd__(key=Utils.HashingOperation.BoardToHashCode(self._board))
# #         for m in moves:
# # #             print("Alpha:",alpha, flush=True)
# # #             print("Beta:",beta, flush=True)
# #             
# #             lock.acquire()
# #             self._board.push(m)
# #             lock.release()
# #             if(depth < self._maxDepth):
# #                 if(parallelization):
# #                     q = Queue()
# #                     
# #                     proc = Process(target=self.MinAlphaBeta_wrapper,  args=(alpha, beta, depth +1, q))
# #                     proc.join()
# #                     proc.start()
# #                     
# #                     (value, _) = q.get()
# #                     
# #                     lock.acquire()
# #                         
# #                     if(value > maxValue):
# #                         maxValue = value
# #                         move = m
# #                         
# #                     lock.release()
# #                     
# #         
# #                     
# #                 else:
# #                     (value, _) = self.MinAlphaBeta(alpha, beta, depth +1 )
# #                         
# #                     if(value > maxValue):
# #                         maxValue = value
# #                         move = m
# #                         
# #             
# #             lock.acquire()
# #             self._board.pop()
# #             lock.release()
# #             
# #         
# #             if (maxValue >= beta):
# # #                 print("Nop at depth:", depth)
# #                 return (maxValue, move)
# #              
# #             if(maxValue > alpha):
# # #                 print("Alpha ", alpha, " -> ", maxValue)
# #                 alpha = maxValue
# #             
# #                 
# # #         print("Nop2 at depth:", depth)
# #         return (maxValue, move)
# # 
# #     def MinAlphaBeta_wrapper(self, a,b,d,q):
# #         q.put(self.MinAlphaBeta_pool(a,b,d))
# # 
# #     def MinAlphaBeta_pool(self, alpha, beta, depth):
# # #         global self._maxDepth
# #         
# #         # 10  : win
# #         # 0   : draw
# #         # -10 : lose
# #         minValue = beta
# #         
# #         moves = self._board.legal_moves()
# #         move = None
# #         if depth == self._maxDepth:# or len(moves) == 0:
# #             (val) = (evaluator.getHeuristicValue(self, len(moves)))
# # #             print("Reached End MinAlpha with val:", val)
# # #             time.sleep(1)
# #             return (val, move)
# #         
# #         value = 0
# #         for m in self._board.legal_moves():
# # #             print("Alpha:",alpha, flush=True)
# # #             print("Beta:",beta, flush=True)
# # #             time.sleep(0.5)
# #             lock.acquire()
# #             self._board.push(m)
# #             lock.release()
# #               
# #             if(depth <= self._maxDepth):
# #                 (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1, parallelization=False)
# # #                 value += v
# # #                 if(depth == alpha_beta_maxDepth):
# # #                     value += self.applyBiais(m)
# #                 if(value < minValue):
# #                     move = m
# #                     minValue = value#self.getNumberPoints(m)
# #             lock.acquire()
# #             self._board.pop()
# #             lock.release()
# #               
# #               
# #             if (minValue <= alpha):
# # #                 print("Nop at min depth:", depth)
# #                 return (minValue, move)
# #               
# #             if(minValue < beta):
# #                 beta = minValue
# #         return (minValue, move)
# # 
# # #         moves = [m for m in self._board.legal_moves()]
# # #         
# # #         return 1
# # 
# # 
# #     def MinAlphaBeta(self, alpha, beta, depth):
# #         minValue =  beta
# #         
# #         moves = self._board.legal_moves()
# #         move = None
# #         if depth == self._maxDepth:# or len(moves) == 0:
# #             (val) = (evaluator.getHeuristicValue(self, len(moves)))
# # #             print("Reached End MinAlpha with val:", val)
# # #             time.sleep(1)
# #             return (val, move)
# #         value = 0
# #         for m in self._board.legal_moves():
# #             if(depth < self._maxDepth -1):
# #                 lock.acquire()
# #                 self._board.push(m)
# #                 lock.release()
# #             
# #                 (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1)
# #                 
# #                 lock.acquire()
# #                 self._board.pop()
# #                 lock.release()
# #             else:
# #                 lock.acquire()
# #                 self._board.push(m)
# #                 lock.release()
# #             
# #                 (v,_) = self.MaxAlphaBeta(alpha, beta, depth + 1)
# #                 value += v
# #                 
# #                 lock.acquire()
# #                 self._board.pop()
# #                 lock.release()
# #             
# #             if(value < minValue ):
# #                 minValue = value
# #                 move = m
# #             if (minValue <= alpha):
# #                 return (minValue, move)
# #                  
# #             if(minValue < beta):
# #                 beta = minValue
# #                 
# #         return (minValue, move)
# #             
# #             
# #             
#             

'''