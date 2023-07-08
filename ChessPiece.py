# Superclass for all pieces, all pieces share the color attribute ("w") or ("b")
class ChessPiece:
    def __init__(self, color):
        self.color = color
    def getColor(self):
        return self.color



# Pawn class, has en passant attribute
class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.rowDict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        self.enPassantPossible = False

    def validMoves(self, board, col, row):
        validMoves = []
        direction = 1 if self.color == "w" else -1

        # Check for a forward move
        if board.isEmptyColRow(col, row + direction):
            validMoves.append((row + direction, col))

        # Check for the initial double-step move
        if board.isEmptyColRow(col, row + (direction * 2)) and ((row == 2 and self.color == "w") or (row == 7 and self.color == "b")):
            validMoves.append((row + (direction * 2), col))

        # # Check for capturing moves diagonally
        for capture_col in [col - 1, col + 1]:
            if board.isValidMove(col, row, self.color) and board.isEnemyPiece(capture_col, row + direction, self.color):
                validMoves.append((row + direction, capture_col))

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
                    validMoves.append((r,c))

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
                validMoves.append((newRow, newCol))
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
                    validMoves.append((r, c))

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
                c += d[0]
                r += d[1]
                if board.isValidMove(c, r, self.color):
                    validMoves.append((r, c))
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
        moves = [(col, row + 1), (col, row - 1), (col + 1, row), (col - 1, row),
                 (col + 1, row + 1), (col + 1, row - 1), (col - 1, row + 1), (col - 1, row - 1)]

        for move in moves:
            if board.isValidMove(move[0], move[1], self.color):
                validMoves.append(move)

        return validMoves

    def __str__(self):
        return "K"
