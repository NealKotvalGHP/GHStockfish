# GHStockfish
<p align="center">
  <img src="https://github.com/NealKotvalGHP/GHStockfish/assets/137081101/1203b9c2-8d3a-4e57-84e1-cefe4b5c3029" alt="Logo" width="300" height="300">
</p>
## Checklist

- ✅ Board Class Created 
- ✅ Piece Class Created
- ✅ Make Moves
- ✅ FEN to Matrix
- ✅ Pawn Logic + Generate Moves
  - ❌ En Passant
- ✅ Rook Logic + Generate Moves 
- ✅ Knight Logic + Generate Moves
- ✅ Bishop Logic + Generate Moves
- ✅ Queen Logic + Generate Moves
- ✅ King Logic + Generate Moves
  - ❌ Castling
  - ❌ Check
  - ❌ Checkmate
- ❌ Edge Cases
- ✅ Generate Moves Via Engine
- ✅ Random Moves
- ❌ Evaluation Function
- ❌ Transposition Table
- ❌ Openings
- ❌ Machine Learning?

# ChessGame Class

The `ChessGame` class represents a chess game and provides methods to play moves, determine legal moves, check for check, and perform other operations related to chess gameplay.

## Methods

### `findLegalMoves(origin, pieceType, pieceColor)`

This method finds the legal moves for a given piece at a given position.

- `origin`: The starting position of the piece on the chessboard.
- `pieceType`: The type of the piece (e.g., "P" for pawn, "R" for rook).
- `pieceColor`: The color of the piece ("w" for white, "b" for black).
- Returns: A list of possible destination squares that are legal moves for the piece.

### `inCheck(testPosition, turn)`

This method checks if the current player is in check in a given position.

- `testPosition`: The position to check for check.
- `turn`: The color of the current player.
- Returns: `True` if the current player is in check, `False` otherwise.

### `color(typeId)`

This method determines the color of a piece based on its type ID.

- `typeId`: The type ID of the piece.
- Returns: The color of the piece ("w" for white, "b" for black).

### `file(location)`

This method determines the file (column) of a given location on the chessboard.

- `location`: The location on the chessboard.
- Returns: The file (column) of the location.

### `rank(location)`

This method determines the rank (row) of a given location on the chessboard.

- `location`: The location on the chessboard.
- Returns: The rank (row) of the location.

### `oppositeColor(color)`

This method determines the opposite color of a given color.

- `color`: The color for which to determine the opposite color.
- Returns: The opposite color.

### `switchTurn()`

This method switches the current turn to the opposite color.

### `printMoveNumberPhrase()`

This method prints the move number and the current player's turn.

### `playMove(move)`

This method plays a move on the chessboard.

- `move`: The move to be played.
- Returns: None.

### `convertToLocation(coordinates)`

This method converts chess algebraic notation coordinates to a location on the chessboard.

- `coordinates`: The algebraic notation coordinates (e.g., "e4").
- Returns: The corresponding location on the chessboard.

## Usage

Here's an example of how to use the `ChessGame` class:

```python
# Create a new chess game
game = ChessGame()

# Print the move number and current player's turn
game.printMoveNumberPhrase()

# Play a move
move = "e2e4"
game.playMove(move)

# Find the legal moves for a piece at a given position
origin = game.convertToLocation("e2")
pieceType = "P"
pieceColor = "w"
legalMoves = game.findLegalMoves(origin, pieceType, pieceColor)

# Check if the current player is in check
testPosition = game.getPosition()
turn = game.getCurrentTurn()
inCheck = game.inCheck(testPosition, turn)
