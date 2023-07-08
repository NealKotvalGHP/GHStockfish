import numpy as np
import ChessPiece

class Board:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.fen = fen
        self.board = fenToMatrix(self.fen)
        self.turn = fen.split()[1]
        self.letToNum = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        self.numToLet = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}

    def initialize(self):
        self.board = fenToMatrix("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
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
        return self.board[y][x]
    
    def getPieceColRow(self, col, row):
        x, y = indexToMatrix(col, row)
        return self.board[y][x]


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
        if (0 < col < 9 and 0 < row < 9 and (str(self.getPieceColRow(col, row)) == "0" or self.getPieceColRow(col, row).color != selfColor)):
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
        piece = self.board[y][x]
        return str(piece) != "0" and piece.color != color
    
    def printValidMoves(self, move):
        col = self.letToNum[move[0]]
        row = int(move[1])

        if (str(self.getPieceColRow(col,row) != "0")):
            print(f"Valid Moves: {self.getPieceColRow(col, row).validMoves(self, col, row)}")

    def getPossibleMoves(self, color):
        possible_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                # Check if the current position contains a piece of the given color
                # if (str(piece)!="0"):
                #     # print(piece.color, color)
                #     # print(str(piece) != "0")
                #     # print(piece.getColor == color)
                if str(piece) != "0" and piece.getColor() == color:
                    rowInd, colInd = matrixToIndex(row, col)
                    validMoves = piece.validMoves(self, colInd, rowInd)
                    for move in validMoves:
                        possible_moves.append((rowInd, colInd, move[0], move[1]))

                    # Generate the possible moves for the piece at this position
                    # Append the valid moves to the `possible_moves` list in the appropriate format
                    
        return possible_moves

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

def matrixToIndex(row, col):
    return 8 - row, col + 1
