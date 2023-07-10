from ChessSim import ChessSim

class Agent:
    def __init__(self, color):
        self.color = color
        pass

    def evaluate(self, game):
        score = 0
        # This function evaluates the current state of the board and returns a score
        # You need to define your own evaluation function based on the specific game

        #add up piece value

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

    


