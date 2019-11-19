'''
Created on 17 nov. 2019

@author: jordane
'''
from random import randint


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
        max_value = player.getNumberPoints(best_move) + MoveManager.applyBiais(player._board, player._mycolor, best_move)
        for m in moves:
            current = player.getNumberPoints(m)
            if(current > max_value):
                max_value = current
                best_move = m
    
        return (best_move, max_value)
    
    @classmethod
    def applyBiais(self, _board, _mycolor, move):
        (_, x, y) = move
        value = 0
        lr_border = False
        tb_border = False
           
        if(x == 0 or x == 9): #left or right border
            value += 1
            lr_border = True
               
        if(y == 0 or y == 9): #top or bottom border
            value += 1
            tb_border = True
               
               
        if(x == 1 or x == 8): #left or right border
            value -= 2
            lr_border = False
               
        if(y == 1 or y == 8): #top or bottom border
            value -= 2
            tb_border = False
           
        if(tb_border and lr_border):
            value += 10
          
        if(_board.is_game_over()):
             
            (nbwhites, nbblacks) = _board.get_nb_pieces()
                 
            if(_mycolor == 1 and nbblacks > nbwhites): #black
                value +=100
            else:
                return -5
 
         
        return value
        
        
        
        
        
        
        
        
        