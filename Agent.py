from ChessSim import ChessSim

class Agent:
    def __init__(self, color):
        self.color = color

    def evaluate(self, game):
        score = 0

        # This function evaluates the current state of the board and returns a score
        # You need to define your own evaluation function based on the specific game


        # FIRST
        # initialize a variable to store the net piece difference of the board
        pieceDiff = 0
        # loop though all pieces on the board and add their weight to the pieceDiff variable
        for piece in game.position:
            pieceDiff += game.PIECE_ID_TO_VALUE_TRANSLATION[piece]
        print(pieceDiff)

        #positional advantage

        #heuristics

        #win/loss
        if game.gameEnded:
            if self.color == "w":
                if game.gameResult == 1:
                    score = float('+inf')
                elif game.gameResult == -1:
                    score = float('-inf')
                else:
                    score = 0
            else:
                if game.gameResult == 1:
                    score = float('-inf')
                elif game.gameResult == -1:
                    score = float('+inf')
                else:
                    score = 0

        return score
    
    def make_best_move(game):
        legalMoves = game.generateAllLegalMoves()
        


    