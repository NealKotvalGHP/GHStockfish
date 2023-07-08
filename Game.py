import Agent
import Board

board = Board.Board()
print("Turn: " + board.getTurn())
board.printBoard()
while True:
    if board.getTurn() == "w":
        move = input("Enter move: ")
        possible = board.checkPossible(move)
        print(board.getPossibleMoves(board.getTurn()))

        if possible:
            board.makeMove(move)
            print("Turn: " + board.getTurn())
            board.printBoard()
        else:
            print("INVALID MOVE")
    else:
        move = board.randomMove()
        board.makeMove(move)
        print("Turn: " + board.getTurn())
        board.printBoard()
        print("BLACK MOVED: " + move)