from copy import copy
import math

class ChessSim:
    def __init__(self, INITIAL_POSITION, startingTurn, castlingRights, enPassantOpportunity, reachedPositions):
        self.INITIAL_POSITION = INITIAL_POSITION

        self.position = copy(self.INITIAL_POSITION)

        self.selectedLocation = -1

        self.legalMoves = []

        self.enPassantOpportunity = enPassantOpportunity

        self.currentTurn = startingTurn

        self.castlingRights = castlingRights

        self.castlingPossible = [[False, False], [False, False]]

        self.reachedPositions = reachedPositions

        self.moveNumber = 1

        self.promotingPawn = False

        self.isCastling = False

        self.PIECE_TYPE_TRANSLATION = {
            ("P", "w") : 1,
            ("R", "w") : 2,
            ("N", "w") : 3,
            ("B", "w") : 4,
            ("Q", "w") : 5,
            ("K", "w") : 6,
            ("P", "b") : 7,
            ("R", "b") : 8,
            ("N", "b") : 9,
            ("B", "b") : 10,
            ("Q", "b") : 11,
            ("K", "b") : 12
        }

        self.PIECE_ID_TRANSLATION = {
            0 : ("", ""),
            1 : ("P", "w"),
            2 : ("R", "w"),
            3 : ("N", "w"),
            4 : ("B", "w"),
            5 : ("Q", "w"),
            6 : ("K", "w"),
            7 : ("P", "b"),
            8 : ("R", "b"),
            9 : ("N", "b"),
            10 : ("B", "b"),
            11 : ("Q", "b"),
            12 : ("K", "b")
        }
        print
        self.PIECE_TYPE_TO_VALUE_TRANSLATION = {
            "P" : 1,
            "R" : 5,
            "N" : 3,
            "B" : 3,
            "Q" : 9,
            "K" : 0
        }

        self.PIECE_ID_TO_VALUE_TRANSLATION = {
            0 : 0,
            1 : 1,
            2 : 5,
            3 : 3,
            4 : 3,
            5 : 9,
            6 : 0,
            7 : -1,
            8 : -5,
            9 : -3,
            10 : -3,
            11 : -9,
            12 : 0
        }

        self.PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION = {
            "P" : 100,
            "R" : 100,
            "N" : 50,
            "B" : 50,
            "Q" : 100,
            "K" : 0
        }

        self.pawnWTable = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

        self.knightWTable = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,
        ]

        self.bishopWTable = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ]

        self.rookWTable = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0
        ]

        self.queenWTable = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -5,  0,  5,  5,  5,  5,  0, -5,
            0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]

        self.kingMidWTable = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            20, 20,  0,  0,  0,  0, 20, 20,
            20, 30, 10,  0,  0, 10, 30, 20
        ]

        self.kingEndWTable = [
            -50,-40,-30,-20,-20,-30,-40,-50,
            -30,-20,-10,  0,  0,-10,-20,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-30,  0,  0,  0,  0,-30,-30,
            -50,-30,-30,-30,-30,-30,-30,-50
        ]

        self.pawnBTable = [
            0,   0,   0,   0,   0,   0,   0,   0,   
            5,  10,  10, -20, -20,  10,  10,   5,
            5,  -5,  -10,   0,   0, -10,  -5,   5,
            0,   0,   0,  20,  20,   0,   0,   0,
            5,   5,  10,  25,  25,  10,   5,   5,
            10,  10,  20,  30,  30,  20,  10,  10,
            50,  50,  50,  50,  50,  50,  50,  50,
            0,   0,   0,   0,   0,   0,   0,   0
        ]

        self.knightBTable = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]

        self.bishopBTable = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]

        self.rookBTable = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        self.queenBTable = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 5, 0, -10,
            -10, 0, 5, 5, 5, 5, 5, -10,
            -5, 0, 5, 5, 5, 5, 0, 0,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]

        self.kingMidBTable = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30
        ]

        self.kingEndBTable = [
            -50, -30, -30, -30, -30, -30, -30, -50,
            -30, -30, 0, 0, 0, 0, -30, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -20, -10, 0, 0, -10, -20, -30,
            -50, -40, -30, -20, -20, -30, -40, -50
        ]

        self.INITIAL_ID_POSITION = [
            25, 27, 29, 31, 32, 30, 28, 26,
            17, 18, 19, 20, 21, 22, 23, 24,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            1, 2, 3, 4, 5, 6, 7, 8,
            9, 11, 13, 15, 16, 14, 12, 10
        ]


        self.gameEnded = False
        self.gameResult = 0

    def run(self):
        self.printBoard()

    def printBoard(self):
        print(self.position)

    def movePiece(self, origin, destination, promotionType):
        self.selectedLocation = copy(origin)
        positionCopy = copy(self.position)
        capture = False
        self.legalMoves = self.findLegalMoves(origin, self.PIECE_ID_TRANSLATION[positionCopy[origin]][0], self.PIECE_ID_TRANSLATION[positionCopy[origin]][1])

        if not self.promotingPawn and not self.gameEnded:
            if (destination >= 0 and destination < 64 and self.legalMoves.count(destination) != 0) or self.isCastling:
                self.position[origin] = 0
                if positionCopy[destination] != 0:
                    capture = True
                self.position[destination] = positionCopy[origin]

                self.castling(destination)
                
                if self.PIECE_ID_TRANSLATION[positionCopy[origin]][0] == "P" and ((self.PIECE_ID_TRANSLATION[positionCopy[origin]][1] == "w" and destination < 8) or (self.PIECE_ID_TRANSLATION[positionCopy[origin]][1] == "b" and destination >= 56)):
                    self.promoteTo(promotionType, self.PIECE_ID_TRANSLATION[positionCopy[origin]][1])
                
                self.enPassant(self.PIECE_ID_TRANSLATION[positionCopy[origin]][0], self.PIECE_ID_TRANSLATION[positionCopy[origin]][1], destination)
                if self.PIECE_ID_TRANSLATION[positionCopy[origin]][0] == "P" and abs(origin - destination) == 16:
                    self.enPassantOpportunity = math.floor((origin + destination) / 2)
                else:
                    self.enPassantOpportunity = -1
                
                if not self.isCastling:
                    self.switchTurn()


                enPassantOpportunityLocal = copy(self.enPassantOpportunity)
                for location in range(len(self.position)):
                    if self.PIECE_ID_TRANSLATION[self.position[location]] == ("P", self.currentTurn):
                        if self.findLegalMoves(location, "P", self.currentTurn).count(self.enPassantOpportunity) == 0:
                            enPassantOpportunityLocal = -1
                        else:
                            enPassantOpportunityLocal = math.floor((origin + destination) / 2)
                            break
                self.enPassantOpportunity = enPassantOpportunityLocal

                if self.currentTurn == "w" and not self.isCastling:
                    self.moveNumber += 1

                if not self.promotingPawn and not self.isCastling:
                    if self.PIECE_ID_TRANSLATION[positionCopy[origin]][0] == "P" or capture:
                        self.reachedPositions.clear()
                    self.reachedPositions.append([copy(self.position), copy(self.currentTurn), copy(self.castlingRights), copy(self.enPassantOpportunity)])
                    self.gameEndLogic()
            else:
                print("Error: Illegal move.")
                print(destination)
        

        self.selectedLocation = -1

    def castling(self, destination):
        if self.castlingPossible[0][0] and destination == 62:
            self.isCastling = True
            self.movePiece(63, 61, "")
            self.castlingRights[0] = [False, False]
            self.isCastling = False
        elif self.castlingPossible[0][1] and destination == 58:
            self.isCastling = True
            self.movePiece(56, 59, "")
            self.castlingRights[0] = [False, False]
            self.isCastling = False
        elif self.castlingPossible[1][0] and destination == 6:
            self.isCastling = True
            self.movePiece(7, 5, "")
            self.castlingRights[1] = [False, False]
            self.isCastling = False
        elif self.castlingPossible[1][1] and destination == 2:
            self.isCastling = True
            self.movePiece(0, 3, "")
            self.castlingRights[1] = [False, False]
            self.isCastling = False
            
        if self.PIECE_ID_TRANSLATION[self.position[self.selectedLocation]][0] == "K":
            if self.PIECE_ID_TRANSLATION[self.position[self.selectedLocation]][1] == "w":
                self.castlingRights[0] = [False, False]
            elif self.PIECE_ID_TRANSLATION[self.position[self.selectedLocation]][1] == "b":
                self.castlingRights[1] = [False, False]
            
        if self.position[63] != self.PIECE_TYPE_TRANSLATION[("R", "w")]:
            self.castlingRights[0][0] = False
        if self.position[56] != self.PIECE_TYPE_TRANSLATION[("R", "w")]:
            self.castlingRights[0][1] = False
        if self.position[7] != self.PIECE_TYPE_TRANSLATION[("R", "b")]:
            self.castlingRights[1][0] = False
        if self.position[0] != self.PIECE_TYPE_TRANSLATION[("R", "b")]:
            self.castlingRights[1][1] = False

    def promoteTo(self, pieceType, pieceColor):
        promotionLocation = -1
        if pieceColor == "w":
            for location in range(0, 8):
                if self.position[location] == self.PIECE_TYPE_TRANSLATION[("P", "w")]:
                    promotionLocation = location
                    break
        elif pieceColor == "b":
            for location in range(56, 64):
                if self.position[location] == self.PIECE_TYPE_TRANSLATION[("P", "b")]:
                    promotionLocation = location
                    break

        self.position[promotionLocation] = self.PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]

        self.reachedPositions.clear()
        self.reachedPositions.append([copy(self.position), copy(self.currentTurn), copy(self.castlingRights), copy(self.enPassantOpportunity)])
        self.gameEndLogic()

    def enPassant(self, pieceType, pieceColor, destination):
        if pieceType == "P" and self.enPassantOpportunity == destination:
            if pieceColor == "w":
                self.position[destination + 8] = 0
            elif pieceColor == "b":
                self.position[destination - 8] = 0

    def gameEndLogic(self):
        movablePieces = False
        for location in range(len(self.position)):
            if self.color(self.position[location]) == self.currentTurn:
                if len(self.findLegalMoves(location, self.PIECE_ID_TRANSLATION[self.position[location]][0], self.currentTurn)) != 0:
                    movablePieces = True
                    break
        if self.inCheck(self.position, self.currentTurn) and not movablePieces:
            if self.currentTurn == "w":
                # Black wins by checkmate.
                self.gameEnded = True
                self.gameResult = -1
                pass
            elif self.currentTurn == "b":
                # White wins by checkmate.
                self.gameEnded = True
                self.gameResult = 1
                pass
        elif not movablePieces:
            # The game is a draw by stalemate.
            self.gameEnded = True
            pass
        
        if len(self.reachedPositions) > 100:
            # The game is a draw by the 50-move rule.
            self.gameEnded = True
            pass

        repetitionCounter = 0
        for absolutePosition in self.reachedPositions:
            if absolutePosition == self.reachedPositions[len(self.reachedPositions) - 1]:
                repetitionCounter += 1
                if repetitionCounter == 3:
                    # The game is a draw by threefold repetition.
                    self.gameEnded = True
                    pass
        
        totalSufficiencyMaterial = 0
        bishopColors = ["", ""]
        for location in range(len(self.position)):
            if self.position[location] != 0:
                if self.PIECE_ID_TRANSLATION[self.position[location]][0] == "B":
                    if bishopColors == ["", ""]:
                        totalSufficiencyMaterial += self.PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION[self.PIECE_ID_TRANSLATION[self.position[location]][0]]
                    if (location % 2 + math.floor(location / 8)) % 2 == 0:
                        bishopColors[0] = "l"
                    else:
                        bishopColors[1] = "d"
                    if bishopColors == ["l", "d"]:
                        totalSufficiencyMaterial += self.PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION[self.PIECE_ID_TRANSLATION[self.position[location]][0]]
                else:
                    totalSufficiencyMaterial += self.PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION[self.PIECE_ID_TRANSLATION[self.position[location]][0]]
                
                if totalSufficiencyMaterial >= 100:
                    break
        if totalSufficiencyMaterial < 100:
            # The game is a draw by insufficient material.
            self.gameEnded = True
            pass

    def findLegalMoves(self, origin, pieceType, pieceColor):
        possibleDestinationSquares = []

        if pieceColor != self.currentTurn:
            return []
        if pieceType == "P":
            if pieceColor == "w":
                if self.position[origin - 8] == 0:
                    possibleDestinationSquares.append(origin - 8)
                    if self.rank(origin) == 2 and self.position[origin - 16] == 0:
                        possibleDestinationSquares.append(origin - 16)
                if self.file(origin) + 1 <= 8 and (self.color(self.position[origin - 7]) == "b" or self.enPassantOpportunity == origin - 7):
                    possibleDestinationSquares.append(origin - 7)
                if self.file(origin) - 1 > 0 and (self.color(self.position[origin - 9]) == "b" or self.enPassantOpportunity == origin - 9):
                    possibleDestinationSquares.append(origin - 9)
            elif pieceColor == "b":
                if self.position[origin + 8] == 0:
                    possibleDestinationSquares.append(origin + 8)
                    if self.rank(origin) == 7 and self.position[origin + 16] == 0:
                        possibleDestinationSquares.append(origin + 16)
                if self.file(origin) - 1 > 0 and (self.color(self.position[origin + 7]) == "w" or self.enPassantOpportunity == origin + 7):
                    possibleDestinationSquares.append(origin + 7)
                if self.file(origin) + 1 <= 8 and (self.color(self.position[origin + 9]) == "w" or self.enPassantOpportunity == origin + 9):
                    possibleDestinationSquares.append(origin + 9)
        elif pieceType == "R" or pieceType == "Q":
            for distanceNorth in range(1, 8):
                if self.rank(origin) + distanceNorth <= 8:
                    if self.position[origin - (8 * distanceNorth)] == 0:
                        possibleDestinationSquares.append(origin - (8 * distanceNorth))
                    elif self.color(self.position[origin - (8 * distanceNorth)]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - (8 * distanceNorth))
                        break
                    elif self.color(self.position[origin - (8 * distanceNorth)]) == pieceColor:
                        break
                else:
                    break
            for distanceEast in range(1, 8):
                if self.file(origin) + distanceEast <= 8:
                    if self.position[origin + distanceEast] == 0:
                        possibleDestinationSquares.append(origin + distanceEast)
                    elif self.color(self.position[origin + distanceEast]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + distanceEast)
                        break
                    elif self.color(self.position[origin + distanceEast]) == pieceColor:
                        break
                else:
                    break
            for distanceSouth in range(1, 8):
                if self.rank(origin) - distanceSouth > 0:
                    if self.position[origin + (8 * distanceSouth)] == 0:
                        possibleDestinationSquares.append(origin + (8 * distanceSouth))
                    elif self.color(self.position[origin + (8 * distanceSouth)]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + (8 * distanceSouth))
                        break
                    elif self.color(self.position[origin + (8 * distanceSouth)]) == pieceColor:
                        break
                else:
                    break
            for distanceWest in range(1, 8):
                if self.file(origin) - distanceWest > 0:
                    if self.position[origin - distanceWest] == 0:
                        possibleDestinationSquares.append(origin - distanceWest)
                    elif self.color(self.position[origin - distanceWest]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - distanceWest)
                        break
                    elif self.color(self.position[origin - distanceWest]) == pieceColor:
                        break
                else:
                    break
        elif pieceType == "N":
            if self.rank(origin) + 2 <= 8 and self.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin - 17)
            if self.rank(origin) + 2 <= 8 and self.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin - 15)
            if self.rank(origin) + 1 <= 8 and self.file(origin) - 2 > 0:
                possibleDestinationSquares.append(origin - 10)
            if self.rank(origin) + 1 <= 8 and self.file(origin) + 2 <= 8:
                possibleDestinationSquares.append(origin - 6)
            if self.rank(origin) - 1 > 0 and self.file(origin) - 2 > 0:
                possibleDestinationSquares.append(origin + 6)
            if self.rank(origin) - 1 > 0 and self.file(origin) + 2 <= 8:
                possibleDestinationSquares.append(origin + 10)
            if self.rank(origin) - 2 > 0 and self.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin + 15)
            if self.rank(origin) - 2 > 0 and self.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin + 17)
        if pieceType == "B" or pieceType == "Q":
            for distanceNorthwest in range(1, 8):
                if self.rank(origin) + distanceNorthwest <= 8 and self.file(origin) - distanceNorthwest > 0:
                    if self.position[origin - (9 * distanceNorthwest)] == 0:
                        possibleDestinationSquares.append(origin - (9 * distanceNorthwest))
                    elif self.color(self.position[origin - (9 * distanceNorthwest)]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - (9 * distanceNorthwest))
                        break
                    elif self.color(self.position[origin - (9 * distanceNorthwest)]) == pieceColor:
                        break
                else:
                    break
            for distanceNortheast in range(1, 8):
                if self.rank(origin) + distanceNortheast <= 8 and self.file(origin) + distanceNortheast <= 8:
                    if self.position[origin - (7 * distanceNortheast)] == 0:
                        possibleDestinationSquares.append(origin - (7 * distanceNortheast))
                    elif self.color(self.position[origin - (7 * distanceNortheast)]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - (7 * distanceNortheast))
                        break
                    elif self.color(self.position[origin - (7 * distanceNortheast)]) == pieceColor:
                        break
                else:
                    break
            for distanceSoutheast in range(1, 8):
                if self.rank(origin) - distanceSoutheast > 0 and self.file(origin) + distanceSoutheast <= 8:
                    if self.position[origin + (9 * distanceSoutheast)] == 0:
                        possibleDestinationSquares.append(origin + (9 * distanceSoutheast))
                    elif self.color(self.position[origin + (9 * distanceSoutheast)]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + (9 * distanceSoutheast))
                        break
                    elif self.color(self.position[origin + (9 * distanceSoutheast)]) == pieceColor:
                        break
                else:
                    break
            for distanceSouthwest in range(1, 8):
                if self.rank(origin) - distanceSouthwest > 0 and self.file(origin) - distanceSouthwest > 0:
                    if self.position[origin + (7 * distanceSouthwest)] == 0:
                        possibleDestinationSquares.append(origin + (7 * distanceSouthwest))
                    elif self.color(self.position[origin + (7 * distanceSouthwest)]) == self.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + (7 * distanceSouthwest))
                        break
                    elif self.color(self.position[origin + (7 * distanceSouthwest)]) == pieceColor:
                        break
                else:
                    break
        elif pieceType == "K":
            if self.rank(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin - 8)
            if self.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin + 1)
            if self.rank(origin) - 1 > 0:
                possibleDestinationSquares.append(origin + 8)
            if self.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin - 1)
            if self.rank(origin) + 1 <= 8 and self.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin - 9)
            if self.rank(origin) + 1 <= 8 and self.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin - 7)
            if self.rank(origin) - 1 > 0 and self.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin + 9)
            if self.rank(origin) - 1 > 0 and self.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin + 7)

            if not self.inCheck(self.position, self.currentTurn):
                self.castlingPossible = [[False, False], [False, False]]
                if pieceColor == "w":
                    if self.castlingRights[0][0]:
                        if self.position[61] == 0 and self.position[62] == 0:
                            testPosition = copy(self.position)
                            testPosition[origin] = 0
                            testPosition[61] = self.PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not self.inCheck(testPosition, self.currentTurn):
                                possibleDestinationSquares.append(62)
                                self.castlingPossible[0][0] = True
                    if self.castlingRights[0][1]:
                        if self.position[59] == 0 and self.position[58] == 0 and self.position[57] == 0:
                            testPosition = copy(self.position)
                            testPosition[origin] = 0
                            testPosition[59] = self.PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not self.inCheck(testPosition, self.currentTurn):
                                possibleDestinationSquares.append(58)
                                self.castlingPossible[0][1] = True
                elif pieceColor == "b":
                    if self.castlingRights[1][0]:
                        if self.position[5] == 0 and self.position[6] == 0:
                            testPosition = copy(self.position)
                            testPosition[origin] = 0
                            testPosition[5] = self.PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not self.inCheck(testPosition, self.currentTurn):
                                possibleDestinationSquares.append(6)
                                self.castlingPossible[1][0] = True
                    if self.castlingRights[1][1]:
                        if self.position[3] == 0 and self.position[2] == 0 and self.position[1] == 0:
                            testPosition = copy(self.position)
                            testPosition[origin] = 0
                            testPosition[3] = self.PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not self.inCheck(testPosition, self.currentTurn):
                                possibleDestinationSquares.append(2)
                                self.castlingPossible[1][1] = True
        
        legalDestinationSquares = copy(possibleDestinationSquares)
        for destination in possibleDestinationSquares:
            testPosition = copy(self.position)
            selfCaptureAttempt = self.color(testPosition[destination]) == self.currentTurn
            testPosition[origin] = 0
            testPosition[destination] = self.PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
            if self.enPassantOpportunity == destination:
                if pieceColor == "w":
                    testPosition[destination + 8] = 0
                elif pieceColor == "b":
                    testPosition[destination - 8] = 0
            if selfCaptureAttempt or self.inCheck(testPosition, self.currentTurn):
                legalDestinationSquares.pop(legalDestinationSquares.index(destination))
                if self.enPassantOpportunity == destination:
                    self.enPassantOpportunity = -1

        return legalDestinationSquares

    def inCheck(self, testPosition, turn):
        opponentColor = self.oppositeColor(turn)
        kingPosition = testPosition.index(self.PIECE_TYPE_TRANSLATION[("K", turn)])
        
        if turn == "w":
            if self.rank(kingPosition) + 1 <= 8 and self.file(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 9]] == ("P", opponentColor):
                return True
            if self.rank(kingPosition) + 1 <= 8 and self.file(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 7]] == ("P", opponentColor):
                return True
        elif turn == "b":
            if self.rank(kingPosition) - 1 > 0 and self.file(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 9]] == ("P", opponentColor):
                return True
            if self.rank(kingPosition) - 1 > 0 and self.file(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 7]] == ("P", opponentColor):
                return True
        for distanceNorth in range(1, 8):
            if self.rank(kingPosition) + distanceNorth <= 8:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition - (8 * distanceNorth)]] == ("R", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition - (8 * distanceNorth)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - (8 * distanceNorth)] != 0:
                    break
            else:
                break
        for distanceEast in range(1, 8):
            if self.file(kingPosition) + distanceEast <= 8:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition + distanceEast]] == ("R", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition + distanceEast]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + distanceEast] != 0:
                    break
            else:
                break
        for distanceSouth in range(1, 8):
            if self.rank(kingPosition) - distanceSouth > 0:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition + (8 * distanceSouth)]] == ("R", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition + (8 * distanceSouth)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + (8 * distanceSouth)] != 0:
                    break
            else:
                break
        for distanceWest in range(1, 8):
            if self.file(kingPosition) - distanceWest > 0:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition - distanceWest]] == ("R", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition - distanceWest]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - distanceWest] != 0:
                    break
            else:
                break
        for distanceNorthwest in range (1, 8):
            if self.rank(kingPosition) + distanceNorthwest <= 8 and self.file(kingPosition) - distanceNorthwest > 0:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition - (9 * distanceNorthwest)]] == ("B", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition - (9 * distanceNorthwest)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - (9 * distanceNorthwest)] != 0:
                    break
            else:
                break
        for distanceNortheast in range (1, 8):
            if self.rank(kingPosition) + distanceNortheast <= 8 and self.file(kingPosition) + distanceNortheast <= 8:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition - (7 * distanceNortheast)]] == ("B", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition - (7 * distanceNortheast)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - (7 * distanceNortheast)] != 0:
                    break
            else:
                break
        for distanceSoutheast in range (1, 8):
            if self.rank(kingPosition) - distanceSoutheast > 0 and self.file(kingPosition) + distanceSoutheast <= 8:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition + (9 * distanceSoutheast)]] == ("B", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition + (9 * distanceSoutheast)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + (9 * distanceSoutheast)] != 0:
                    break
            else:
                break
        for distanceSouthwest in range (1, 8):
            if self.rank(kingPosition) - distanceSouthwest > 0 and self.file(kingPosition) - distanceSouthwest > 0:
                if self.PIECE_ID_TRANSLATION[testPosition[kingPosition + (7 * distanceSouthwest)]] == ("B", opponentColor) or self.PIECE_ID_TRANSLATION[testPosition[kingPosition + (7 * distanceSouthwest)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + (7 * distanceSouthwest)] != 0:
                    break
            else:
                break

        if self.rank(kingPosition) + 2 <= 8 and self.file(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 17]] == ("N", opponentColor):
            return True
        if self.rank(kingPosition) + 2 <= 8 and self.file(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 15]] == ("N", opponentColor):
            return True
        if self.rank(kingPosition) + 1 <= 8 and self.file(kingPosition) - 2 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 10]] == ("N", opponentColor):
            return True
        if self.rank(kingPosition) + 1 <= 8 and self.file(kingPosition) + 2 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 6]] == ("N", opponentColor):
            return True
        if self.rank(kingPosition) - 1 > 0 and self.file(kingPosition) - 2 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 6]] == ("N", opponentColor):
            return True
        if self.rank(kingPosition) - 1 > 0 and self.file(kingPosition) + 2 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 10]] == ("N", opponentColor):
            return True
        if self.rank(kingPosition) - 2 > 0 and self.file(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 15]] == ("N", opponentColor):
            return True
        if self.rank(kingPosition) - 2 > 0 and self.file(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 17]] == ("N", opponentColor):
            return True

        if self.rank(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 8]] == ("K", opponentColor):
            return True
        if self.file(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 1]] == ("K", opponentColor):
            return True
        if self.rank(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 8]] == ("K", opponentColor):
            return True
        if self.file(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 1]] == ("K", opponentColor):
            return True
        if self.rank(kingPosition) + 1 <= 8 and self.file(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 9]] == ("K", opponentColor):
            return True
        if self.rank(kingPosition) + 1 <= 8 and self.file(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition - 7]] == ("K", opponentColor):
            return True
        if self.rank(kingPosition) - 1 > 0 and self.file(kingPosition) + 1 <= 8 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 9]] == ("K", opponentColor):
            return True
        if self.rank(kingPosition) - 1 > 0 and self.file(kingPosition) - 1 > 0 and self.PIECE_ID_TRANSLATION[testPosition[kingPosition + 7]] == ("K", opponentColor):
            return True
        
        return False

    def color(self, typeId):
        if typeId != 0 and typeId <= 6:
            return "w"
        elif typeId > 6:
            return "b"
        else:
            return ""

    def file(self, location):
        return location % 8 + 1

    def rank(self, location):
        return 8 - math.floor(location / 8)

    def oppositeColor(self, color):
        if color == "w":
            return "b"
        elif color == "b":
            return "w"

    def switchTurn(self):
        self.currentTurn = self.oppositeColor(self.currentTurn)

    def printMoveNumberPhrase(self):
        if self.currentTurn == "w":
            print("Move " + str(self.moveNumber) + ". White to move.")
        elif self.currentTurn == "b":
            print("Move " + str(self.moveNumber) + ". Black to move.")

    def playMove(self, move):
        originCoordinates = move[0] + move[1]
        destinationCoordinates = move[2] + move[3]
        if len(move) == 5:
            promotionType = move[4]
        else:
            promotionType = ""

        origin = self.convertToLocation(originCoordinates)
        destination = self.convertToLocation(destinationCoordinates)
        
        self.movePiece(origin, destination, promotionType)

    def convertToLocation(self, coordinates):
        fileLabels = "abcdefgh"
        rankLabels = "12345678"

        fileIndex = fileLabels.index(coordinates[0])
        rankIndex = rankLabels.index(coordinates[1])

        location = 8 * (7 - rankIndex) + fileIndex
        return location