
import player.ai.AiPlayer3 as AiPlayer3
import player.ai.RandomPlayer as RandomPlayer
import game.board.Reversi as Reversi
import myPlayer
import time
from io import StringIO
import sys

list = []


def startGame():
    b = Reversi.Board(10)

    players = []
    player1 = AiPlayer3.AiPlayer3()
    player1.newGame(b._BLACK)

    players.append(player1)
    player2 = RandomPlayer.myPlayer() #random player
    player2.newGame(b._WHITE)

    players.append(player2)

    totalTime = [0, 0]  # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK
    nbmoves = 1

    outputs = ["", ""]
    # sysstdout = sys.stdout
    # stringio = StringIO()

    print(b.legal_moves())
    while not b.is_game_over():
        # print("Referee Board:")
        # print(b)
        # print("Before move", nbmoves)
        # print("Legal Moves: ", b.legal_moves())
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
        (x, y) = move
        if not b.is_valid_move(nextplayercolor, x, y):
            # print(otherplayer, nextplayer, nextplayercolor)
            # print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        players[otherplayer].playOpponentMove(x, y)

        nextplayer = otherplayer
        nextplayercolor = othercolor

        # print(b)

    print("The game is over")
    print(b)
    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("Time:", totalTime)
    print("Winner: ", end="")
    global list
    list.append(totalTime[0])
    if nbwhites > nbblacks:
        print("WHITE")
        return 2
    elif nbblacks > nbwhites:
        print("BLACK")
        return 1
    else:
        print("DEUCE")
        return 0


def run(times):
    black = white = draw = 0
    for i in range(0, times):
        res = startGame()
        if res == 2:
            white += 1
        if res == 1:
            black += 1
        if res == 0:
            draw += 1
    print("Black : ", black, " White : ", white, " Draw : ", draw)
    global list
    size = len(list)
    s = sum(list)
    print("averge time :", str(s / size))


run(10)
