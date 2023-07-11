import numpy as np
from ChessSim import ChessSim

class Agent:
    def __init__(self, color):
        self.color = color

    def evaluate(self, game):
        score = 0

        # first check if game is over, if so, assign -inf or +inf to score
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



        # This function evaluates the current state of the board and returns a score
        # You need to define your own evaluation function based on the specific game



        # initialize a variable to store the net piece difference of the board
        pieceDiff = 0
        # loop though all pieces on the board and add their weight to the pieceDiff variable
        for piece in game.position:
            pieceDiff += game.PIECE_ID_TO_VALUE_TRANSLATION[piece]
        # print("piece diff: " + str(pieceDiff))



        #positional advantages

        # all pieces on back 2 ranks
        # positive "back2RanksDiff" means white has that much more material on their first 2 ranks (bad for white)
        # negative means black has that much more material on their back 2 ranks (bad for black)
        back2RanksDiff = 0
        whiteBack2Ranks = game.position[:16]
        blackBack2Ranks = game.position[-16:]

        for piece in whiteBack2Ranks:
            # dont count the king and dont count opposite colored pieces
            if game.PIECE_ID_TO_VALUE_TRANSLATION[piece] > 0 and game.PIECE_ID_TO_VALUE_TRANSLATION[piece] != 9999:
                back2RanksDiff += game.PIECE_ID_TO_VALUE_TRANSLATION[piece]
            
        
        for piece in blackBack2Ranks:
            # dont count the king and dont count opposite colored pieces
            if game.PIECE_ID_TO_VALUE_TRANSLATION[piece] < 0 and game.PIECE_ID_TO_VALUE_TRANSLATION[piece] != -9999:
                back2RanksDiff += game.PIECE_ID_TO_VALUE_TRANSLATION[piece]
        
        # list of piece IDs on the 4 center squares of board + find difference
        # positive difference is bad for white, good for black
        # negative is bad for black, good for white
        centerSquares = [game.position[27], game.position[28], game.position[35], game.position[36]]
        centerPawnsDiff = centerSquares.count(1) - centerSquares.count(7)
        
            
        # DEBUG -> print the position in the shape of chessboard for readability
        print(np.reshape(game.position, (8, 8)))



        #heuristics


        # combine all evaluations above and weigh them into the variable "score"

        score = (pieceDiff - (back2RanksDiff / 7) - (centerPawnsDiff / 2))
        return score
    
    def make_best_move(game):
        legalMoves = game.generateAllLegalMoves()
        


    