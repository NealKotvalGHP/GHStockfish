class Agent:
    def __init__(self, color, max_depth=3):
        self.color = color
        self.max_depth = max_depth

    def evaluate(self, board):
        # Evaluation function to assign a score to the board position
        # Implement your evaluation function here
        # Return a positive score if the position is favorable for self.color, negative if unfavorable, and 0 for neutral

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.get_possible_moves(self.color):
                board.make_move(move)
                eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                board.undo_move()

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.get_possible_moves(opposite_color(self.color)):
                board.make_move(move)
                eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                board.undo_move()

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_best_move(self, board):
        best_score = float('-inf')
        best_move = None

        for move in board.get_possible_moves(self.color):
            board.make_move(move)
            score = self.minimax_alpha_beta(board, self.max_depth - 1, float('-inf'), float('inf'), False)
            board.undo_move()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

def opposite_color(color):
    return "w" if color == "b" else "b"