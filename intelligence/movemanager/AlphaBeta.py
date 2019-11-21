'''
Created on 20 nov. 2019

@author: jordane
'''
from multiprocessing import Queue, Process, Lock
import time

from intelligence.heuristics import evaluator
from bloom import __utils__ as Utils

lock = Lock()

class AlphaBeta:

    def __init__(self, player):
        self._player = player
        self._board = player._board
        self._mycolor = player._mycolor
        
        self._bloomTable = player._bloomTable
        self._maxDepth = 8
        
    def __update__(self, player, MaxDepth = 8):
        self._player = player
        self._board = player._board
        self._mycolor = player._mycolor
        
        self._bloomTable = player._bloomTable
        self._maxDepth = MaxDepth
        

    @staticmethod
    def __alpha__(self):
        return -1000000
    
    @staticmethod
    def __beta__(self):
        return 10000000

    
    def AlphaBetaWrapper(self, InitDepth = 0, MaxDepth = 8, Parallelization = False):
        self._maxDepth = MaxDepth
        return self.MaxAlphaBeta(InitDepth, AlphaBeta.__alpha__(), AlphaBeta.__beta__(), Parallelization)
        
        
#https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
    @classmethod
    def MaxAlphaBeta(self, alpha, beta, depth, parallelization = False):
#         global alpha_beta_maxDepth
#         time.sleep(1)
        # 10  : win
        # 0   : draw
        # -10 : lose
        maxValue =  self.__alpha__()
        moves = self._player._board.legal_moves()
        if depth == self._maxDepth or len(moves) == 0:
            (val) = (evaluator.get_corner_score(self))
            print("Reached End MaxAlpha with val:", val)
#             time.sleep(1)
#             print("Move: with val:", val)
            return (val, None)
        
        move = None

        self._bloomTable.__iadd__(key=Utils.HashingOperation.BoardToHashCode(self._player._board))

        for m in moves:
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
            
            lock.acquire()
            self._player._board.push(m)
            lock.release()
            if(depth < self._maxDepth):
                if(parallelization):
#                     p_args = [alpha, beta, depth]
                    
#                     processPool.map(self.MinAlphaBeta_wrapper,  ([alpha, beta, depth +1 ]))
                    q = Queue()
                    proc = Process(target=self.MinAlphaBeta_wrapper,  args=(alpha, beta, depth + 1, q))
                    proc.start()
                    value = q.get()
                    proc.join(15000)
#                     value = processPool.map_async(self.MinAlphaBeta_wrapper,  [(alpha, beta, depth +1)])
#                     value = value.get()
#                     print("Launched Pool.", flush=True)
#                     sys.stdout.flush()
#                     time.sleep(10)
#                     value = self.MinAlphaBeta(alpha, beta, depth+1)
#                     sys.stdout.flush()
                    
                    lock.acquire()
    #                 if(depth == alpha_beta_maxDepth):
    #                     value += self.applyBiais(m)
                        
                    if(value > maxValue):
                        maxValue = value
                        move = m
                        
                    lock.release()
                    
                else:
                    value = self.MinAlphaBeta(alpha, beta, depth + 1)
    #                 if(depth == alpha_beta_maxDepth):
    #                     value += self.applyBiais(m)
                        
                    if(value > maxValue):
                        maxValue = value
                        move = m
                        
                    
            lock.acquire()
            self._player._board.pop()
            lock.release()
            
            
            
            if (maxValue >= beta):
                print("Nop at depth:", depth)
                return (maxValue, move)
            
            if(maxValue > alpha):
                alpha = maxValue
                
        return (maxValue, move)

    @classmethod
    def MinAlphaBeta_wrapper(self, a,b,d,q):
        q.put(self.MinAlphaBeta_pool(a,b,d))

    @classmethod
    def MinAlphaBeta_pool(self, alpha, beta, depth):
#         global self._maxDepth
        
        # 10  : win
        # 0   : draw
        # -10 : lose
        minValue = self.__beta__()
        
        moves = self._player._board.legal_moves()
        if depth == self._maxDepth or len(moves) == 0:
            (val) = (evaluator.get_corner_score(self))
            print("Reached End MinAlpha with val:", val)
#             time.sleep(1)
            return (val)
        
        for m in self._player._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._player._board.push(m)
            lock.release()
              
            if(depth <= self._maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1, parallelization=False)
#                 if(depth == alpha_beta_maxDepth):
#                     value += self.applyBiais(m)
                if(value < minValue):
                    minValue = value#self.getNumberPoints(m)
            lock.acquire()
            self._player._board.pop()
            lock.release()
              
              
            if (minValue <= alpha):
                print("Nop at min depth:", depth)
                return minValue
              
            if(minValue < beta):
                beta = minValue
        return minValue

#         moves = [m for m in self._board.legal_moves()]
#         
#         return 1
    @classmethod
    def MinAlphaBeta(self, alpha, beta, depth):
#         global self._maxDepth
#         print("TODO")
        # 10  : win
        # 0   : draw
        # -10 : lose
        minValue =  self.__beta__()
        
        moves = self._player._board.legal_moves()
        if depth == self._maxDepth or len(moves) == 0:
            (val) = (evaluator.get_corner_score(self))
            print("Reached End MinAlpha with val:", val)
#             time.sleep(1)
            return (val)
        
        for m in self._player._board.legal_moves():
#             print("Alpha:",alpha, flush=True)
#             print("Beta:",beta, flush=True)
#             time.sleep(0.5)
            lock.acquire()
            self._player._board.push(m)
            lock.release()
            
            if(depth < self._maxDepth):
                (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1)
#                 if(depth == alpha_beta_maxDepth):
#                     value += self.applyBiais(m)
                if(value < minValue ):
                    minValue = value#self.getNumberPoints(m)
            lock.acquire()
            self._player._board.pop()
            lock.release()
            
            
            if (minValue <= alpha):
                print("Nop at min depth:", depth)
                return minValue
            
            if(minValue < beta):
                beta = minValue
        return minValue
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     
# #https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
#     def MaxAlphaBeta(self, alpha, beta, depth, parallelization = False):
# #         global alpha_beta_maxDepth
# #         time.sleep(1)
#         # 10  : win
#         # 0   : draw
#         # -10 : lose
#         maxValue =  alpha
#         moves = self._board.legal_moves()
#         move = None
#         
#         if depth == self._maxDepth:# or len(moves) == 0:
#             (val) = (evaluator.getHeuristicValue(self, len(moves)))
#             return (val, move)
#         
# 
# #         self._bloomTable.__iadd__(key=Utils.HashingOperation.BoardToHashCode(self._board))
#         for m in moves:
# #             print("Alpha:",alpha, flush=True)
# #             print("Beta:",beta, flush=True)
#             
#             lock.acquire()
#             self._board.push(m)
#             lock.release()
#             if(depth < self._maxDepth):
#                 if(parallelization):
#                     q = Queue()
#                     
#                     proc = Process(target=self.MinAlphaBeta_wrapper,  args=(alpha, beta, depth +1, q))
#                     proc.join()
#                     proc.start()
#                     
#                     (value, _) = q.get()
#                     
#                     lock.acquire()
#                         
#                     if(value > maxValue):
#                         maxValue = value
#                         move = m
#                         
#                     lock.release()
#                     
#         
#                     
#                 else:
#                     (value, _) = self.MinAlphaBeta(alpha, beta, depth +1 )
#                         
#                     if(value > maxValue):
#                         maxValue = value
#                         move = m
#                         
#             
#             lock.acquire()
#             self._board.pop()
#             lock.release()
#             
#         
#             if (maxValue >= beta):
# #                 print("Nop at depth:", depth)
#                 return (maxValue, move)
#              
#             if(maxValue > alpha):
# #                 print("Alpha ", alpha, " -> ", maxValue)
#                 alpha = maxValue
#             
#                 
# #         print("Nop2 at depth:", depth)
#         return (maxValue, move)
# 
#     def MinAlphaBeta_wrapper(self, a,b,d,q):
#         q.put(self.MinAlphaBeta_pool(a,b,d))
# 
#     def MinAlphaBeta_pool(self, alpha, beta, depth):
# #         global self._maxDepth
#         
#         # 10  : win
#         # 0   : draw
#         # -10 : lose
#         minValue = beta
#         
#         moves = self._board.legal_moves()
#         move = None
#         if depth == self._maxDepth:# or len(moves) == 0:
#             (val) = (evaluator.getHeuristicValue(self, len(moves)))
# #             print("Reached End MinAlpha with val:", val)
# #             time.sleep(1)
#             return (val, move)
#         
#         value = 0
#         for m in self._board.legal_moves():
# #             print("Alpha:",alpha, flush=True)
# #             print("Beta:",beta, flush=True)
# #             time.sleep(0.5)
#             lock.acquire()
#             self._board.push(m)
#             lock.release()
#               
#             if(depth <= self._maxDepth):
#                 (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1, parallelization=False)
# #                 value += v
# #                 if(depth == alpha_beta_maxDepth):
# #                     value += self.applyBiais(m)
#                 if(value < minValue):
#                     move = m
#                     minValue = value#self.getNumberPoints(m)
#             lock.acquire()
#             self._board.pop()
#             lock.release()
#               
#               
#             if (minValue <= alpha):
# #                 print("Nop at min depth:", depth)
#                 return (minValue, move)
#               
#             if(minValue < beta):
#                 beta = minValue
#         return (minValue, move)
# 
# #         moves = [m for m in self._board.legal_moves()]
# #         
# #         return 1
# 
# 
#     def MinAlphaBeta(self, alpha, beta, depth):
#         minValue =  beta
#         
#         moves = self._board.legal_moves()
#         move = None
#         if depth == self._maxDepth:# or len(moves) == 0:
#             (val) = (evaluator.getHeuristicValue(self, len(moves)))
# #             print("Reached End MinAlpha with val:", val)
# #             time.sleep(1)
#             return (val, move)
#         value = 0
#         for m in self._board.legal_moves():
#             if(depth < self._maxDepth -1):
#                 lock.acquire()
#                 self._board.push(m)
#                 lock.release()
#             
#                 (value, _) = self.MaxAlphaBeta(alpha, beta, depth + 1)
#                 
#                 lock.acquire()
#                 self._board.pop()
#                 lock.release()
#             else:
#                 lock.acquire()
#                 self._board.push(m)
#                 lock.release()
#             
#                 (v,_) = self.MaxAlphaBeta(alpha, beta, depth + 1)
#                 value += v
#                 
#                 lock.acquire()
#                 self._board.pop()
#                 lock.release()
#             
#             if(value < minValue ):
#                 minValue = value
#                 move = m
#             if (minValue <= alpha):
#                 return (minValue, move)
#                  
#             if(minValue < beta):
#                 beta = minValue
#                 
#         return (minValue, move)
#             
#             
#             
            

