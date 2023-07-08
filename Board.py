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

    def printBoard(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))

    def getBoard(self):
        return self.board

    def getTurn(self):
        return self.turn

    def getPiece(self, chessDex):
        col = self.letToNum[chessDex[0]]
        row = int(chessDex[1])
        x, y = indexToMatrix(col, row)
        return self.board[x][y]
    
    def getPieceColRow(self, col, row):
        x, y = indexToMatrix(col, row)
        print("X,Y: " + str(x) + ", " + str(y))
        return self.board[x][y]


    def makeMove(self, move):
        startRow = 8 - int(move[1])
        startCol = ord(move[0]) - ord('a')
        endRow = 8 - int(move[3])
        endCol = ord(move[2]) - ord('a')

        piece = self.board[startRow][startCol]
        self.board[startRow][startCol] = 0
        self.board[endRow][endCol] = piece
        self.turn = "b" if self.turn == "w" else "w"

    def isValidMove(self, col, row, selfColor):
        if (0 < col < 9 and 0 < row < 9 and (str(self.getPiece(col, row)) == "0" or self.getPiece(col, row).color != selfColor)):
            return True
        return False

    def isEmptyColRow(self, col, row):
        return str(self.getPiece(self.xyToChess(col, row))) == "0"

    def xyToChess(self, col, row):
        return self.numToLet[col] + str(row)

    def chessToMatrix(self, chessDex):
        return indexToMatrix(self.letToNum[chessDex[0]], chessDex[1])

    def isEnemyPiece(self, col, row, color):
        x, y = indexToMatrix(col, row)
        piece = self.board[x][y]
        return str(piece) != "0" and piece.color != color
    
    def printValidMoves(self, move):
        col = self.letToNum[move[0]]
        row = int(move[1])
        print(f"Piece: {str(self.getPieceColRow(col, row))}")
        print([move[:2]])
        print(f"Col, Row: {col, row}")
        if (str(self.getPiece(move[:2])) != "0"):
            print(f"Valid Moves: {str(self.getPieceColRow(col, row).validMoves(self, col, row))}")


def fenToMatrix(fen):
    matrix = [[0] * 8 for _ in range(8)]
    parts = fen.split()
    boardFen = parts[0]
    pieceValues = {
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
    for char in boardFen:
        if char == '/':
            row -= 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            matrix[row][col] = pieceValues[char]
            col += 1

    return np.flipud(matrix)

def indexToMatrix(col, row):
    return col - 1, 8 - row
