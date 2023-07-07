import numpy as np
import ChessPiece

"""
!!!WARNING!!!
Before you enter my mess of terrible code you must understand:
 - chessdex is a word i made up, its pretty much what you use when you play chess like e4,
 - the board is a 8x8 matrix of 0s and Piece subclasses (pawn, knight, bishop, queen, etc.)
 - i use three ways of "indexing", (row, col), [x][y], and chessDex, i use them interchangeably so everything becomes really confusing fast
 - the point of this class is to handle the state of the board,
 - the point of the Piece class is to generate valid moves for that individual piece and keep track of piece traits like being able to castle
"""

class Board:
    #initialize board as starting position via fen function chatgpt wrote(which sucks)
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.fen = fen
        self.board = fen_to_matrix(self.fen)
        self.turn = fen.split()[1]
        self.letToNum = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.numToLet = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}

    #resets the board to starting pos
    def initialize(self):
        self.board = fen_to_matrix("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.turn = "w"

    #prints the matrix, but fancy
    def print_board(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))

    #returns the matrix
    def get_board(self):
        return self.board

    #returns the current turn, "w" or "b"
    def get_turn(self):
        return self.turn

    #returns the piece object at a certain chessDex, i.e "e4"
    def get_piece(self, index):
        col = self.letToNum[index[0]] - 1
        row = 8 - int(index[1])
        return self.board[row][col]

    #makes a move based off chessDex format, i.e "e2e4", takes piece on e2 and moves to e4
    def make_move(self, move):
        print("Valid Moves: " + str(self.get_piece(move[:2]).valid_moves(self, self.letToNum[move[0]], int(move[1]))))
        print(type(self.get_piece(move[:2])))
        print(self.get_piece(move[:2]))
        start_row = 8 - int(move[1])
        start_col = ord(move[0]) - ord('a')
        end_row = 8 - int(move[3])
        end_col = ord(move[2]) - ord('a')

        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0
        self.board[end_row][end_col] = piece
        self.turn = "b" if self.turn == "w" else "w"

    #checks if a square can be moved to via (col, row), requirements = no same color, no out of bounds
    def is_valid_move(self, col, row, selfColor):
        if not (1 <= col <= 8 and 1 <= row <= 8):
            return False
        #converts column row to matrix index, i.e column 1 row 2 to [0][6]
        x,y = indexToMatrix(col, row)

        piece = self.board[x][y]

        if (str(piece) != "0"):
            print("Checking: " + str(col) + ", " + str(row))
            print(selfColor)
            print(piece.color)

        if str(piece) == "0":
            return True

        if (selfColor == piece.color):
            return False
        
        

        return True

    #checks if a square is empty via (col, row)
    def isEmptyColRow(self, col, row):
        return str(self.get_piece(self.xyToChess(col, row))) == "0"

    #converts (col, row) to chessDex, i.e "e4"
    def xyToChess(self, col, row):
        return self.numToLet[col] + str(row)

    #converts chessDex("e4") to Matrix index
    def chessToMatrix(self, chessDex):
        return indexToMatrix(self.letToNum[chessDex[0]], chessDex[1])

    #checks if there is an enemy piece on some (col, row)
    def is_enemy_piece(self, col, row, color):
        x, y = indexToMatrix(col, row)
        piece = self.board[row][col]
        return str(piece) != "0" and piece.color != color

#loads FEN to 8x8 matrix
def fen_to_matrix(fen):
    matrix = [[0] * 8 for _ in range(8)]
    #i hate chatgpt for using functions i didnt know existed
    parts = fen.split()
    board_fen = parts[0]
    #very inefficient way of loading objects into matrix 0 -> empty
    piece_values = {
        'P': ChessPiece.Pawn(color="w"),
        'N': ChessPiece.Knight(color="w"),
        'B': ChessPiece.Bishop(color="w"),
        'R': ChessPiece.Rook(color="w"),
        'Q': ChessPiece.Queen(color="w"),
        'K': ChessPiece.King(color="w"),
        'p': ChessPiece.Pawn(color="b"),
        'n': ChessPiece.Knight(color="b"),
        'b': ChessPiece.Bishop(color="b"),
        'r': ChessPiece.Rook(color="b"),
        'q': ChessPiece.Queen(color="b"),
        'k': ChessPiece.King(color="b")
    }
    row, col = 7, 0
    for char in board_fen:
        if char == '/':
            row -= 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            matrix[row][col] = piece_values[char]
            col += 1

    return np.flipud(matrix)

#converts (row, col) to Matrix index
def indexToMatrix(row, col):
    return col - 1, 8 - row