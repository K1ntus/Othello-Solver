#http://www.samsoft.org.uk/reversi/openings.htm
# from IPython.utils.py3compat import xrange
from random import randint
import time

from bloom import __utils__ as Utils
from bloom.__utils__ import HashingOperation
from bloom.bloom_filter import BloomFilter
from game.board import Reversi
from intelligence.movemanager import MovingData


class OpeningMove:
    ''' Class used to manage the opening move (ie. at the beginning of the game).
    We are currently using a bloom filter that will contains hashed board that we will
    compare with board after pushing a move to test
    '''
    def __init__(self, color):
        self._bloom = BloomFilter(max_elements=10000, error_rate=0.005, filename=None, start_fresh=False)
        self.InstanciateHashMoveList(color)
        
        
    @classmethod
    def fixStringForNewMove(self, toCompare, toUpdate):
        """Utils function to make readable a list of opening move by separating the hash 
        by substring of size 2"""
        for i in range(0, len(toCompare), 2):
            toUpdate.replace(toCompare[i:i+2], "")
    
        return toUpdate

    def GetMove(self, board):
        """
        Check if an opening move is available for the player depending of his available move
        
        We check if the board after a push is present in the bloom filters, 
            if it is, we append it to a list
            
        At he end, we return a random move from this result list.
        """
#         print("Board key: ", Utils.HashingOperation.board_to_str(board))

        currentBoardHashValue = Utils.HashingOperation.BoardToHashCode(board)
        res_contain = self._bloom.__contains__(key=currentBoardHashValue)
#         if(res_contain):
#         print("Search Opening move In The Bloom Filter", flush=True)
            
        moves = board.legal_moves()
        move = []
        find_a_move = False
    
            
        for m in moves:
            board.push(m)
                
                
            newBoardHashValue = Utils.HashingOperation.BoardToHashCode(board)
            updatedBoardHashValue = self.fixStringForNewMove(currentBoardHashValue, newBoardHashValue)
            res_contain = self._bloom.__contains__(key=updatedBoardHashValue)
            if(res_contain):
#                 print("Adding: ", updatedBoardHashValue, " -> ", Utils.HashingOperation.board_to_str(board), flush=True)
                move.append(m)
                find_a_move = True
#             else:
#                 print(Utils.HashingOperation.board_to_str(board), " -> ", updatedBoardHashValue)
            board.pop()
        if(find_a_move):
            return move[randint(0,len(move)-1)]
                
#         else:
#             print("Nope, I do not have the key : ", hashValue, flush=True)
#             return None
        print("No move has been predicted")

#         time.sleep(1)
        return None
    
    
    
    def InstanciateHashMoveList(self, color):    
        """
        Add an hashed board to the bloom filter managing the opening move
        """    
        openingMoveArray = self.GetOpeningMoveList(color)
        for input_str in openingMoveArray:
#             if(color == Board._WHITE):
#                 someString = input_str.swapcase()
#             else: 
#                 someString = input_str
            someString = input_str
            if(color is Reversi.Board._WHITE):
                someString.swapcase()
            h = Utils.HashingOperation.StringToHashCode(someString)
            self._bloom.add(key=h)
#             print("Instanciate: ", someString, " -> ", h)
        return
    
    
    
    @classmethod
    def MoveStringToHash(input_str):
        """
        convert a board+move to a hashed string that we will manage the color of the player.
        """
        _board = Reversi.Board(10)
        
        for char_id in range(0, len(input_str), 2):
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
        """Return an array of string corresponding to opening moves"""
#         return MovingData.OpeningMoveData.getMoveList()
        #diagonal opening
        opening_moves = ["e5F5E6f6"]
         
#         diagonalOpeningsWhite = [
#             "e5F5E6f6",
#             "f4e5f5E6f6"                    # DiagonalOpening
#             
#         ]
         
         
        diagonalOpeningsBlack = [
#                 "d4D5e5F5E6f6",           # Diagonal Opening ?good
                "f4e5f5E6f6",               # Diagonal Opening
                "E4f4e5f5E6f6",             # Diagonal Opening
                "f4G4e5F5E6f6",
                 
                "f4G4e5f5g5E6f6",           # Diagonal Opening +
                 
                "f4G4e5f5G5E6F6G6",         # Dialog Opening ++
                "E4F4G4E5f5g5E6f6",         # Dialog Opening ++
                 
                "f4G4e5f5g5h5E6F6G6",                
                "f3E4f4G4E5f5g5E6f6",       # Heath/Tobidashi
                "f4g4e5f5G5h5E6F6G6",       # Heath/Tobidashi +
                 
#                 "d4E4D5E5F5E6f6",           
#                 "d4E4d5E5F5d6e6f6",         # Diagonal Opening ++
#                 
#                 
#                 # Variations linked to Diagonal Opening ++
 
                "c4D4c5D5E5c6D6e6D7",           # Cow
                "c4d4e4c5d5e5c6D6e6D7",         # Chimney
                "c4D4c5d5e5f5c6D6e6D7",         # Cow +
                "d3c4d4B5C5d5E5c6d6e6",         # Rose-v-Toth
                "d3c4D4C5f5c6F6D7",             # Tanida
                "c4D4C5f5c6D7",                 # Cow Bat/Bat/Cambridge
                "d3c4D4C5B6f5c6D7F6",           # Aircraft/Feldborg  
 
#                 "d4E4d5E5F5d6E6f6E7",           # Cow
#                 "d4e4f4d5e5f5d6E6f6E7",         # Chimney
#                 "d4E4d5e5f5g5d6E6f6E7",         # Cow +
#                 "e3d4e4C5D5e5F5d6e6f6",         # Rose-v-Toth
#                 "D5d4E4d6E7g5G6e3",             # Tanida
#                 "D5d4E4d6E7g5",                 # Cow Bat/Bat/Cambridge
#                 "D5d4E4d6E7g5G6e3C6",           # Aircraft/Feldborg
 
#                 # End
 
#                 
#                 
#                 "d4E4C5D5E5F5d6e6f6",           # Heath/Tobidashi
#                 "e3d4e4C5D5e5F5d6e6f6",         # Heath/Tobidashi +
#                 "e3d4E4C5D4d6E7",               # Heath-Bat
                "f3E4f4G4E5F5G5E6F6G6",           # Heath-Chimney
                "E4F4G4d5e5f5g5h5E6F6G6",         # Heath-Chimney +
                "E4F4G4E5F5g5h5E6F6G6"
#                 "e3F3d4E4C5D5d6"                # Iwasaki Variation    
 
 
  
             
            ]
 
        
        parallelOpeningsBlack = [
            "E4f4E5f5E6f6",             # Parallel Opening
            "E4f4d5e5f5E6f6"            # Parallel Opening +
            ]
#         parallelOpeningsWhite = [
#             "E4f4E5f5E6f6",             # Parallel Opening
#             "d5e4f4e5f5E6f6"            # Parallel Opening +
#             ]
 
        
        perpendicularOpenings = [
            "f4e5f5E6F6G6",             # Perpendicular Opening (C4e3)
            "f4e5f5E6F6G6e7",           # Perpendicular Opening + (C4e3F5)
            "f4e5f5e6F6G6e7" ,          # Perpendicular Opening + (C4e3F6)
            "E4f4e5F5e6F6G6d7",         # Tiger +
            "E4f4e5f5e6f6G6d7f7",       # Tiger ++
            "E4f4e5F5e6f6g6h6d7",       # Perpendicular Opening + (C4e3F6)
            "D4f4E5f5e6f6g6h6d7",       # Personak Opening (after Perpendicular Opening + C4e3F6)
             
            "F3F4e5F5e6F6G6e7",         # Sweallow
            "F3F4e5F5e6f6G6e7g7"        # Sweallow +
             
             
             
             
             
             
             
             
             
             
#             "f4D5d6G6f7D7h7F8",
#             "f4D5G6f7G7h7",
#             "f4D5G5d6G6h6f7G7h7G8",
#             "e4f4D5G5G6d6f7G7h7G8",
#             "f4D5G5d6G6f7G7h7G8",
#             "F3D4c4e4f4g4c5D5G5H5d6G6h6c7D7E7f7G7",
#             "e4f4g4D5E5H5d6G6h6D7E7f7G7",
#             "f4D5d6G6E7f7G7",
#             "f4D5d6G6E4f7G7",
#             "D4f4D5d6G6h6f7G7",
#             "D4f4D5d6G6d7E7f7G7",
#             "D2B3d3e3F3b4c4D4E4f4b5C5D5B6c6d6G6B7d7f7G7",
#             "D4f4D5d6G6d7f7G7",
#             "D4f4c5D5C6d6G6b7C7d7E7f7G7d8",
#             "D4f4c5D5d6G6f7G7",
#             "D4f4D5d6G6f7G7",
#             "D4f4D5d6G6f7G7",
# 
# 
#             "f4c5D5G7",
#             "f4D5G5d6G6h6d7E7f7H7G8",
#             "f4g4D5G5d6G6d7E7f7E8",
#             "f4D5G5G6f7",
#             "D3E4f4D5F5e6G6f7",
#             "f4G4c5D5G6g5F3f7H6g7E7d7",
#             "f4G4c5D5G6",
#             "f4c5D5G6",
#             "f4D5G5d6F7",
#             "f4D5G5d6E7g4F7d7",
#             "f4D5G5d6E7g4F7d4E4f3E3",
# 
# 
#             "f4D5G5d6E7g4F7d4E4f3C7g6E6g7",
#             "f4D5G5d6E7g4F7d4E4f3C7g6E6",
#             "f4D5G5d6E7g4F7d4E4f3C7g6C5g7H6e8",
#             "f4D5G5d6E7g4F7d4E4f3C7g6",
#             "f4D5G5d6E7g4F7d4E4f3C6g6C5g7D3f8E3d8",
#             "f4D5G5d6E7g4F7d4E4f3C6g6C4",
#             "f4D5G5d6E7g4F7d4E4f3C6g6",
#             "f4D5G5d6E7g4F7d4E4f3C6",
#             "f4D5G5d6E7g4F7d4E4f3",
#             "f4D5G5d6E7g4F3",
#             "f4D5G5d6E7g4E4d4",
#             "f4D5G5d6E7g4E4",
#             "f4D5G5d6E7g4D7",
#             "f4D5G5d6E7f7",
#             "f4D5"
            ]
         
        opening_moves += diagonalOpeningsBlack
        opening_moves += parallelOpeningsBlack
#         if(color == Board._BLACK):
#             opening_moves += diagonalOpeningsBlack
#             opening_moves += parallelOpeningsBlack
#         else:
#             opening_moves += diagonalOpeningsWhite
#             opening_moves += parallelOpeningsWhite
        opening_moves += perpendicularOpenings
        
        opening_moves += MovingData.OpeningMoveData.getMoveList()
          
        return opening_moves
        
        
        