from ChessSim import ChessSim
import math
from copy import copy
import numpy as np

class Agent:
    def __init__(self, color):
        self.color = color

    def evaluate(self, game):
        score = 0

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
    
    def playBestMove(self, game):
        legalMoves = self.generateAllLegalMoves(game)

        selectedMove = self.selectRandomMove(game, legalMoves)


        return selectedMove
    
    def selectRandomMove(self, game, legalMoves):
        selectedMove = ""
        promotion = False
        for location in range(len(legalMoves)):
            if len(legalMoves[location]) != 0:
                selectedMove = self.convertToCoordinates(location) + self.convertToCoordinates(legalMoves[location][0])
                if self.color == "w" and game.position[location] == 1 and selectedMove[3] == "8":
                    promotion = True
                elif self.color == "b" and game.position[location] == 7 and selectedMove[3] == "1":
                    promotion = True
                break
        if promotion:
            selectedMove = copy(selectedMove) + "Q"
        
        return selectedMove

    def convertToCoordinates(self, location):
        fileLabels = "abcdefgh"
        rankLabels = "12345678"

        file = fileLabels[location % 8]
        rank = rankLabels[7 - math.floor(location / 8)]

        return file + rank
    
    def generateAllLegalMoves(self, game):
        allLegalMoves = []
        for i in range(64):
            if game.color(game.position[i]) == game.currentTurn:
                piece = game.PIECE_ID_TRANSLATION[game.position[i]][0]
                pieceColor = game.PIECE_ID_TRANSLATION[game.position[i]][1]
                if game.currentTurn == pieceColor:
                    allLegalMoves.append(game.findLegalMoves(i, piece, pieceColor))
            else:
                allLegalMoves.append([])
        return allLegalMoves