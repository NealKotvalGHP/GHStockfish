# import Agent
import Board

board = Board.Board()
print("Turn: " + board.getTurn())
board.printBoard()
while True:
    move = input("Enter move: ")
    print(board.getPossibleMoves(board.getTurn()))
    board.makeMove(move)
    print("Turn: " + board.getTurn())
    board.printBoard()