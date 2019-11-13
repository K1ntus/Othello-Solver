import Reversi
from heuristics import ShittyLevelPlayer, BeginnerLevelPlayer, RandomPlayer
import myPlayer
import time
from io import StringIO
import sys

# b = Reversi.Board(10)


def runMatch():
    b = Reversi.Board(10)
    
    players = []
    player1 = myPlayer.myPlayer()   #IA (black)
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = BeginnerLevelPlayer.myPlayer()   #random (white)
    player2.newGame(b._WHITE)
    players.append(player2)
    
    totalTime = [0,0] # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK
    nbmoves = 1
    
    outputs = ["",""]
    sysstdout= sys.stdout
    stringio = StringIO()
    
    print("Running A Match ...")
    
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
        sys.stdout = stringio
        
        move = players[nextplayer].getPlayerMove()
        
        
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
    #     print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
    #     print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
        (x,y) = move 
        if not b.is_valid_move(nextplayercolor,x,y):
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        players[otherplayer].playOpponentMove(x,y)
    
        nextplayer = otherplayer
        nextplayercolor = othercolor
        
    return (totalTime, b)
    
    #     print(b)

def mainLauncher(b):
    (totalTime,b) = runMatch()
    print("The game is over")
    print(b)
    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("Time:", totalTime)
    print("Winner: ", end="")
    if nbwhites > nbblacks:
        print("WHITE")
        return -1
    elif nbblacks > nbwhites:
        print("BLACK")
        return 1
    else:
        print("DEUCE")
        return 0

def runMultipleGame(x):
    median = 0
    for i in range (0, x):
        print("")
        print("Test: ", i)
        print("Current Val:", median)
        b = Reversi.Board(10)
        median += mainLauncher(b)
        print("")
    
    
    print("Median score: ", median)



print("")
# mainLauncher(b)
runMultipleGame(1)
print("")

