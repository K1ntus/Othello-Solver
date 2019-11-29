
# import game.board.Reversi as Reversi
# import helpers.boardHelper as boardHelper

# b = Reversi.Board(10)
# print(boardHelper.getSortedMoves(b,b._nextPlayer))

import queue
from threading import Thread

def foo(i):
    if i == 5:
        for x in range(100):
            print(str(x))
    return i

def run():
    que = queue.Queue()
    for i in range(10):
        worker = Thread(target=lambda q ,arg1 : q.put((foo(i),'i')), args=(que ,i))
        worker.start()

    data =[]
    for i in range(10):
        data.append(que.get())
    que.task_done()
    print(data)
    tmp = sorted(data, key=lambda d :d[0] ,reverse=True)
    print(tmp)

run()
