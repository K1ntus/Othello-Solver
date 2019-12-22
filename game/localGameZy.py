from io import StringIO
import sys
import time

from game.board import Reversi
# import player.ai.AlphaBetaPlayer as myPlayer
# import player.ai.AiPlayer1 as myPlayer
import player.ai.AiPlayerPVS as myPlayer
# import player.ai.RandomPlayer as myPlayer
import ia_v2 as Enemy1
# import alexis as Enemy1
# import jd as myPlayer
from ui.ui import Gui



# import player.ai.RandomPlayer as Enemy1
# import player.ai.BeginnerLevelPlayer2 as Enemy1
# import player.ai.AlphaBetaPlayer as Enemy1localGame.py

DISPLAY_MODE=True

b = Reversi.Board(10)

players = []
player1 = myPlayer.myPlayer()
player1.newGame(b._BLACK)
players.append(player1)
# player2 = myPlayer.myPlayer()
player2 = Enemy1.myPlayer()
player2.newGame(b._WHITE)
players.append(player2)

totalTime = [0,0] # total real time for each player
nextplayer = 0
nextplayercolor = b._BLACK
nbmoves = 1
game_board = None
if(DISPLAY_MODE):
    game_board = Gui()
    game_board.show_game()
    time.sleep(1)

outputs = ["",""]
# sysstdout= sys.stdout
# stringio = StringIO()

# print(b.legal_moves())
while not b.is_game_over():
#     print("Referee Board:")
#     print(b)
#     print("Before move", nbmoves)
#     print("Legal Moves: ", b.legal_moves())
    nbmoves += 1
    otherplayer = (nextplayer + 1) % 2
    othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
    
    currentTime = time.time()
    # sys.stdout = stringio
    move = players[nextplayer].getPlayerMove()
    # sys.stdout = sysstdout
    # playeroutput = "\r" + stringio.getvalue()
    # stringio.truncate(0)
    # print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
    # outputs[nextplayer] += playeroutput
    totalTime[nextplayer] += time.time() - currentTime
    # print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
    (x,y) = move
    print(nextplayercolor,x,y)
    if not b.is_valid_move(nextplayercolor,x,y):
        print(otherplayer, nextplayer, nextplayercolor)
        print("Problem: illegal move")
        break
    
    
    if(DISPLAY_MODE):
        #si les available move sont mal affiches, mets a None. Je debuggerais qd je serais sur mon linux
        availMove = [m for m in players[nextplayer]._board.legal_moves()]

        (nbB, nbW) = b.get_nb_pieces()
        game_board.update(board=b, blacks=nbB, whites=nbW, availMove=availMove, current_player_color=nextplayercolor)
        
        b.push([nextplayercolor, x, y])
        game_board.clear_board(b)
        # print(b)
        (nbB, nbW) = b.get_nb_pieces()
        game_board.update(board=b, blacks=nbB, whites=nbW, availMove=availMove, current_player_color=nextplayercolor)
        availMove = None
    else:        
        b.push([nextplayercolor, x, y])
        
    players[otherplayer].playOpponentMove(x,y)
    
    
    

    nextplayer = otherplayer
    nextplayercolor = othercolor
    
#     time.sleep(5)

    

print("The game is over")
print(b)
(nbwhites, nbblacks) = b.get_nb_pieces()
print("Time:", totalTime)
print("Winner: ", end="")
if nbwhites > nbblacks:
    print("WHITE")
elif nbblacks > nbwhites:
    print("BLACK")
else:
    print("DEUCE")
    
time.sleep(1000)

