# Superclass for all pieces, all pieces share the color attribute ("w") or ("b")
class ChessPiece:
    def __init__(self, color):
        self.color = color

# Pawn class, has en passant attribute
class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.rowDict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        self.enPassantPossible = False

    def validMoves(self, board, col, row):
        validMoves = []
        direction = 1 if self.color == "w" else -1

        if board.isEmptyColRow(col, row + direction):
            validMoves.append((col, row + direction))

        if board.isEmptyColRow(col, row + (direction * 2)) and ((row == 2 and self.color == "w") or (row == 7 and self.color == "b")):
            validMoves.append((col, row + (direction * 2)))
        return validMoves

    def __str__(self):
        return "P"

# Rook class
class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.canCastle = True

    def validMoves(self, board, col, row):
        validMoves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for d in directions:
            c, r = col, row

            while True:
                c += d[0]
                r += d[1]

                if board.isValidMove(c, r, self.color):
                    validMoves.append((c, r))

                    if board.isEnemyPiece(c, r, self.color):
                        break
                else:
                    break

        return validMoves

    def __str__(self):
        return "R"

# Knight class
class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def validMoves(self, board, col, row):
        validMoves = []
        directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for d in directions:
            newCol, newRow = col + d[0], row + d[1]
            if board.isValidMove(newCol, newRow, self.color):
                validMoves.append((newCol, newRow))
        return validMoves

    def __str__(self):
        return "N"

# Bishop class
class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def validMoves(self, board, col, row):
        validMoves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            c, r = col, row
            while True:
                c += d[0]
                r += d[1]

                if board.isValidMove(c, r, self.color):
                    validMoves.append((c, r))

                    if board.isEnemyPiece(c, r, self.color):
                        break
                else:
                    break

        return validMoves

    def __str__(self):
        return "B"

# Queen class
class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def validMoves(self, board, col, row):
        validMoves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            c, r = col, row
            while True:
                r += d[0]
                c += d[1]
                if board.isValidMove((c, r), self.color):
                    validMoves.append((c, r))
                    if board.isEnemyPiece(c, r, self.color):
                        break
                else:
                    break
        return validMoves

    def __str__(self):
        return "Q"

# King class
class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.canCastle = True

    def validMoves(self, board, col, row):
        validMoves = []
        moves = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1), (row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]
        for move in moves:
            if board.isValidMove(move, self.color):
                validMoves.append(move)
        return validMoves

    def __str__(self):
        return "K"
