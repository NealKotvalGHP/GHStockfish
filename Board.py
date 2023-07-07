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

    def is_valid_move(self, col, row, color):
        if not (0 < col < 9 and 0 < row < 9):
            return False

        piece = self.board[row][col]
        if str(piece) == "0" or piece.color != color:
            return True

        return False

    def _is_valid_range(self, move):
        start_col = self.letToNum[move[0]]
        start_row = int(move[1])
        end_col = self.letToNum[move[2]]
        end_row = int(move[3])

        piece = self.get_piece(move[:2])
        piece = str(piece).lower()
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)

        if piece == 'p':
            if (start_row == 2 and piece.color == "w") or (start_row == 7 and piece.color == "b"):
                if (row_diff == 2 or row_diff == 1) and col_diff == 0:
                    return True
                else:
                    return False
            if row_diff == 1 and end_col == start_col:
                return True
            if row_diff == 1 and col_diff == 1 and str(self.get_piece(move[2:])).lower() == "b":
                return True
        elif piece == 'r':
            if row_diff == 0 or col_diff == 0:
                return True
        elif piece == 'n':
            if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
                return True
            if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
                return True
        elif piece == 'b':
            if abs(start_row - end_row) == abs(start_col - end_col):
                return True
        elif piece == 'q':
            if start_row == end_row or start_col == end_col:
                return True
            if row_diff == col_diff:
                return True
        elif piece == 'k':
            if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                return True

        return False

    def _is_turn(self, move):
        return self.get_piece(move[:2]).color == self.turn

    def _is_empty(self, move):
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