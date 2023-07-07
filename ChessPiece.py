class ChessPiece:
    def __init__(self, color):
        self.color = color

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.rowDict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        self.en_passant_possible = False

    def valid_moves(self, board, col, row):
        valid_moves = []
        direction = 1 if self.color == "w" else -1
        if board.isEmptyColRow(col, row + direction):
            valid_moves.append((col, row + direction))
        if board.isEmptyColRow(col, row + (direction * 2)) and (row == 2 or row == 7):
            valid_moves.append((col, row + (direction * 2)))
        return valid_moves

    def __str__(self):
        return "P"

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.can_castle = True

    def valid_moves(self, board, col, row):
        valid_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in directions:
            start_col, start_row = col + d[0], row + d[1]
            while board.isEmptyColRow(start_col, start_row):
                valid_moves.append((start_col, start_row))
                start_col += d[0]
                start_row += d[1]
        return valid_moves

    def __str__(self):
        return "R"

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def valid_moves(self, board, col, row):
        valid_moves = []
        directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for d in directions:
            new_col, new_row = col + d[0], row + d[1]
            if board.is_valid_move(new_col, new_row, self.color):
                valid_moves.append((new_col, new_row))
        return valid_moves

    def __str__(self):
        return "N"

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def valid_moves(self, board, col, row):
        valid_moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            c, r = col, row
            while True:
                c += d[0]
                r += d[1]
                #something wrong with is_valid_move function
                if board.is_valid_move(c, r, self.color):
                    valid_moves.append((c, r))

                    if board.is_enemy_piece(c, r, self.color):
                        break
                else:
                    break
        return valid_moves

    def __str__(self):
        return "B"

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def valid_moves(self, board, col, row):
        valid_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            c, r = col, row
            while True:
                r += d[0]
                c += d[1]
                if board.is_valid_move((c, r), self.color):
                    valid_moves.append((c, r))
                    if board.is_enemy_piece(c, r, self.color):
                        break
                else:
                    break
        return valid_moves

    def __str__(self):
        return "Q"

class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.can_castle = True

    def valid_moves(self, board, col, row):
        valid_moves = []
        moves = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1), (row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]
        for move in moves:
            if board.is_valid_move(move, self.color):
                valid_moves.append(move)
        return valid_moves

    def __str__(self):
        return "K"
