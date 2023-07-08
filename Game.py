import Agent
import Board

board = Board.Board()
print("Turn: " + board.get_turn())
board.print_board()
while True:
    move = input("Enter move: ")
    board.print_Valid_moves(move)
    board.make_move(move)
    print("Turn: " + board.get_turn())
    board.print_board()