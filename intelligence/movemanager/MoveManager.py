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
        max_value = player.getNumberPoints(best_move) + player.applyBiais(best_move)
        for m in moves:
            current = player.getNumberPoints(m)
            if(current > max_value):
                max_value = current
                best_move = m
    
        return (best_move, max_value)
    
    

        
        
        
        
        
        
        
        
        