#!/usr/bin/env python

from game.board import Reversi
from player.ai import ShittyLevelPlayer, BeginnerLevelPlayer, BeginnerLevelPlayer2, RandomPlayer
from player.ai import AlphaBetaPlayer as myPlayer
import time
from io import StringIO
import sys

import os
from contextlib import redirect_stdout # save in file


'''
A special implementation of localGame used to do probability tests over multiple game.
It is possible to print the state of every round by put on <verb>. If this variable 
is set at False, only the final board (ie. when game will be over) will be printed.

These messages are also saved into a file over a custom folder by using the dup mechanics.
(Output file can be set at the send of this script)
'''
# b = Reversi.Board(10)

nbTest = 300

verb = False

def firstSet():
    b = Reversi.Board(10)
    
    players = []
    player1 = myPlayer.myPlayer()   #IA (black)
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = BeginnerLevelPlayer2.myPlayer()   #random (white)
    player2.newGame(b._WHITE)
    players.append(player2)
    
    return (b, players)
def secondSet():
    b = Reversi.Board(10)
    
    players = []
    player1 = myPlayer.myPlayer()   #IA (black)
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = RandomPlayer.myPlayer()   #random (white)
    player2.newGame(b._WHITE)
    players.append(player2)
    
    return (b, players)

def thirdSet():
    b = Reversi.Board(10)
    
    players = []
    player1 = myPlayer.myPlayer()   #IA (black)
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = myPlayer.myPlayer()   #IA (white)
    player2.newGame(b._WHITE)
    players.append(player2)
    
    return (b, players)


def runMatch(b, players):
    
#     players = []
#     player1 = myPlayer.myPlayer()   #IA (black)
#     player1.newGame(b._BLACK)
#     players.append(player1)
#     player2 = BeginnerLevelPlayer2.myPlayer()   #random (white)
#     player2.newGame(b._WHITE)
#     players.append(player2)
    
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
        if(verb):
            print("Referee Board:")
            print(b)
            print("Before move", nbmoves)
            print("Legal Moves: ", b.legal_moves())
        
        
        nbmoves += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
        
        currentTime = time.time()
        sys.stdout = stringio
        
        move = players[nextplayer].getPlayerMove()
        
        
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        
        if(verb):
            print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        
        
        if(verb):
            print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
        (x,y) = move 
        if not b.is_valid_move(nextplayercolor,x,y):
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        players[otherplayer].playOpponentMove(x,y)
    
        nextplayer = otherplayer
        nextplayercolor = othercolor
        
#         print(b)        
    return (totalTime, b)
    

def mainLauncher(b, players):
    (totalTime,b) = runMatch(b, players)
    print("The game is over")
    print(b)

    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("Time:", totalTime)
    print("Winner: ", end="")
    if nbwhites > nbblacks:
        print("WHITE")
        return 0
    elif nbblacks > nbwhites:
        print("BLACK")
        return 1
    else:
        print("DEUCE")
        return 0

def runMultipleGame(x):
    game1 = 0
    
    for i in range (0, x, 1):
        print("")
        print("Test: ", i+1)
#         (a1,a2) = thirdSet()      #myPlayer vs myPlayer
#         (a1,a2) = secondSet()     #myplayer vs random
        (a1,a2) = firstSet()        #myplayer vs beginner strong
        game1 += mainLauncher(a1,a2)
        print("* Statistiques")
        print("    IA:", game1, "over", i+1)
        
        
#     game3 = 0
#     for i in range (0, x, 3):
#         print("")
#         print("Test: ", i)
#         (a1,a2) = firstSet()
#         game1 += mainLauncher(a1,a2)
#         print("* Statistiques")
#         print("    IA1:", game1, "over", i/3 +1)
#         print("    IA2:", game2, "over", i/3 +1)
#         print("    IA3:", game3, "over", i/3 +1)
#         time.sleep(3)
#         
#         print("Test: ", i+1)
#         print("Current Val:", median)
#         (a1,a2) = secondSet()
#         game2 += mainLauncher(a1,a2)
#         print("* Statistiques")
#         print("    IA1:", game1, "over", i/3 +1)
#         print("    IA2:", game2, "over", i/3 +1)
#         print("    IA3:", game3, "over", i/3 +1)
#         time.sleep(3)
#         
#         print("Test: ", i+2)
#         (a1,a2) = thirdSet()
#         game3 += mainLauncher(a1,a2)
#         print("* Statistiques")
#         print("    IA1:", game1, "over", i/3 +1)
#         print("    IA2:", game2, "over", i/3 +1)
#         print("    IA3:", game3, "over", i/3 +1)
#         time.sleep(3)
        
#         print("")
#     
#     
#     print("Total score: ", game1+game2+game3)

def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd
    
stdout_fd = sys.stdout.fileno()
with open('../logs/log_vs_basic.txt', 'w') as f:
# with open('../logs/log.txt', 'w') as f:
# with open('../logs/log_versus_and_verbose.txt', 'w') as f:
    with redirect_stdout(f):
        print('it now prints to `help.text`')
        
    stdout = sys.stdout
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied: 
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(f), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(f, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
            
# time.sleep(0.5)

print("")
print("#################")
# mainLauncher(b)
runMultipleGame(nbTest)
print("Over: ", nbTest, "Tests.")
print("")

