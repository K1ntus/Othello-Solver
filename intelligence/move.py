'''
Created on 17 nov. 2019

@author: jordane
'''
from IPython.utils.py3compat import xrange
from random import randint
import time

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
    def __init__(self):
        self._bloom = BloomFilter(max_elements=10000, error_rate=0.1, filename=None, start_fresh=False)
        self.InstanciateHashMoveList()
    

    def GetMove(self, reversi_board):
        res_contain = self._bloom.__contains__(key=Utils.HashingOperation.BoardToHashCode(reversi_board))
        if(res_contain):
            print("YEAH ! I Contain ", Utils.HashingOperation.BoardToHashCode(reversi_board))
            time.sleep(2)
        else:
            print("Nope")
            time.sleep(2)
        return None
    
    
    
    def InstanciateHashMoveList(self):        
        openingMoveArray = self.GetOpeningMoveList()
        for input_str in openingMoveArray:
            self._bloom.add(key=Utils.HashingOperation.StringToHashCode(input_str))
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
    def GetOpeningMoveList(self):
        #diagonal opening
        opening_moves = []
        diagonalOpenings = [
                "C4c3",             # Diagonal Opening
                "C4c3D3",           # Diagonal Opening +
                "C4c3D3c5",         # Diagonal Opening ++
                
                
                # Variations linked to Diagonal Opening ++
                "C4c3D3c5D6",           # Cow
                "C4c3D3c5D6e3",         # Chimney
                "C4c3D3c5D6f4",         # Cow +
                "C4c3D3c5D6f4F5",       # Rose-v-Toth
                "C4c3D3c5D6f4F5d2",     # Tanida
                "C4c3D3c5D6f4",         # Cow Bat/Bat/Cambridge
                "C4c3D3c5D6f4F5d2B5",   # Aircraft/Feldborg
                # End
                
                
                "C4c3D3c5B4",       # Heath/Tobidashi
                "C4c3D3c5B4d2",     # Heath/Tobidashi +
                "C4c3D3c5B4d2D6",   # Heath-Bat
                "C4c3D3c5B4e3",     # Heath-Chimney
                "C4c3D3c5B4d2E2"    # Iwasaki Variation          
            
            ]
        
        opening_moves += diagonalOpenings
        return opening_moves
        
        
        
        
        
        
        
        
        
        
        