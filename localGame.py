#!/usr/bin/env python

import Reversi
from heuristics import ShittyLevelPlayer, BeginnerLevelPlayer, BeginnerLevelPlayer2, RandomPlayer
import myPlayer
import time
from io import StringIO
import sys

import os
from contextlib import redirect_stdout # save in file

# b = Reversi.Board(10)

nbTest = 300


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
    player2 = BeginnerLevelPlayer.myPlayer()   #random (white)
    player2.newGame(b._WHITE)
    players.append(player2)
    
    return (b, players)


def runMatch(b, players):
    
    players = []
    player1 = myPlayer.myPlayer()   #IA (black)
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = BeginnerLevelPlayer2.myPlayer()   #random (white)
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
#         if(True):
#             print("Referee Board:")
#             print(b)
#             print("Before move", nbmoves)
#             print("Legal Moves: ", b.legal_moves())
        
        
        nbmoves += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
        
        currentTime = time.time()
        sys.stdout = stringio
        
        move = players[nextplayer].getPlayerMove()
        
        
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        
        if(False):
            print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        
        
        if(False):
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
        
        print(b)        
    return (totalTime, b)
    

def mainLauncher(b, players):
    (totalTime,b) = runMatch(b, players)
    print("The game is over")
    print(b)
    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("Time:", totalTime)
    print("Winner: ", end="")
    if nbwhites == nbblacks:
        print("DEUCE")
        return 0        
    elif nbwhites > 50:
        print("WHITE")
        return 0
    else:
        print("BLACK")
        return 1

def runMultipleGame(x):
    median = 0
    for i in range (0, x, 3):
        print("")
        print("Test: ", i)
        print("Current Val:", median)
        (a1,a2) = firstSet()
        median += mainLauncher(a1,a2)
        time.sleep(3)
        
        print("Test: ", i+1)
        print("Current Val:", median)
        (a1,a2) = secondSet()
        median += mainLauncher(a1,a2)
        time.sleep(3)
        
        print("Test: ", i+2)
        print("Current Val:", median)
        (a1,a2) = thirdSet()
        median += mainLauncher(a1,a2)
        time.sleep(3)
        
        print("")
    
    
    print("Median score: ", median)

def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd

stdout_fd = sys.stdout.fileno()
with open('log.txt', 'w') as f:
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
        
time.sleep(2)

print("")
print("#################")
# mainLauncher(b)
runMultipleGame(nbTest)
print("Over: ", nbTest, "Tests.")
print("")

