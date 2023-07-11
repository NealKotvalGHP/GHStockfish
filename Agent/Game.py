import Agent
import Old

board = Old.Board()
print("Turn: " + board.getTurn())
board.printBoard()
while True:
        move = board.randomMove()
        board.makeMove(move)
        print("Turn: " + board.getTurn())
        board.printBoard()
        print("BLACK MOVED: " + move)