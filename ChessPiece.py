
#superclass for all pieces, all pieces share the color attribute ("w") or ("b")
class ChessPiece:
    def __init__(self, color):
        self.color = color

#pawn class, has en passant attribute
class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.rowDict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        self.en_passant_possible = False

    def valid_moves(self, board, col, row):
        #list of all possible valid moves
        valid_moves = []
        #if white then the row direction is +1 since it goes up, otherwise it is -1
        direction = 1 if self.color == "w" else -1

        #check if the space ahead is empty, if yes -> valid move
        if board.isEmptyColRow(col, row + direction):
            valid_moves.append((col, row + direction))

        #check if the space two spaces ahead is empty and if you are on home row
        if board.isEmptyColRow(col, row + (direction * 2)) and ((row == 2 and self.color == "w") or (row == 7 and self.color == "b")):
            valid_moves.append((col, row + (direction * 2)))
        return valid_moves

    def __str__(self):
        return "P"

#rook class, pretty self explanatory
class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.can_castle = True
    #check for rook valid moves
    def valid_moves(self, board, col, row):
        valid_moves = []

        # Check valid moves in horizontal and vertical directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for d in directions:
            c, r = col, row

            while True:
                c += d[0]
                r += d[1]

                if board.is_valid_move(c, r, self.color):
                    valid_moves.append((c, r))

                    if board.is_enemy_piece(c, r, self.color):
                        break
                else:
                    break

        return valid_moves

    def __str__(self):
        return "R"

#knight class, moves weird
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

#bishop class
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

#queen class, going to be pretty annoying to implement
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

#king class
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
