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

ChessPiece Class Documentation
The ChessPiece class is a superclass for all chess pieces. It represents a generic chess piece and provides a common attribute for all pieces, which is the color of the piece.

Class Attributes:
color: A string representing the color of the chess piece ("w" for white or "b" for black).
Class Methods:
__init__(self, color): Initializes a ChessPiece object with the given color.
__str__(self): Returns a string representation of the chess piece. This method is overridden in the subclasses.
Pawn Class Documentation
The Pawn class represents a pawn chess piece. It inherits from the ChessPiece superclass and adds an additional attribute for en passant moves.

Class Attributes:
color: A string representing the color of the pawn ("w" for white or "b" for black).
rowDict: A dictionary mapping row numbers to chess notation letters for pawn promotion.
en_passant_possible: A boolean indicating if the pawn can be captured en passant.
Class Methods:
__init__(self, color): Initializes a Pawn object with the given color.
valid_moves(self, board, col, row): Returns a list of valid moves for the pawn on the chess board.
__str__(self): Returns a string representation of the pawn.
Rook Class Documentation
The Rook class represents a rook chess piece. It inherits from the ChessPiece superclass.

Class Attributes:
color: A string representing the color of the rook ("w" for white or "b" for black).
can_castle: A boolean indicating if the rook can participate in castling.
Class Methods:
__init__(self, color): Initializes a Rook object with the given color.
valid_moves(self, board, col, row): Returns a list of valid moves for the rook on the chess board.
__str__(self): Returns a string representation of the rook.
Knight Class Documentation
The Knight class represents a knight chess piece. It inherits from the ChessPiece superclass.

Class Attributes:
color: A string representing the color of the knight ("w" for white or "b" for black).
Class Methods:
__init__(self, color): Initializes a Knight object with the given color.
valid_moves(self, board, col, row): Returns a list of valid moves for the knight on the chess board.
__str__(self): Returns a string representation of the knight.
Bishop Class Documentation
The Bishop class represents a bishop chess piece. It inherits from the ChessPiece superclass.

Class Attributes:
color: A string representing the color of the bishop ("w" for white or "b" for black).
Class Methods:
__init__(self, color): Initializes a Bishop object with the given color.
valid_moves(self, board, col, row): Returns a list of valid moves for the bishop on the chess board.
__str__(self): Returns a string representation of the bishop.
Queen Class Documentation
The Queen class represents a queen chess piece. It inherits from the ChessPiece superclass.

Class Attributes:
color: A string representing the color of the queen ("w" for white or "b" for black).
Class Methods:
__init__(self, color): Initializes a Queen object with the given color.
valid_moves(self, board, col, row): Returns a list of valid moves for the queen on the chess board.
__str__(self): Returns a string representation of the queen.
King Class Documentation
The King class represents a king chess piece. It inherits from the ChessPiece superclass.

Class Attributes:
color: A string representing the color of the king ("w" for white or "b" for black).
can_castle: A boolean indicating if the king can participate in castling.
Class Methods:
__init__(self, color): Initializes a King object with the given color.
valid_moves(self, board, col, row): Returns a list of valid moves for the king on the chess board.
__str__(self): Returns a string representation of the king.
Note: The code provided contains additional comments that explain the functionality of the code. It's recommended to review those comments for better understanding of the implementation.
