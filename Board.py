import numpy as np
import ChessPiece

class Board:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.fen = fen
        self.board = fen_to_matrix(self.fen)
        self.turn = fen.split()[1]
        self.letToNum = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.numToLet = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}

    def initialize(self):
        self.board = fen_to_matrix("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.turn = "w"

    def print_board(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))

    def get_board(self):
        return self.board

    def get_turn(self):
        return self.turn

    def get_piece(self, index):
        col = self.letToNum[index[0]] - 1
        row = 8 - int(index[1])
        return self.board[row][col]

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

    def is_valid_move(self, col, row, selfColor):
        if not (1 <= col <= 8 and 1 <= row <= 8):
            return False

        piece = self.board[row][col]
        if str(piece) == "0" or piece.color != selfColor:
            return True

        return False

    def isEmptyMove(self, move):
        if self.get_piece(move[:2]) == 0:
            return True
        return False

    def isEmptyColRow(self, col, row):
        return str(self.get_piece(self.xyToChess(col, row))) == "0"

    def xyToChess(self, col, row):
        return self.numToLet[col] + str(row)

    def chessToMatrix(self, chessDex):
        return indexToMatrix(self.letToNum[chessDex[0]], chessDex[1])

    def is_enemy_piece(self, col, row, color):
        x, y = indexToMatrix(col, row)
        piece = self.board[row][col]
        return str(piece) != "0" and piece.color != self.turn

def fen_to_matrix(fen):
    matrix = [[0] * 8 for _ in range(8)]
    parts = fen.split()
    board_fen = parts[0]
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

def indexToMatrix(row, col):
    return col - 1, 8 - row