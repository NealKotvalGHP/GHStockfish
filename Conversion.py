import numpy as np

def fen_to_matrix(fen):
    # Create an empty 8x8 matrix
    matrix = [[0] * 8 for _ in range(8)]

    # Split the FEN string into different parts
    parts = fen.split()
    board_fen = parts[0]  # FEN representation of the chessboard

    # Map FEN characters to their corresponding piece values
    piece_values = {
        'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,  # White pieces
        'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6  # Black pieces
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

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in fen_to_matrix(fen)]))
