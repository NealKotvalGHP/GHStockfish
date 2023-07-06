import numpy as np

class Board:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.fen = fen
        self.board = fen_to_matrix(self.fen)
        self.turn = fen.split()[1]
        self.rowDict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    def initialize(self):
        self.board = fen_to_matrix("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.turn = "w"

    def print_board(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))

    def make_move(self, move):
        # Example of move format: 'e2e4'

        if self.is_valid_move(move):
            start_row = 8 - int(move[1])
            start_col = ord(move[0]) - ord('a')
            end_row = 8 - int(move[3])
            end_col = ord(move[2]) - ord('a')

            piece = self.board[start_row][start_col]
            self.board[start_row][start_col] = 0
            self.board[end_row][end_col] = piece
            if self.turn == "w":
                self.turn = "b"
            else:
                self.turn = "w"

        else:
            print("Invalid Move")

    def is_valid_move(self, move):
        print("ValRange: " + str(self._is_valid_range(move)))
        print("IsEmpty: " + str(not self._is_empty(move)))
        print("IsTurn: " + str(self._is_turn(move)))
        print("ValidPath: " + str(self._is_valid_path(move)))
        if (
            self._is_valid_range(move) and 
            not self._is_empty(move) and 
            self._is_turn(move) and
            self._is_valid_path(move)
            ):
            return True
        return False

    def is_checkmate(self):
        # Implement the logic to check if the game is in a checkmate state
        pass

    def get_piece(self, index):
        col = self.rowDict[index[0]]-1
        row = 8 - int(index[1])

        return self.board[row][col]
    
    def _is_turn(self, move):
        if (self.get_piece(move[:2]).lower()[1] != self.turn):
            return False
        return True

    def _is_valid_range(self, move):
        start_col = self.rowDict[move[0]]
        start_row = int(move[1])
        end_col = self.rowDict[move[2]]
        end_row = int(move[3])

        # Piece-specific valid range checks
        piece = self.get_piece(move[:2])
        piece = piece[:1].lower()
        rowDiff = abs(end_row - start_row)
        colDiff = abs(end_col - start_col)
        # print("Piece: " + str(piece))
        # print("RowDiff: " + str(rowDiff))
        # print("ColDiff: " + str(colDiff))

        if piece == 'p':
            # Pawn
            if (start_row == 2 and self.get_piece(move[:2])[1] == "W") or (start_row == 7 and self.get_piece(move[:2])[1] == "B"):
                # First move, can move 2 squares forward
                # print("RowDiff: " + str(end_row-start_row))
                if (rowDiff == 2 or rowDiff == 1) and colDiff==0:
                    # print("Passed Pawn Test")
                    return True
                else:
                    return False
            if rowDiff == 1 and end_col == start_col:
                # Regular pawn move
                return True
            if rowDiff == 1 and colDiff == 1 and self.get_piece(move[2:])[1].lower() == "b":
                # Pawn capture
                return True
        elif piece == 'r':
            # Rook
            if rowDiff == 0 or colDiff == 0:
                # Moving in the same row or column
                return True
            
        elif piece == 'n':
            # Knight
            if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
                # L-shaped move
                return True
            if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
                # L-shaped move
                return True
        elif piece == 'b':
            # Bishop
            if abs(start_row - end_row) == abs(start_col - end_col):
                # Moving diagonally
                return True
        elif piece == 'q':
            # Queen
            if start_row == end_row or start_col == end_col:
                # Moving in the same row or column
                return True
            if rowDiff == colDiff:
                # Moving diagonally
                return True
        elif piece == 'k':
            # King
            if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                # Moving within a 1-square range
                return True

        return False
    
    def _is_empty(self,move):
        print(self.get_piece(move[:2]))
        if self.get_piece(move[:2]) == 0:
            return True
        return False

    def get_board(self):
        return self.board
    
    def get_turn(self):
        return self.turn

    def chessToMatrix(self, chessDex):
        indexToMatrix(self.rowDict(chessDex[0]), chessDex[1])

    def _is_valid_path(self, move):
        start_col = self.rowDict[move[0]]
        start_row = int(move[1])
        end_col = self.rowDict[move[2]]
        end_row = int(move[3])

        row_diff = end_row - start_row
        col_diff = end_col - start_col
        print(start_row)
        print(start_col)
        # Check if it is a diagonal move
        if abs(row_diff) == abs(col_diff):
            if self.turn == "w":
                row_dir = 1 if row_diff > 0 else -1
                col_dir = 1 if col_diff > 0 else -1
                start_row_mat, start_col_mat = self.chessToMatrix(move[:2])
                # Check if any squares in the diagonal path are occupied
                
                while row != end_row and col != end_col:
                    row_mat, col_mat = indexToMatrix(row, col)
                    if start_row_mat != row_mat and start_col_mat != col_mat:
                        row_mat, col_mat = indexToMatrix(row, col)
                        print(row_mat, col_mat)
                        if self.board[row_mat][col_mat] != 0:
                            return False
                    row += row_dir
                    col += col_dir
            if self.turn == "b":
                row_dir = 1 if row_diff > 0 else -1
                col_dir = 1 if col_diff > 0 else -1
                start_row_mat, start_col_mat = self.chessToMatrix(move[:2])
                
                while row != end_row and col != end_col:
                    
                    row_mat, col_mat = indexToMatrix(row, col)
                    print(row_mat, col_mat)
                    if self.board[row_mat][col_mat] != 0:
                        return False
                    row -= row_dir
                    col -= col_dir

        # Check if it is a straight line move (horizontal or vertical)
        elif row_diff == 0 or col_diff == 0:

            

            if self.turn == "w":
                row_dir = 0 if row_diff == 0 else 1
                col_dir = 0 if col_diff == 0 else 1

                row = start_row + row_dir
                col = start_col + col_dir
               
                # Check if any squares in the straight path are occupied
                while row != end_row or col != end_col:

                    row_mat, col_mat = indexToMatrix(row, col)
                    print("RowMat, ColMat")
                    print(row_mat,col_mat)
                    
                    if self.board[row_mat][col_mat] != 0:
                        return False
                    row += row_dir
                    col += col_dir
            if self.turn == "b":
                row_dir = 0 if row_diff == 0 else 1
                col_dir = 0 if col_diff == 0 else 1

                row = start_row - row_dir
                col = start_col - col_dir

                # Check if any squares in the straight path are occupied
                while row != end_row or col != end_col:

                    row_mat, col_mat = indexToMatrix(row, col)
                    
                    if self.board[row_mat][col_mat] != 0:
                        return False
                    row -= row_dir
                    col -= col_dir

        # Return True if it is a valid path (no pieces in the way)
        return True


def fen_to_matrix(fen):
    # Create an empty 8x8 matrix
    matrix = [[0] * 8 for _ in range(8)]

    # Split the FEN string into different parts
    parts = fen.split()
    board_fen = parts[0]  # FEN representation of the chessboard

    # Map FEN characters to their corresponding piece values
    piece_values = {
        'P': 'PW',
        'N': 'NW',
        'B': 'BW',
        'R': 'RW',
        'Q': 'QW',
        'K': 'KW',
        'p': 'PB',
        'n': 'NB',
        'b': 'BB',
        'r': 'RB',
        'q': 'QB',
        'k': 'KB'
    }


    # Convert FEN representation to the matrix
    row, col = 7, 0  # Starting position (8th rank, first file)
    for char in board_fen:
        if char == '/':  # Move to the next rank
            row -= 1
            col = 0
        elif char.isdigit():  # Skip empty squares
            col += int(char)
        else:  # Place the piece on the matrix
            matrix[row][col] = piece_values[char]
            col += 1

    return np.flipud(matrix)

def indexToMatrix(row,col):
    return 8-row+1,col-1