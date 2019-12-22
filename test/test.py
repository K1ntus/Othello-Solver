import timeit
import game.board.ReversiBit as ReversiBit
import multiprocessing
# import helpers.boardHelper as boardHelper

# print(boardHelper.getSortedMoves(b,b._nextPlayer))

import queue
from threading import Thread

# def foo(i):
#     if i == 5:
#         for x in range(100):
#             print(str(x))
#     return i
#
# def run():
#     que = queue.Queue()
#     for i in range(10):
#         worker = Thread(target=lambda q ,arg1 : q.put((foo(i),'i')), args=(que ,i))
#         worker.start()
#
#     data =[]
#     for i in range(10):
#         data.append(que.get())
#     que.task_done()
#     print(data)
#     tmp = sorted(data, key=lambda d :d[0] ,reverse=True)
#     print(tmp)
#
# run()

def checkboard():
    b = ReversiBit.Board(10)
    b.push([1, 3, 5])
    moves = b.legal_moves()
    print(moves)
    b.bbPrint()

    # print( b.legal_moves())
    # board = b._bbW | b._bbB
    # for i in range(100,0,-1):
    #     j= i-1
    #     if ((board >>j) &1) >0 :
    #         print(j)

print(timeit.timeit(checkboard, number=1))
print(multiprocessing.cpu_count())