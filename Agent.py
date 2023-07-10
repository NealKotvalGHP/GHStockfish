from ChessSim import ChessSim

class Agent:
    def __init__(self, color):
        self.color = color
        pass

    def evaluate(self):

        sim = ChessSim()

        sim.run()

        # initialize a variable to store the net piece difference of the board
        score = 0

        # loop though all pieces on the board and add their weight to the score variable
        for piece in sim.position:
            score += sim.PIECE_ID_TO_VALUE_TRANSLATION[piece]

        print(score)


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

    


Agent.evaluate(Agent)