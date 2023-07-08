import Agent
import Board

board = Board.Board()
print("Turn: " + board.getTurn())
board.printBoard()
while True:
    move = input("Enter move: ")
    board.printValidMoves(move)
    board.makeMove(move)
    print("Turn: " + board.getTurn())
    board.printBoard()