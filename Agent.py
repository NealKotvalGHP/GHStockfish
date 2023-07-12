from ChessSim import ChessSim
import math
from copy import copy
from copy import deepcopy
import numpy as np
import time

class Agent:
    
    def __init__(self, color, depth):
        self.color = color
        self.depth = depth
        self.nextEvaluations = []


    def minimax(self, game, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or game.gameEnded:
            if depth == self.depth - 1:
                self.nextEvaluations.append(self.evaluate(game))
            return self.evaluate(game)
        if maximizingPlayer:
            maxEval = float('-inf')
            moves = self.generateAllLegalMoves(game)
            for move in moves:
                branch = ChessSim(deepcopy(game.position), deepcopy(game.currentTurn), deepcopy(game.castlingRights), deepcopy(game.castlingPossible), deepcopy(game.enPassantOpportunity), deepcopy(game.reachedPositions))
                branch.playMove(self.convertToMove(move, branch))
                eval = self.minimax(branch, depth-1, deepcopy(alpha), deepcopy(beta), False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if depth == self.depth - 1:
                self.nextEvaluations.append(maxEval)
            return maxEval
        else:
            minEval = float('inf')
            moves = self.generateAllLegalMoves(game)
            for move in moves:
                branch = ChessSim(deepcopy(game.position), deepcopy(game.currentTurn), deepcopy(game.castlingRights), deepcopy(game.castlingPossible), deepcopy(game.enPassantOpportunity), deepcopy(game.reachedPositions))
                branch.playMove(self.convertToMove(move, branch))
                eval = self.minimax(branch, depth-1, deepcopy(alpha), deepcopy(beta), True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if depth == self.depth - 1:
                self.nextEvaluations.append(minEval)
            return minEval

    def evaluate(self, game):
        score = 0

        #positional advantage

        #heuristics

        #win/loss
        if game.gameEnded:
            if self.color == "w":
                if game.gameResult == 1:
                    score = float('inf')
                elif game.gameResult == -1:
                    score = float('-inf')
                else:
                    score = 0
            return score
        
        

        # initialize a variable to store the net piece difference of the board
        pieceDiff = 0
        # loop though all pieces on the board and add their weight to the pieceDiff variable
        for piece in game.position:
            pieceDiff += game.PIECE_ID_TO_VALUE_TRANSLATION[piece]
        # print("piece diff: " + str(pieceDiff))


        
        #positional advantages

        # PIECE MAPS !!!
        # init a variable to store the score of the avaluated positions
        netPositionScore = 0
        idxInBoard = -1

        
        for piece in game.position:
            idxInBoard += 1
            pieceType = game.PIECE_ID_TRANSLATION[piece][0]
            pieceColor = game.PIECE_ID_TRANSLATION[piece][1]
            
            if pieceColor == "w":
                if pieceType == "P":
                    netPositionScore += game.pawnWTable[idxInBoard]
                elif pieceType == "N":
                    netPositionScore += game.knightWTable[idxInBoard]
                elif pieceType == "B":
                    netPositionScore += game.bishopWTable[idxInBoard]
                elif pieceType == "R":
                    netPositionScore += game.rookWTable[idxInBoard]
                elif pieceType == "Q":
                    netPositionScore += game.queenWTable[idxInBoard]
            else:
                if pieceType == "P":
                    netPositionScore -= game.pawnBTable[idxInBoard]
                elif pieceType == "N":
                    netPositionScore -= game.knightBTable[idxInBoard]
                elif pieceType == "B":
                    netPositionScore -= game.bishopBTable[idxInBoard]
                elif pieceType == "R":
                    netPositionScore -= game.rookBTable[idxInBoard]
                elif pieceType == "Q":
                    netPositionScore -= game.queenBTable[idxInBoard]
        

        

        # print(netPositionScore)


        # DEBUG -> print the position in the shape of chessboard for readability
        # print(np.reshape(game.position, (8, 8)))



        #heuristics


        # combine all evaluations above and weigh them into the variable "score"
        

        score += (100 * pieceDiff) + (netPositionScore / 2)

        return score
    
    def playBestMove(self, game):
        start = time.time()

        self.nextEvaluations = []
        sim = copy(game)
        if self.color == "w":
            self.minimax(sim, self.depth, float('-inf'), float('inf'), True)
            bestEval = max(self.nextEvaluations)
        elif self.color == "b":
            self.minimax(sim, self.depth, float('-inf'), float('inf'), False)
            bestEval = min(self.nextEvaluations)
        bestMoveIndex = self.nextEvaluations.index(bestEval)
        bestMove = self.convertToMove(self.generateAllLegalMoves(sim)[bestMoveIndex], game)

        end = time.time()

        print(f"Move took: {end-start} seconds")
        
        return bestMove


    # move is a 2-tuple. 3-tuple if there is promotion information. Converts to string.
    def convertToMove(self, move, game):
        convertedMove = self.convertToCoordinates(move[0]) + self.convertToCoordinates(move[1])

        promotionType = ""
        if game.PIECE_ID_TRANSLATION[game.position[move[0]]][0] == "P":
            if convertedMove[3] == "8" and game.currentTurn == "w":
                promotionType = "Q"
            elif convertedMove[3] == "1" and game.currentTurn == "b":
                promotionType = "Q"
        
        return convertedMove + promotionType

    def convertToCoordinates(self, location):
        fileLabels = "abcdefgh"
        rankLabels = "12345678"

        file = fileLabels[location % 8]
        rank = rankLabels[7 - math.floor(location / 8)]

        return file + rank
    
    def generateAllLegalMoves(self, game):
        allLegalMoves = [(i, move) for i in range(64) if game.color(game.position[i]) == game.currentTurn
                        for move in game.findLegalMoves(i, *game.PIECE_ID_TRANSLATION[game.position[i]])]
        return allLegalMoves
