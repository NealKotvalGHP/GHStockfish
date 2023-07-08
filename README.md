# GHStockfish

- [x] Board Class Created
- [x] Piece Class Created
- [x] Make Moves
- [x] FEN to Matrix
- [x] Pawn Logic + Generate Moves
- [ ] En Passant
- [x] Rook Logic + Generate Moves
- [ ] Knight Logic + Generate Moves
- [ ] Bishop Logic + Generate Moves
- [ ] Queen Logic + Generate Moves
- [ ] King Logic + Generate Moves
- [ ] Generate Moves Via Engine
- [ ] Random Moves
- [ ] Evaluation Function
- [ ] Transposition Table
- [ ] Openings
- [ ] Machine Learning?

# Board Class Documentation

The `Board` class represents a chess board and is used to handle the state of the board. It utilizes an 8x8 matrix to represent the positions of the chess pieces on the board.

### Class Attributes:

- `fen`: A string representing the FEN (Forsyth–Edwards Notation) notation of the current state of the chess board.
- `board`: A 2-dimensional list representing the 8x8 matrix of the chess board.
- `turn`: A string representing the current turn, either 'w' for white or 'b' for black.
- `letToNum`: A dictionary mapping chess notation letters (a-h) to column numbers (1-8).
- `numToLet`: A dictionary mapping column numbers (1-8) to chess notation letters (a-h).

### Class Methods:

- `__init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")`: Initializes a `Board` object with the given FEN notation or the default starting position.
- `initialize(self)`: Resets the board to the starting position.
- `print_board(self)`: Prints the current state of the chess board in a fancy format.
- `get_board(self)`: Returns the current state of the chess board as a 2-dimensional list.
- `get_turn(self)`: Returns the current turn, either 'w' for white or 'b' for black.
- `get_piece(self, index)`: Returns the chess piece object at the given chessDex (e.g., "e4").
- `make_move(self, move)`: Makes a move on the chess board based on the given chessDex move (e.g., "e2e4").
- `is_valid_move(self, col, row, selfColor)`: Checks if a square can be moved to based on the given column, row, and selfColor (current player color).
- `isEmptyColRow(self, col, row)`: Checks if a square at the given column and row is empty.
- `xyToChess(self, col, row)`: Converts the column and row coordinates to chessDex notation (e.g., "e4").
- `chessToMatrix(self, chessDex)`: Converts the chessDex notation (e.g., "e4") to matrix index coordinates.
- `is_enemy_piece(self, col, row, color)`: Checks if there is an enemy piece at the given column and row coordinates.

### Helper Functions:

- `fen_to_matrix(fen)`: Converts the FEN notation to an 8x8 matrix representing the chess board.
- `indexToMatrix(col, row)`: Converts the column and row coordinates to matrix index coordinates.

**Note:** The code provided contains additional comments that explain the functionality and quirks of the implementation. It's recommended to review those comments for better understanding of the code.
