'''
Created on 17 nov. 2019

@author: jordane
'''
from IPython.utils.py3compat import xrange
from random import randint
import time

from Reversi import Board
import Reversi
from data import __utils__ as Utils
from data.__utils__ import HashingOperation
from data.bloom_filter import BloomFilter


class MoveManager(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    @staticmethod
    def MoveForGameBeginning(player, moves):
        best_move = moves[randint(0,len(moves)-1)]
        max_value = player.getNumberPoints(best_move) + player.applyBiais(best_move)
        for m in moves:
            current = player.getNumberPoints(m)
            if(current > max_value):
                max_value = current
                best_move = m
    
        return (best_move, max_value)
    
    
#http://www.samsoft.org.uk/reversi/openings.htm
class OpeningMove(object):
    def __init__(self, color):
        self._bloom = BloomFilter(max_elements=10000, error_rate=0.1, filename=None, start_fresh=False)
        self.InstanciateHashMoveList(color)
    

    def GetMove(self, board):
        hashValue = Utils.HashingOperation.BoardToHashCode(board)
        res_contain = self._bloom.__contains__(key=hashValue)
        if(res_contain):
            print("YEAH ! I Contain ", hashValue, flush=True)
#             time.sleep(20)
        else:
            print("Nope, I do not have the key : ", hashValue, flush=True)
#             time.sleep(2)
        return None
    
    
    
    def InstanciateHashMoveList(self, color):        
        openingMoveArray = self.GetOpeningMoveList(color)
        for input_str in openingMoveArray:
            self._bloom.add(key=Utils.HashingOperation.StringToHashCode(input_str.swapcase()))
        return
    
    
    
    @classmethod
    def MoveStringToHash(input_str):
        _board = Reversi.Board(10)
        
        for char_id in xrange(0, len(input_str), 2):
            (x_and_color, posY) = input_str[char_id:char_id+1]
            (color, x, y) = (0, 0, posY)
            
            
            if(x_and_color.isupper()): #then white
                color = _board._WHITE
            else: 
                color = _board._BLACK
                
            x = OpeningMove.CharConvertTable(x_and_color)
            
            _board.push(color, x, y)
        
        return HashingOperation.board_to_str(_board)
    
    
    @classmethod
    def GetOpeningMoveList(self, color):
        #diagonal opening
        opening_moves = []
        diagonalOpenings = [
                "d4D5e5F5E6f6",             # Diagonal Opening
                "d4E4D5E5F5E6f6",           # Diagonal Opening +
                "d4E4d5E5F5d6e6f6",         # Diagonal Opening ++
                
                
                # Variations linked to Diagonal Opening ++
                "d4E4d5E5F5d6E6f6E7",           # Cow
                "d4e4f4d5e5f5d6E6f6E7",         # Chimney
                "d4E4d5e5f5g5d6E6f6E7",         # Cow +
#                 "e3d4e4C5D5e5F5d6e6f6",       # Rose-v-Toth
#                 "C4c3D3c5D6f4F5d2",     # Tanida
#                 "C4c3D3c5D6f4",         # Cow Bat/Bat/Cambridge
#                 "C4c3D3c5D6f4F5d2B5",   # Aircraft/Feldborg
#                 # End
#                 
#                 
                "d4E4C5D5E5F5d6e6f6",       # Heath/Tobidashi
                "e3d4e4C5D5e5F5d6e6f6",     # Heath/Tobidashi +
#                 "C4c3D3c5B4d2D6",   # Heath-Bat
#                 "C4c3D3c5B4e3",     # Heath-Chimney
#                 "C4c3D3c5B4d2E2"    # Iwasaki Variation          
            
            ]
#         
#         parallelOpenings = [
#             "C4c5",
#             "C4c5D6"
#             ]
#         
#         perpendicularOpenings = [
#             "C4e3F6e6F5g6E7c5",
#             "C4e3F6e6F5g6",
#             "C4e3F6e6F5c5F4g6F7g5",
#             "C4e3F6e6F5c5F4g6F7d3",
#             "C4e3F6e6F5c5F4g6F7",
#             "C4e3F6e6F5c5F4g5G4f3C6d3D6b3C3b4E2b6",
#             "C4e3F6e6F5c5F4g5G4f3C6d3D6",
#             "C4e3F6e6F5c5D6",
#             "C4e3F6e6F5c5D3",
#             "C4e3F6e6F5c5C3g5",
#             "C4e3F6e6F5c5C3c6D6",
#             "C4e3F6e6F5c5C3c6D3d2E2b3C1c2B4a3A5b5A6a4A2",
#             "C4e3F6e6F5c5C3c6",
#             "C4e3F6e6F5c5C3b4D6c6B5a6B6c7",
#             "C4e3F6e6F5c5C3b4",
#             "C4e3F6e6F5c5C3",
#             "C4e3F6e6F5",
#             "C4e3F6b4",
#             "C4e3F5e6F4c5D6c6F7g5G6",
#             "C4e3F5e6F4c5D6c6F7f3",
#             "C4e3F5e6F4",
#             "C4e3F5e6D3",
#             "C4e3F5b4F3f4E2e6G5f6D6c6",
#             "C4e3F5b4F3",
#             "C4e3F5b4",
#             "C4e3F4c5E6",
#             "C4e3F4c5D6f3E6c6",
#             "C4e3F4c5D6f3E6c3D3e2D2",
#             "C4e3F4c5D6f3E6c3D3e2B6f5G5f6",
#             "C4e3F4c5D6f3E6c3D3e2B6f5G5",
#             "C4e3F4c5D6f3E6c3D3e2B6f5B4f6G5d7",
#             "C4e3F4c5D6f3E6c3D3e2B6f5",
#             "C4e3F4c5D6f3E6c3D3e2B5f5B4f6C2e7D2c7",
#             "C4e3F4c5D6f3E6c3D3e2B5f5B3",
#             "C4e3F4c5D6f3E6c3D3e2B5f5",
#             "C4e3F4c5D6f3E6c3D3e2B5",
#             "C4e3F4c5D6f3E6c3D3e2",
#             "C4e3F4c5D6f3E2",
#             "C4e3F4c5D6f3D3c3",
#             "C4e3F4c5D6f3D3",
#             "C4e3F4c5D6f3C6",
#             "C4e3F4c5D6e6",
#             "C4e3"
#             ]
        
        opening_moves += diagonalOpenings
#         opening_moves += parallelOpenings
#         opening_moves += perpendicularOpenings
         
        if(color == Board._BLACK):
            return opening_moves
        return opening_moves
        
        
        
        
        
        
        
        
        
        
        