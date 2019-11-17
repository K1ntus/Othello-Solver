'''
Created on 17 nov. 2019

@author: jordane

https://llimllib.github.io/bloomfilter-tutorial/
'''
import hashlib

_BLACK = 1
_WHITE = 2
_EMPTY = 0
class HashingOperation(object):
    '''
    classdocs
    '''

    @staticmethod
    def generateHashCode(reversi_game):
        board_str = HashingOperation.board_to_str(reversi_game)
        print("Bloom key is: ")
        print(board_str)
        byte_str = str.encode(board_str)
        type(byte_str)
        h = hashlib.sha256(byte_str)
        print("Bloom key became: ")
        print(h)
        return int(h.hexdigest(), base=16) 
    
    
    
    
    @staticmethod
    def _piece2str(c):
        if c==_WHITE:
            return 'O'
        elif c==_BLACK:
            return 'X'
        else:
            return '.'

    @staticmethod
    def board_to_str(reversi_game):
        toreturn=""
        for l in reversi_game._board:
            for c in l:
                toreturn += HashingOperation._piece2str(c)
#             toreturn += "\n"
        return toreturn

    
        