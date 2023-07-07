class ChessPiece:
    def __init__(self, color):
        self.color = color

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.rowDict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        self.en_passant_possible = False

    #checks for all pawn valid moves, row, col corresponds to x, y where x begins at 1
    def valid_moves(self, board, col, row):
        valid_moves = []

        direction = 1 if self.color == "w" else -1

        #check if directly ahead is empty
        if board.isEmptyColRow(col,row+direction):
            valid_moves.append((col,row+direction))
        #check if two ahead is empty
    
        if board.isEmptyColRow(col, row+(direction*2)) and (row == 2 or row == 7):
            valid_moves.append((col, row+(direction*2)))
        #check for any diagonal captures
        return valid_moves

        

    def __str__(self):
        return "P"
    
class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.can_castle = True

    def valid_moves(self, board, col, row):
        valid_moves = []
        #check left


        start_col = col
        start_row = row
        print(start_col, start_row)
        direction = -1
        start_col+=direction

        while start_col < 9 and start_col > 0 and (board.isEmptyColRow(start_col, start_row)) :
            valid_moves.append((start_col,start_row))
            start_col+=direction
        # if start_col < 8 and start_col > 0 and board.get_piece(board.xyToChess(start_col+direction,start_row)).color != self.color:
        #     valid_moves.append((start_col+direction,start_row))

        #check right
        start_col = col
        start_row = row
        direction = 1
        start_col+=direction

        while start_col < 9 and start_col > 0 and (board.isEmptyColRow(start_col, start_row)) :
            valid_moves.append((start_col,start_row))
            start_col+=direction
        # if start_col < 8 and start_col > 0 and board.get_piece(board.xyToChess(start_col+direction,start_row)).color != self.color:
        #     valid_moves.append((start_col+direction,start_row))

        #check up
        start_col = col
        start_row = row

        direction = 1
        start_row+=direction
        while start_row < 9 and start_row > 0 and (board.isEmptyColRow(start_col, start_row)) :
            valid_moves.append((start_col,start_row))
            start_row+=direction
        # if start_row < 8 and start_row > 0 and board.get_piece(board.xyToChess(start_col,start_row+direction)).color != self.color:
        #     valid_moves.append((start_col,start_row+direction))
        
        #check down
        start_col = col
        start_row = row
        direction = -1
        start_row+=direction

        while start_row < 9 and start_row > 0 and (board.isEmptyColRow(start_col, start_row)) :
            valid_moves.append((start_col,start_row))
            start_row+=direction
        # if start_row < 8 and start_row > 0 and board.get_piece(board.xyToChess(start_col,start_row+direction)).color != self.color:
        #     valid_moves.append((start_col,start_row+direction))


        return valid_moves
    
    def __str__(self):
        return "R"

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def valid_moves(self, board, col, row):
        valid_moves = []
        return valid_moves

    def __str__(self):
        return "N"

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def valid_moves(self, board, current_square):
        valid_moves = []
        row, col = current_square

        #northeast

        #northwest

        #southeast

        #southwest

        #right

        #left

        #up

        #down

        return valid_moves

    def __str__(self):
        return "B"

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)

    def valid_moves(self, board, current_square):
        valid_moves = []
        row, col = current_square

        # Check valid moves in horizontal, vertical, and diagonal directions
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (-1, 1), (1, -1), (-1, -1)
        ]

        for d in directions:
            r, c = row, col

            while True:
                r += d[0]
                c += d[1]

                if board.is_valid_move((r, c), self.color):
                    valid_moves.append((r, c))

                    if board.is_enemy_piece((r, c), self.color):
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

    def valid_moves(self, board, current_square):
        valid_moves = []
        row, col = current_square

        # Possible king moves relative to the current square
        moves = [
            (row + 1, col), (row - 1, col),
            (row, col + 1), (row, col - 1),
            (row + 1, col + 1), (row + 1, col - 1),
            (row - 1, col + 1), (row - 1, col - 1)
        ]

        for move in moves:
            if board.is_valid_move(move, self.color):
                valid_moves.append(move)

        return valid_moves
    
    def __str__(self):
        return "K"