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
  - ✅ En Passant
- ✅ Rook Logic + Generate Moves 
- ✅ Knight Logic + Generate Moves
- ✅ Bishop Logic + Generate Moves
- ✅ Queen Logic + Generate Moves
- ✅ King Logic + Generate Moves
  - ✅ Castling
  - ✅ Check
  - ✅ Checkmate
- ✅ Edge Cases
- ✅ Generate Moves Via Engine
- ❌ Random Moves
- ❌ Evaluation Function
- ❌ Transposition Table
- ❌ Openings
- ❌ Machine Learning?


# ChessSim Documentation

The `ChessSim` class is a Python implementation of a simplified chess simulator. It allows you to simulate and play out chess games using a command-line interface. This documentation provides an overview of the code and its functionalities.

## Class: ChessSim

### Initialization

```python
def __init__(self)
```

The constructor initializes the `ChessSim` object and sets up the initial state of the chess game. It defines various instance variables to track the game state, including the chessboard position, selected location, legal moves, en passant opportunity, current turn, castling rights, reached positions, move number, promoting pawn flag, piece type translation, piece ID translation, piece type to value translation, piece type to sufficiency value translation, game end flag, and game result.

### Method: game

```python
def game(self)
```

This method starts the chess game by printing the initial board state and playing two sample moves (`e2e4` and `e7e5`). It serves as a simple example of how to use the other methods to play moves in the game.

### Method: printBoard

```python
def printBoard(self)
```

This method prints the current chessboard state to the console. It displays the list of positions representing the chessboard and the pieces' arrangement.

### Method: movePiece

```python
def movePiece(self, origin, destination, promotionType)
```

This method handles the movement of a chess piece from the origin to the destination square. It takes three arguments: `origin` (the starting square index), `destination` (the target square index), and `promotionType` (the piece type for pawn promotion). It performs various checks, such as legality of the move, capturing, castling, en passant, pawn promotion, switch of turns, and updating the game state.

### Method: castling

```python
def castling(self, destination)
```

This method handles the castling move for the king and rooks. It takes the `destination` square index as an argument and updates the chessboard position and castling rights accordingly.

### Method: promoteTo

```python
def promoteTo(self, pieceType, pieceColor)
```

This method handles the promotion of a pawn to a different piece type. It takes `pieceType` (the type of the promoted piece) and `pieceColor` (the color of the promoted piece) as arguments. It updates the chessboard position and checks for game end conditions.

### Method: enPassant

```python
def enPassant(self, pieceType, pieceColor, destination)
```

This method handles the en passant capture move. It takes `pieceType` (the type of the moving piece), `pieceColor` (the color of the moving piece), and `destination` (the destination square index) as arguments. It updates the chessboard position accordingly.

### Method: gameEndLogic

```python
def gameEndLogic(self)
```

This method checks for various game end conditions, such as checkmate, stalemate, the 50-move rule, threefold repetition, and insufficient material. It updates the game end flag and result accordingly.

### Method: findLegalMoves

```python
def findLegalMoves(self, origin, pieceType, pieceColor)
```

This method finds all legal moves for a given chess piece at the `origin` square. It takes `origin` (the square index of the piece), `pieceType` (the type of the piece), and `pieceColor` (the color of the piece) as arguments. It returns a list of legal destination square indices.

### Method: inCheck

```python
def inCheck(self, testPosition, turn)
```

This method checks if the king of the specified `turn` color is in check in the given `testPosition`. It takes `testPosition` (the position to test) and `turn` (the current turn color) as arguments. It returns `True` if the king is in check, otherwise `False`.

### Helper Methods

The following methods are also defined within the `ChessSim` class:

- `color(self, pieceID)`: Returns the color of a piece based on its `pieceID`.
- `oppositeColor(self, color)`: Returns the opposite color of the specified `color`.
- `rank(self, squareIndex)`: Returns the rank (row) of the specified `squareIndex`.
- `file(self, squareIndex)`: Returns the file (column) of the specified `squareIndex`.
- `printMoveNumberPhrase(self)`: Prints the current move number phrase.

## Conclusion

The `ChessSim` class provides a simple implementation of a chess simulator. It allows you to simulate chess games, make moves, and check for game end conditions. By utilizing the provided methods and variables, you can extend the functionality of this class to create your own chess AI or user interface. Enjoy playing chess with the `ChessSim`!

