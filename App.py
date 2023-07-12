import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import math
from copy import copy
from copy import deepcopy
from Agent import Agent
from ChessSim import ChessSim

class Piece:
    def __init__(self, type, color, location, value, sufficiencyValue, image):
        self.type = type
        self.color = color
        self.location = location
        self.value = value
        self.sufficiencyValue = sufficiencyValue
        self.image = image

class Square:
    def __init__(self, complex, color, location):
        self.complex = complex
        self.color = color
        self.location = location

class Chess:
    def __init__(self, computerColor):
        self.root = Tk()

        self.SQUARE_WIDTH = 75

        self.chessBoard = Canvas(self.root, width = 8 * self.SQUARE_WIDTH, height = 8 * self.SQUARE_WIDTH, background = "#FFFFFF")

        self.INITIAL_POSITION = [
            8, 9, 10, 11, 12, 10, 9, 8,
            7, 7, 7, 7, 7, 7, 7, 7,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1,
            2, 3, 4, 5, 6, 4, 3, 2
        ]

        self.DEFAULT_LIGHT_SQUARE_COLOR = "#DDDDDD"
        self.DEFAULT_DARK_SQUARE_COLOR = "#444460"
        
        self.HIGHLIGHTED_LIGHT_SQUARE_COLOR = "#FFFF99"
        self.HIGHLIGHTED_DARK_SQUARE_COLOR = "#88884C"

        self.position = copy(self.INITIAL_POSITION)

        self.legalMoves = []

        self.enPassantOpportunity = -1

        self.castlingRights = [
            [True, True], 
            [True, True]
        ]

        self.castlingPossible = [
            [False, False],
            [False, False]
        ]

        self.currentTurn = "w"
        self.computerColor = computerColor
        self.computerThinking = False

        self.reachedPositions = [[self.INITIAL_POSITION, "w", self.castlingRights, self.enPassantOpportunity]]

        self.moveNumber = 1

        self.promotingPawn = False

        self.squares = self.initializeSquares()
        self.square_ids = []

        self.pieces = self.initializePieces()

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

        self.PIECE_TYPE_TO_IMAGE_TRANSLATION = {
            ("P", "w") : self.pieces[8 - 1].image,
            ("R", "w") : self.pieces[9 - 1].image,
            ("N", "w") : self.pieces[11 - 1].image,
            ("B", "w") : self.pieces[13 - 1].image,
            ("Q", "w") : self.pieces[15 - 1].image,
            ("K", "w") : self.pieces[16 - 1].image,
            ("P", "b") : self.pieces[24 - 1].image,
            ("R", "b") : self.pieces[25 - 1].image,
            ("N", "b") : self.pieces[27 - 1].image,
            ("B", "b") : self.pieces[29 - 1].image,
            ("Q", "b") : self.pieces[31 - 1].image,
            ("K", "b") : self.pieces[32 - 1].image
        }

        self.PIECE_TYPE_TO_VALUE_TRANSLATION = {
            "P" : 1,
            "R" : 5,
            "N" : 3,
            "B" : 3,
            "Q" : 9,
            "K" : 9999
        }

        self.PIECE_ID_TO_VALUE_TRANSLATION = {
            0 : 0,
            1 : 1,
            2 : 5,
            3 : 3,
            4 : 3,
            5 : 9,
            6 : 9999,
            7 : -1,
            8 : -5,
            9 : -3,
            10 : -3,
            11 : -9,
            12 : -9999
        }

        self.PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION = {
            "P" : 100,
            "R" : 100,
            "N" : 50,
            "B" : 50,
            "Q" : 100,
            "K" : 0
        }

        self.pieceIdToNumberTranslation = {
            0: -1
        }

        self.piece_ids = []
        self.idPositions = copy(self.INITIAL_ID_POSITION)

        self.selectedPiece = 0

        self.gameEnded = False
        self.gameResult = 0

        self.agent = Agent(self.computerColor, 3)

    def run(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title("Chess")

        self.chessBoard.grid(column=0, row=0)

        self.printMoveNumberPhrase()

        for piece in range(len(self.pieces)):
            self.piece_ids.append(self.chessBoard.create_image(self.SQUARE_WIDTH * (self.pieces[piece].location % 8), self.SQUARE_WIDTH * math.floor(self.pieces[piece].location / 8), image = self.pieces[piece].image, anchor = "nw"))
            self.pieceIdToNumberTranslation[self.piece_ids[piece]] = piece

        for square in range(len(self.squares)):
            self.square_ids.append(self.chessBoard.create_rectangle(self.SQUARE_WIDTH * (self.squares[square].location % 8), self.SQUARE_WIDTH * math.floor(self.squares[square].location / 8), self.SQUARE_WIDTH * (self.squares[square].location % 8) + self.SQUARE_WIDTH, self.SQUARE_WIDTH * math.floor(self.squares[square].location / 8) + self.SQUARE_WIDTH, fill = self.squares[square].color, outline = self.squares[square].color))
            self.chessBoard.tag_lower(self.square_ids[square])
        
        self.chessBoard.create_rectangle(-800, -800, -730, -500, fill = "#F1F1F1", outline = "#111111", width = 5, tags = ("white_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[32].image, anchor = "nw", tags = ("white_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[33].image, anchor = "nw", tags = ("white_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[34].image, anchor = "nw", tags = ("white_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[35].image, anchor = "nw", tags = ("white_promotion_UI"))
        
        self.chessBoard.create_rectangle(-800, -800, -730, -500, fill = "#F1F1F1", outline = "#111111", width = 5, tags = ("black_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[36].image, anchor = "nw", tags = ("black_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[37].image, anchor = "nw", tags = ("black_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[38].image, anchor = "nw", tags = ("black_promotion_UI"))
        self.chessBoard.create_image(-800, -800, image = self.pieces[39].image, anchor = "nw", tags = ("black_promotion_UI"))

        self.pieceBinds()
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<ButtonRelease>", self.deselect)

        if self.computerColor == "w":
            self.playComputerResponse()
        
        self.root.mainloop()
    
    def playComputerResponse(self):
        self.chessBoard.update()
        self.computerThinking = True
        copyOfSelf = ChessSim(deepcopy(self.position), deepcopy(self.currentTurn), deepcopy(self.castlingRights), deepcopy(self.castlingPossible), deepcopy(self.enPassantOpportunity), deepcopy(self.reachedPositions))
        self.playMove(self.agent.playBestMove(copyOfSelf))
        self.computerThinking = False

    def setSelectedPiece(self, id, computerExecuted):
        if not self.computerThinking or computerExecuted:
            self.selectedPiece = id
            self.chessBoard.tag_raise(self.selectedPiece)

            origin = self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].location
        
            self.legalMoves = self.findLegalMoves(origin, self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].type, self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].color)
        
            self.highlightSquares()

    def drag(self, e):
        if not self.computerThinking:
            self.chessBoard.moveto(self.selectedPiece, e.x - self.SQUARE_WIDTH / 2, e.y - self.SQUARE_WIDTH / 2)

    def deselect(self, e):
        self.movePiece(e.x, e.y, "")

    def movePiece(self, x, y, promotionType):
        self.unhighlightSquares()
        capture = False
        origin = self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].location

        if not self.promotingPawn and not self.gameEnded and self.selectedPiece != 0:
            destination = math.floor(y / self.SQUARE_WIDTH) * 8 + math.floor(x / self.SQUARE_WIDTH)
            if destination >= 0 and destination < 64 and self.legalMoves.count(destination) != 0:
                self.chessBoard.moveto(self.selectedPiece, self.SQUARE_WIDTH * (destination % 8), self.SQUARE_WIDTH * math.floor(destination / 8))
                self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].location = destination
                if self.position[destination] != 0:
                    self.chessBoard.moveto(self.idPositions[destination], -200, -200)
                self.position[origin] = 0
                if self.position[destination] != 0:
                    capture = True
                self.position[destination] = self.PIECE_TYPE_TRANSLATION[(self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].type, self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].color)]
                self.idPositions[origin] = 0
                self.idPositions[destination] = self.selectedPiece

                self.castling(destination)
                
                self.pawnPromotion(destination)
                if promotionType != "":
                    self.promoteTo(promotionType, self.currentTurn)
                
                self.enPassant(self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].type, self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].color, destination)
                if self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].type == "P" and abs(origin - destination) == 16:
                    self.enPassantOpportunity = math.floor((origin + destination) / 2)
                else:
                    self.enPassantOpportunity = -1
                
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
                            
                if self.currentTurn == "w":
                    self.moveNumber += 1

                if not self.promotingPawn:
                    if self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].type == "P" or capture:
                        self.reachedPositions.clear()
                    self.reachedPositions.append([copy(self.position), copy(self.currentTurn), copy(self.castlingRights), copy(self.enPassantOpportunity)])
                    self.gameEndLogic()
                    if not self.gameEnded:
                        self.printMoveNumberPhrase()
                        if self.currentTurn == self.computerColor:
                            self.playComputerResponse()

            else:
                self.chessBoard.moveto(self.selectedPiece, self.SQUARE_WIDTH * (origin % 8), self.SQUARE_WIDTH * math.floor(origin / 8))
        else:
            self.chessBoard.moveto(self.selectedPiece, self.SQUARE_WIDTH * (origin % 8), self.SQUARE_WIDTH * math.floor(origin / 8))
        self.selectedPiece = 0

    def castling(self, destination):
        if self.castlingPossible[0][0] and destination == 62:
            self.position[63] = 0
            self.position[61] = self.PIECE_TYPE_TRANSLATION[("R", "w")]
            self.idPositions[63] = 0
            self.idPositions[61] = 10
            self.chessBoard.moveto(10, self.SQUARE_WIDTH * (61 % 8), self.SQUARE_WIDTH * math.floor(61 / 8))
            self.pieces[10 - 1].location = 61
            self.castlingRights[0] = [False, False]
        elif self.castlingPossible[0][1] and destination == 58:
            self.position[56] = 0
            self.position[59] = self.PIECE_TYPE_TRANSLATION[("R", "w")]
            self.idPositions[56] = 0
            self.idPositions[59] = 9
            self.chessBoard.moveto(9, self.SQUARE_WIDTH * (59 % 8), self.SQUARE_WIDTH * math.floor(59 / 8))
            self.pieces[9 - 1].location = 59
            self.castlingRights[0] = [False, False]
        elif self.castlingPossible[1][0] and destination == 6:
            self.position[7] = 0
            self.position[5] = self.PIECE_TYPE_TRANSLATION[("R", "b")]
            self.idPositions[7] = 0
            self.idPositions[5] = 26
            self.chessBoard.moveto(26, self.SQUARE_WIDTH * (5 % 8), self.SQUARE_WIDTH * math.floor(5 / 8))
            self.pieces[26 - 1].location = 5
            self.castlingRights[1] = [False, False]
        elif self.castlingPossible[1][1] and destination == 2:
            self.position[0] = 0
            self.position[3] = self.PIECE_TYPE_TRANSLATION[("R", "b")]
            self.idPositions[0] = 0
            self.idPositions[3] = 25
            self.chessBoard.moveto(25, self.SQUARE_WIDTH * (3 % 8), self.SQUARE_WIDTH * math.floor(3 / 8))
            self.pieces[25 - 1].location = 3
            self.castlingRights[1] = [False, False]
            
        if self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].type == "K":
            if self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].color == "w":
                self.castlingRights[0] = [False, False]
            elif self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].color == "b":
                self.castlingRights[1] = [False, False]

        if self.position[63] != self.PIECE_TYPE_TRANSLATION[("R", "w")]:
            self.castlingRights[0][0] = False
        if self.position[56] != self.PIECE_TYPE_TRANSLATION[("R", "w")]:
            self.castlingRights[0][1] = False
        if self.position[7] != self.PIECE_TYPE_TRANSLATION[("R", "b")]:
            self.castlingRights[1][0] = False
        if self.position[0] != self.PIECE_TYPE_TRANSLATION[("R", "b")]:
            self.castlingRights[1][1] = False

    def pawnPromotion(self, destination):
        baseX = self.SQUARE_WIDTH * (destination % 8)
        baseY = self.SQUARE_WIDTH * math.floor(destination / 8)
        offsetXWhite = [0, 0, 0, 0, 0]
        offsetYWhite = [75, 75, 150, 225, 300]
        offsetXBlack = [0, 0, 0, 0, 0]
        offsetYBlack = [-305, -77, -152, -227, -302]
        if self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].type == "P" and not self.currentTurn == self.computerColor:
            if self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].color == "w" and destination < 8:
                self.promotingPawn = True
                for id in self.chessBoard.find_withtag("white_promotion_UI"):
                    self.chessBoard.moveto(id, baseX + offsetXWhite[id - 105], baseY + offsetYWhite[id - 105])
                    self.chessBoard.tag_raise(id)
            elif self.pieces[self.pieceIdToNumberTranslation[self.selectedPiece]].color == "b" and destination >= 56:
                self.promotingPawn = True
                for id in self.chessBoard.find_withtag("black_promotion_UI"):
                    self.chessBoard.moveto(id, baseX + offsetXBlack[id - 110], baseY + offsetYBlack[id - 110])
                    self.chessBoard.tag_raise(id)

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
        
        self.chessBoard.moveto(self.idPositions[promotionLocation], -200, -200)
        promotedPieceId = self.chessBoard.create_image(self.SQUARE_WIDTH * (promotionLocation % 8), self.SQUARE_WIDTH * math.floor(promotionLocation / 8), image = self.PIECE_TYPE_TO_IMAGE_TRANSLATION[(pieceType, pieceColor)], anchor = "nw")
        self.pieces.append(Piece(pieceType, pieceColor, promotionLocation, self.PIECE_TYPE_TO_VALUE_TRANSLATION[pieceType], self.PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION[pieceType], self.PIECE_TYPE_TO_IMAGE_TRANSLATION[(pieceType, pieceColor)]))
        self.chessBoard.tag_bind(promotedPieceId, "<Button-1>", lambda x: self.setSelectedPiece(promotedPieceId, False))

        self.position[promotionLocation] = self.PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
        self.idPositions[promotionLocation] = promotedPieceId
        self.pieceIdToNumberTranslation[promotedPieceId] = len(self.pieces) - 1

        if pieceColor == "w":
            for id in self.chessBoard.find_withtag("white_promotion_UI"):
                self.chessBoard.moveto(id, -800, -800)
        elif pieceColor == "b":
            for id in self.chessBoard.find_withtag("black_promotion_UI"):
                self.chessBoard.moveto(id, -800, -800)

        self.reachedPositions.clear()
        self.reachedPositions.append([copy(self.position), copy(self.currentTurn), copy(self.castlingRights), copy(self.enPassantOpportunity)])
        self.gameEndLogic()
        if not self.gameEnded:
            self.printMoveNumberPhrase()
            if self.currentTurn == self.computerColor and self.promotingPawn:
                self.promotingPawn = False
                self.playComputerResponse()
        
        self.promotingPawn = False

    def enPassant(self, pieceType, pieceColor, destination):
        if pieceType == "P" and self.enPassantOpportunity == destination:
            if pieceColor == "w":
                self.chessBoard.moveto(self.idPositions[destination + 8], -200, -200)
                self.position[destination + 8] = 0
                self.idPositions[destination + 8] = 0
            elif pieceColor == "b":
                self.chessBoard.moveto(self.idPositions[destination - 8], -200, 200)
                self.position[destination - 8] = 0
                self.idPositions[destination - 8] = 0

    def gameEndLogic(self):
        movablePieces = False
        for location in range(len(self.position)):
            if self.color(self.position[location]) == self.currentTurn:
                if len(self.findLegalMoves(location, self.pieces[self.pieceIdToNumberTranslation[self.idPositions[location]]].type, self.currentTurn)) != 0:
                    movablePieces = True
                    break
        if self.inCheck(self.position, self.currentTurn) and not movablePieces:
            if self.currentTurn == "w":
                print("Black wins by checkmate.")
                self.gameEnded = True
                self.gameResult = -1
                pass
            elif self.currentTurn == "b":
                print("White wins by checkmate.")
                self.gameEnded = True
                self.gameResult = 1
                pass
        elif not movablePieces:
            print("The game is a draw by stalemate.")
            self.gameEnded = True
            pass
        
        if len(self.reachedPositions) > 100:
            print("The game is a draw by the 50-move rule.")
            self.gameEnded = True
            pass

        repetitionCounter = 0
        for absolutePosition in self.reachedPositions:
            if absolutePosition == self.reachedPositions[len(self.reachedPositions) - 1]:
                repetitionCounter += 1
                if repetitionCounter == 3:
                    print("The game is a draw by threefold repetition.")
                    self.gameEnded = True
                    pass
        
        totalSufficiencyMaterial = 0
        bishopColors = ["", ""]
        for location in range(len(self.idPositions)):
            if self.idPositions[location] != 0:
                if self.pieces[self.pieceIdToNumberTranslation[self.idPositions[location]]].type == "B":
                    if bishopColors == ["", ""]:
                        totalSufficiencyMaterial += self.pieces[self.pieceIdToNumberTranslation[self.idPositions[location]]].sufficiencyValue
                    if (location % 2 + math.floor(location / 8)) % 2 == 0:
                        bishopColors[0] = "l"
                    else:
                        bishopColors[1] = "d"
                    if bishopColors == ["l", "d"]:
                        totalSufficiencyMaterial += self.pieces[self.pieceIdToNumberTranslation[self.idPositions[location]]].sufficiencyValue
                else:
                    totalSufficiencyMaterial += self.pieces[self.pieceIdToNumberTranslation[self.idPositions[location]]].sufficiencyValue
                
                if totalSufficiencyMaterial >= 100:
                    break
        if totalSufficiencyMaterial < 100:
            print("The game is a draw by insufficient material.")
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
                if self.rank(origin) + distanceNorthwest <= 8 and self.file( origin) - distanceNorthwest > 0:
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

    def initializeSquares(self):
        squares = []
        for location in range(64):
            if (location % 2 + math.floor(location / 8)) % 2 == 0:
                complex = "l"
                color = self.DEFAULT_LIGHT_SQUARE_COLOR
            else:
                complex = "d"
                color = self.DEFAULT_DARK_SQUARE_COLOR
            squares.append(Square(complex, color, location))
        return squares

    def highlightSquares(self):
        for square in self.squares:
            if self.legalMoves.count(square.location) != 0:
                if square.complex == "l":
                    square.color = self.HIGHLIGHTED_LIGHT_SQUARE_COLOR
                elif square.complex == "d":
                    square.color = self.HIGHLIGHTED_DARK_SQUARE_COLOR
                self.chessBoard.itemconfig(self.square_ids[square.location], fill = square.color, outline = square.color)

    def unhighlightSquares(self):
        for square in self.squares:
            if self.legalMoves.count(square.location) != 0:
                if square.complex == "l":
                    square.color = self.DEFAULT_LIGHT_SQUARE_COLOR
                elif square.complex == "d":
                    square.color = self.DEFAULT_DARK_SQUARE_COLOR
                self.chessBoard.itemconfig(self.square_ids[square.location], fill = square.color, outline = square.color)

    def initializePieces(self):
        pieces = [
            Piece("P", "w", 48, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("P", "w", 49, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("P", "w", 50, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("P", "w", 51, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("P", "w", 52, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("P", "w", 53, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("P", "w", 54, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("P", "w", 55, 1, 100, PhotoImage(file = 'Sprites/White_Pawn.png')),
            Piece("R", "w", 56, 5, 100, PhotoImage(file = 'Sprites/White_Rook.png')),
            Piece("R", "w", 63, 5, 100, PhotoImage(file = 'Sprites/White_Rook.png')),
            Piece("N", "w", 57, 3, 50, PhotoImage(file = 'Sprites/White_Knight.png')),
            Piece("N", "w", 62, 3, 50, PhotoImage(file = 'Sprites/White_Knight.png')),
            Piece("B", "w", 58, 3, 50, PhotoImage(file = 'Sprites/White_Bishop.png')),
            Piece("B", "w", 61, 3, 50, PhotoImage(file = 'Sprites/White_Bishop.png')),
            Piece("Q", "w", 59, 9, 100, PhotoImage(file = 'Sprites/White_Queen.png')),
            Piece("K", "w", 60, 9999, 0, PhotoImage(file = 'Sprites/White_King.png')),
            Piece("P", "b", 8, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("P", "b", 9, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("P", "b", 10, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("P", "b", 11, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("P", "b", 12, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("P", "b", 13, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("P", "b", 14, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("P", "b", 15, 1, 100, PhotoImage(file = 'Sprites/Black_Pawn.png')),
            Piece("R", "b", 0, 5, 100, PhotoImage(file = 'Sprites/Black_Rook.png')),
            Piece("R", "b", 7, 5, 100, PhotoImage(file = 'Sprites/Black_Rook.png')),
            Piece("N", "b", 1, 3, 50, PhotoImage(file = 'Sprites/Black_Knight.png')),
            Piece("N", "b", 6, 3, 50, PhotoImage(file = 'Sprites/Black_Knight.png')),
            Piece("B", "b", 2, 3, 50, PhotoImage(file = 'Sprites/Black_Bishop.png')),
            Piece("B", "b", 5, 3, 50, PhotoImage(file = 'Sprites/Black_Bishop.png')),
            Piece("Q", "b", 3, 9, 100, PhotoImage(file = 'Sprites/Black_Queen.png')),
            Piece("K", "b", 4, 9999, 0, PhotoImage(file = 'Sprites/Black_King.png')),

            Piece("Q", "wp", -100, 0, 0, PhotoImage(file = 'Sprites/White_Queen.png')),
            Piece("N", "wp", -100, 0, 0, PhotoImage(file = 'Sprites/White_Knight.png')),
            Piece("R", "wp", -100, 0, 0, PhotoImage(file = 'Sprites/White_Rook.png')),
            Piece("B", "wp", -100, 0, 0, PhotoImage(file = 'Sprites/White_Bishop.png')),
            Piece("Q", "bp", -100, 0, 0, PhotoImage(file = 'Sprites/Black_Queen.png')),
            Piece("N", "bp", -100, 0, 0, PhotoImage(file = 'Sprites/Black_Knight.png')),
            Piece("R", "bp", -100, 0, 0, PhotoImage(file = 'Sprites/Black_Rook.png')),
            Piece("B", "bp", -100, 0, 0, PhotoImage(file = 'Sprites/Black_Bishop.png'))
        ]
        return pieces

    def pieceBinds(self):
        self.chessBoard.tag_bind(1, "<Button-1>", lambda x: self.setSelectedPiece(1, False))
        self.chessBoard.tag_bind(2, "<Button-1>", lambda x: self.setSelectedPiece(2, False))
        self.chessBoard.tag_bind(3, "<Button-1>", lambda x: self.setSelectedPiece(3, False))
        self.chessBoard.tag_bind(4, "<Button-1>", lambda x: self.setSelectedPiece(4, False))
        self.chessBoard.tag_bind(5, "<Button-1>", lambda x: self.setSelectedPiece(5, False))
        self.chessBoard.tag_bind(6, "<Button-1>", lambda x: self.setSelectedPiece(6, False))
        self.chessBoard.tag_bind(7, "<Button-1>", lambda x: self.setSelectedPiece(7, False))
        self.chessBoard.tag_bind(8, "<Button-1>", lambda x: self.setSelectedPiece(8, False))
        self.chessBoard.tag_bind(9, "<Button-1>", lambda x: self.setSelectedPiece(9, False))
        self.chessBoard.tag_bind(10, "<Button-1>", lambda x: self.setSelectedPiece(10, False))
        self.chessBoard.tag_bind(11, "<Button-1>", lambda x: self.setSelectedPiece(11, False))
        self.chessBoard.tag_bind(12, "<Button-1>", lambda x: self.setSelectedPiece(12, False))
        self.chessBoard.tag_bind(13, "<Button-1>", lambda x: self.setSelectedPiece(13, False))
        self.chessBoard.tag_bind(14, "<Button-1>", lambda x: self.setSelectedPiece(14, False))
        self.chessBoard.tag_bind(15, "<Button-1>", lambda x: self.setSelectedPiece(15, False))
        self.chessBoard.tag_bind(16, "<Button-1>", lambda x: self.setSelectedPiece(16, False))
        self.chessBoard.tag_bind(17, "<Button-1>", lambda x: self.setSelectedPiece(17, False))
        self.chessBoard.tag_bind(18, "<Button-1>", lambda x: self.setSelectedPiece(18, False))
        self.chessBoard.tag_bind(19, "<Button-1>", lambda x: self.setSelectedPiece(19, False))
        self.chessBoard.tag_bind(20, "<Button-1>", lambda x: self.setSelectedPiece(20, False))
        self.chessBoard.tag_bind(21, "<Button-1>", lambda x: self.setSelectedPiece(21, False))
        self.chessBoard.tag_bind(22, "<Button-1>", lambda x: self.setSelectedPiece(22, False))
        self.chessBoard.tag_bind(23, "<Button-1>", lambda x: self.setSelectedPiece(23, False))
        self.chessBoard.tag_bind(24, "<Button-1>", lambda x: self.setSelectedPiece(24, False))
        self.chessBoard.tag_bind(25, "<Button-1>", lambda x: self.setSelectedPiece(25, False))
        self.chessBoard.tag_bind(26, "<Button-1>", lambda x: self.setSelectedPiece(26, False))
        self.chessBoard.tag_bind(27, "<Button-1>", lambda x: self.setSelectedPiece(27, False))
        self.chessBoard.tag_bind(28, "<Button-1>", lambda x: self.setSelectedPiece(28, False))
        self.chessBoard.tag_bind(29, "<Button-1>", lambda x: self.setSelectedPiece(29, False))
        self.chessBoard.tag_bind(30, "<Button-1>", lambda x: self.setSelectedPiece(30, False))
        self.chessBoard.tag_bind(31, "<Button-1>", lambda x: self.setSelectedPiece(31, False))
        self.chessBoard.tag_bind(32, "<Button-1>", lambda x: self.setSelectedPiece(32, False))

        self.chessBoard.tag_bind(106, "<Button-1>", lambda x: self.promoteTo("Q", "w"))
        self.chessBoard.tag_bind(107, "<Button-1>", lambda x: self.promoteTo("N", "w"))
        self.chessBoard.tag_bind(108, "<Button-1>", lambda x: self.promoteTo("R", "w"))
        self.chessBoard.tag_bind(109, "<Button-1>", lambda x: self.promoteTo("B", "w"))
        self.chessBoard.tag_bind(111, "<Button-1>", lambda x: self.promoteTo("Q", "b"))
        self.chessBoard.tag_bind(112, "<Button-1>", lambda x: self.promoteTo("N", "b"))
        self.chessBoard.tag_bind(113, "<Button-1>", lambda x: self.promoteTo("R", "b"))
        self.chessBoard.tag_bind(114, "<Button-1>", lambda x: self.promoteTo("B", "b"))

    def playMove(self, move):
        print(move)
        originCoordinates = move[0] + move[1]
        destinationCoordinates = move[2] + move[3]
        if len(move) == 5:
            promotionType = move[4]
        else:
            promotionType = ""

        origin = self.convertToLocation(originCoordinates)
        destination = self.convertToLocation(destinationCoordinates)

        x = self.SQUARE_WIDTH * (destination % 8) + self.SQUARE_WIDTH / 2
        y = self.SQUARE_WIDTH * math.floor(destination / 8) + self.SQUARE_WIDTH / 2
        
        self.setSelectedPiece(self.idPositions[origin], True)
        self.movePiece(x, y, promotionType)

    def convertToLocation(self, coordinates):
        fileLabels = "abcdefgh"
        rankLabels = "12345678"

        fileIndex = fileLabels.index(coordinates[0])
        rankIndex = rankLabels.index(coordinates[1])

        location = 8 * (7 - rankIndex) + fileIndex
        return location
    
game = Chess("w")
game.run()