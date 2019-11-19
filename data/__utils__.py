'''
Created on 17 nov. 2019

@author: jordane

https://llimllib.github.io/bloomfilter-tutorial/
'''
import hashlib

import Reversi


_BLACK = 1
_WHITE = 2
_EMPTY = 0
class HashingOperation(object):
    '''
    classdocs
    '''

    @staticmethod
    def BoardToHashCode(reversi_game):
        board_str = HashingOperation.board_to_str(reversi_game)
        return HashingOperation.StringToHashCode(board_str)
    
    @staticmethod
    def StringToHashCode(board_str):
#         print("Board is: ", board_str)
        byte_str = str.encode(board_str)
        type(byte_str)
        h = byte_str.hex()
#         h = hashlib.sha256(byte_str)
#         print("Bloom key Instanciated: ", h)
#         print("")
        return h
#         return int(h.hexdigest(), base=16) 
#         return int(byte_str.hexdigest(), base=16) 
    
    
    
    
    
    @staticmethod
    def IndiceToChar(int_value):
        convertTable = {
            1:'a',
            2:'b',
            3:'c',
            4:'d',
            5:'e',
            6:'f',
            7:'g',
            8:'h',
            9:'i',
            10:'j'
            
            }
        
        return convertTable[int_value]
    
    @staticmethod
    def CharToIndice(char):
        convertTable = {
            'A':1, 'a':1,
            'B':2, 'b':2,
            'C':3, 'c':3,
            'D':4, 'd':4,
            'E':5, 'e':5,
            'F':6, 'f':6,
            'G':7, 'g':7,
            'H':8, 'h':8,
            'I':9, 'i':9,
            'J':10, 'j':10
            
            }
        
        return convertTable[char]
    
    @staticmethod
    def _piece2str(c, x, y):        
        x = HashingOperation.IndiceToChar(x)        
        
        if c==_WHITE:
            x = x.upper()
        elif c==_BLACK:
            x = x.lower()
        else:
            return ''
        return x + str(y)
#     
#     @staticmethod
#     def _str2piece(str):  
#         c = None
#         x = HashingOperation.CharToIndice(str.)
#         y = 0      
#         x = HashingOperation.IndiceToChar(x)        
#         
#         if c==_WHITE:
#             x = x.upper()
#         elif c==_BLACK:
#             x = x.lower()
#         else:
#             return ''
#         return (c,x,y)
#         
        
        

    @staticmethod
    def board_to_str(reversi_game):
        toreturn=""
        y = 1
        for l in reversi_game._board:
            x = 1
            for c in l:
                toreturn += HashingOperation._piece2str(c, x, y)
                x+=1
            y +=1
        return toreturn

    
        