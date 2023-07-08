# GHStockfish

- [x] Board Class Created
- [x] Piece Class Created
- [x] Make Moves
- [x] FEN to Matrix
- [x] Pawn Logic + Generate Moves
- [ ] En Passant
- [x] Rook Logic + Generate Moves
- [X] Knight Logic + Generate Moves
- [X] Bishop Logic + Generate Moves
- [X] Queen Logic + Generate Moves
- [X] King Logic + Generate Moves
- [ ] Castling
- [ ] Edge Cases
- [ ] Generate Moves Via Engine
- [ ] Random Moves
- [ ] Evaluation Function
- [ ] Transposition Table
- [ ] Openings
- [ ] Machine Learning?
# Board Class

The `Board` class represents a chessboard and provides methods to manage the state of the board and perform various operations.

## Class Overview

### Attributes

- `fen` (str): The FEN notation representing the current state of the board.
- `board` (numpy.ndarray): An 8x8 matrix representing the chessboard.
- `turn` (str): The current turn in the game ("w" for white, "b" for black).
- `letToNum` (dict): A dictionary mapping letters to column numbers.
- `numToLet` (dict): A dictionary mapping column numbers to letters.

### Methods

- `__init__(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")`: Initializes a new instance of the `Board` class.
- `initialize()`: Resets the board to the starting position.
- `printBoard()`: Prints the current state of the board.
- `getBoard() -> numpy.ndarray`: Returns the matrix representation of the board.
- `getTurn() -> str`: Returns the current turn.
- `getPiece(chessDex: str) -> ChessPiece`: Returns the chess piece object at the specified chessDex (e.g., "e4").
- `getPieceColRow(col: int, row: int) -> ChessPiece`: Returns the chess piece object at the specified column and row.
- `makeMove(move: str)`: Makes a move on the board based on the specified chessDex move (e.g., "e2e4").
- `isValidMove(col: int, row: int, selfColor: str) -> bool`: Checks if a move to the specified column and row is valid for the given color.
- `isEmptyColRow(col: int, row: int) -> bool`: Checks if the specified column and row on the board is empty.
- `xyToChess(col: int, row: int) -> str`: Converts column and row indices to chessDex notation (e.g., (1, 1) becomes "a1").
- `chessToMatrix(chessDex: str) -> Tuple[int, int]`: Converts chessDex notation to column and row indices.
- `isEnemyPiece(col: int, row: int, color: str) -> bool`: Checks if there is an enemy piece at the specified column and row for the given color.
- `printValidMoves(move: str)`: Prints the valid moves for the piece at the specified chessDex move.

### Helper Functions

- `fenToMatrix(fen: str) -> numpy.ndarray`: Converts a FEN notation to a matrix representation of the board.
- `indexToMatrix(col: int, row: int) -> Tuple[int, int]`: Converts column and row indices to matrix indices.

## Usage

### Creating a Board

```python
board = Board()
```

### Initializing the Board

```python
board.initialize()
```

### Getting the Current Turn

```python
turn = board.getTurn()
```

### Making a Move

```python
board.makeMove("e2e4")
```

### Getting the Piece at a Specific ChessDex

```python
piece = board.getPiece("e4")
```

### Printing the Valid Moves for a Move

```python
board.printValidMoves("e4")
```

### Checking if a Move is Valid

```python
isValid = board.isValidMove(5, 2, "w")
```

### Printing the Current State of the Board

```python
board.printBoard()
```

## Notes

- The board is represented as an 8x8 matrix, where the rows are numbered from 1 to 8 and the columns are represented by letters 'a' to 'h'.
- The `fen` attribute represents the current state of the board in Forsyth–Edwards Notation (FEN).
- The `board` attribute is a numpy ndarray where each element represents a chess piece object or 0 for an empty square.
- The `turn` attribute stores the current turn in the game, "w" for white and "b" for black.
- The `letToNum` and `numToLet` dictionaries are used for converting between letters and column numbers.
- The `makeMove` method updates the board state by moving a piece from one position to another.
- The `isValidMove` method checks if a move to a specific column and row is valid for the given color.
- The `printValidMoves` method prints the valid moves for the piece at a specified chessDex move.
- The `getPiece` method returns the chess piece object at a specified chessDex position.
- The `isEmptyColRow` method checks if a specific column and row on the board is empty.
- The `xyToChess` method converts column and row indices to chessDex notation.
- The `chessToMatrix` method converts chessDex notation to column and row indices.
- The `isEnemyPiece` method checks if there is an enemy piece at a specific column and row for the given color.

```


Please note that this documentation assumes the availability of the `ChessPiece` superclass and its subclasses (`Pawn`, `Rook`, `Knight`, `Bishop`, `Queen`, `King`) in the code.
