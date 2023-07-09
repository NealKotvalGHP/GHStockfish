import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import math
from copy import copy
from Board import Board
from Agent import Agent


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
    def __init__(self, root, chessBoard, SQUARE_WIDTH, INITIAL_POSITION, DEFAULT_LIGHT_SQUARE_COLOR, DEFAULT_DARK_SQUARE_COLOR, 
                 HIGHLIGHTED_LIGHT_SQUARE_COLOR, HIGHLIGHTED_DARK_SQUARE_COLOR, currentTurn, position, legalMoves, enPassantOpportunity, 
                 castlingRights, reachedPositions, moveNumber, promotingPawn, squares, square_ids, pieces, piece_ids, INITIAL_ID_POSITION,
                 PIECE_TYPE_TRANSLATION, PIECE_ID_TRANSLATION, PIECE_TYPE_TO_IMAGE_TRANSLATION, PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION,
                 pieceIdToNumberTranslation, idPositions, selectedPiece, gameEnded):
        self.root = root
        self.chessBoard = chessBoard
        self.SQUARE_WIDTH = SQUARE_WIDTH
        self.INITIAL_POSITION = INITIAL_POSITION
        self.DEFAULT_LIGHT_SQUARE_COLOR = DEFAULT_LIGHT_SQUARE_COLOR
        self.DEFAULT_DARK_SQUARE_COLOR = DEFAULT_DARK_SQUARE_COLOR
        self.HIGHLIGHTED_LIGHT_SQUARE_COLOR = HIGHLIGHTED_LIGHT_SQUARE_COLOR
        self.HIGHLIGHTED_DARK_SQUARE_COLOR = HIGHLIGHTED_DARK_SQUARE_COLOR
        self.currentTurn = currentTurn
        self.position = position
        self.legalMoves = legalMoves
        self.enPassantOpportunity = enPassantOpportunity
        self.castlingRights = castlingRights
        self.reachedPositions = reachedPositions
        self.moveNumber = moveNumber
        self.promotingPawn = promotingPawn
        self.squares = squares
        self.square_ids = square_ids
        self.pieces = pieces
        self.piece_ids = piece_ids
        self.INITIAL_ID_POSITION = INITIAL_ID_POSITION
        self.PIECE_TYPE_TRANSLATION = PIECE_TYPE_TRANSLATION
        self.PIECE_ID_TRANSLATION = PIECE_ID_TRANSLATION
        self.PIECE_TYPE_TO_IMAGE_TRANSLATION = PIECE_TYPE_TO_IMAGE_TRANSLATION
        self.PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION = PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION
        self.pieceIdToNumberTranslation = pieceIdToNumberTranslation
        self.idPositions = idPositions
        self.selectedPiece = selectedPiece
        self.gameEnded = gameEnded

    def game(self):
        global root
        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.title("Chess")

        global SQUARE_WIDTH
        SQUARE_WIDTH = 75

        global chessBoard 
        chessBoard = Canvas(root, width = 8 * SQUARE_WIDTH, height = 8 * SQUARE_WIDTH, background = "#FFFFFF")
        chessBoard.grid(column=0, row=0)

        INITIAL_POSITION = [
            8, 9, 10, 11, 12, 10, 9, 8,
            7, 7, 7, 7, 7, 7, 7, 7,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1,
            2, 3, 4, 5, 6, 4, 3, 2
        ]

        global DEFAULT_DARK_SQUARE_COLOR
        DEFAULT_DARK_SQUARE_COLOR = "#444460"

        global DEFAULT_LIGHT_SQUARE_COLOR
        DEFAULT_LIGHT_SQUARE_COLOR = "#DDDDDD"

        global HIGHLIGHTED_DARK_SQUARE_COLOR
        HIGHLIGHTED_DARK_SQUARE_COLOR = "#55554C"

        global HIGHLIGHTED_LIGHT_SQUARE_COLOR
        HIGHLIGHTED_LIGHT_SQUARE_COLOR = "#FFFFCC"

        global position
        position = copy(INITIAL_POSITION)

        global legalMoves
        legalMoves = []

        global enPassantOpportunity
        enPassantOpportunity = -1

        global currentTurn
        currentTurn = "w"

        global castlingRights
        castlingRights = [
            [True, True], 
            [True, True]
        ]

        global reachedPositions
        reachedPositions = [[INITIAL_POSITION, "w", castlingRights, enPassantOpportunity]]

        global moveNumber
        moveNumber = 1
        Chess.printMoveNumberPhrase(currentTurn)

        global promotingPawn
        promotingPawn = False

        global squares
        squares = Chess.initializeSquares()
        global square_ids
        square_ids = []

        global pieces
        pieces = Chess.initializePieces()

        INITIAL_ID_POSITION = [
            25, 27, 29, 31, 32, 30, 28, 26,
            17, 18, 19, 20, 21, 22, 23, 24,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            1, 2, 3, 4, 5, 6, 7, 8,
            9, 11, 13, 15, 16, 14, 12, 10
        ]

        global PIECE_TYPE_TRANSLATION
        PIECE_TYPE_TRANSLATION = {
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

        global PIECE_ID_TRANSLATION
        PIECE_ID_TRANSLATION = {
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

        global PIECE_TYPE_TO_IMAGE_TRANSLATION
        PIECE_TYPE_TO_IMAGE_TRANSLATION = {
            ("P", "w") : pieces[8 - 1].image,
            ("R", "w") : pieces[9 - 1].image,
            ("N", "w") : pieces[11 - 1].image,
            ("B", "w") : pieces[13 - 1].image,
            ("Q", "w") : pieces[15 - 1].image,
            ("K", "w") : pieces[16 - 1].image,
            ("P", "b") : pieces[24 - 1].image,
            ("R", "b") : pieces[25 - 1].image,
            ("N", "b") : pieces[27 - 1].image,
            ("B", "b") : pieces[29 - 1].image,
            ("Q", "b") : pieces[31 - 1].image,
            ("K", "b") : pieces[32 - 1].image
        }

        global PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION
        PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION = {
            ("P", "w") : 100,
            ("R", "w") : 100,
            ("N", "w") : 50,
            ("B", "w") : 50,
            ("Q", "w") : 100,
            ("K", "w") : 0,
            ("P", "b") : 100,
            ("R", "b") : 100,
            ("N", "b") : 50,
            ("B", "b") : 50,
            ("Q", "b") : 100,
            ("K", "b") : 0
        }

        global pieceIdToNumberTranslation
        pieceIdToNumberTranslation = {
            0: -1
        }

        global piece_ids
        piece_ids = []
        global idPositions
        idPositions = INITIAL_ID_POSITION

        global selectedPiece
        selectedPiece = 0

        global gameEnded
        gameEnded = False

        for piece in range(len(pieces)):
            piece_ids.append(chessBoard.create_image(SQUARE_WIDTH * (pieces[piece].location % 8), SQUARE_WIDTH * math.floor(pieces[piece].location / 8), image = pieces[piece].image, anchor = "nw"))
            pieceIdToNumberTranslation[piece_ids[piece]] = piece

        for square in range(len(squares)):
            square_ids.append(chessBoard.create_rectangle(SQUARE_WIDTH * (squares[square].location % 8), SQUARE_WIDTH * math.floor(squares[square].location / 8), SQUARE_WIDTH * (squares[square].location % 8) + SQUARE_WIDTH, SQUARE_WIDTH * math.floor(squares[square].location / 8) + SQUARE_WIDTH, fill = squares[square].color, outline = squares[square].color))
            chessBoard.tag_lower(square_ids[square])


        chessBoard.create_rectangle(-800, -800, -730, -500, fill = "#F1F1F1", outline = "#111111", width = 5, tags = ("white_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[32].image, anchor = "nw", tags = ("white_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[33].image, anchor = "nw", tags = ("white_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[34].image, anchor = "nw", tags = ("white_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[35].image, anchor = "nw", tags = ("white_promotion_UI"))
        
        chessBoard.create_rectangle(-800, -800, -730, -500, fill = "#F1F1F1", outline = "#111111", width = 5, tags = ("black_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[36].image, anchor = "nw", tags = ("black_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[37].image, anchor = "nw", tags = ("black_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[38].image, anchor = "nw", tags = ("black_promotion_UI"))
        chessBoard.create_image(-800, -800, image = pieces[39].image, anchor = "nw", tags = ("black_promotion_UI"))

        Chess.pieceBinds()
        root.bind("<B1-Motion>", Chess.drag)
        root.bind("<ButtonRelease>", Chess.deselect)

        # This is where you would input a move to play. Player still has to choose
        # which piece to promote to when promoting.
        # playMove("e2e4")
        # playMove("e7e5")

        root.mainloop()

    def setSelectedPiece(self, id):
        global selectedPiece
        selectedPiece = id
        chessBoard.tag_raise(selectedPiece)

        origin = pieces[pieceIdToNumberTranslation[selectedPiece]].location
        
        global legalMoves
        legalMoves = Chess.findLegalMoves(origin, pieces[pieceIdToNumberTranslation[selectedPiece]].type, pieces[pieceIdToNumberTranslation[selectedPiece]].color, position)
        
        Chess.highlightSquares(legalMoves)

    def drag(self, e):
        chessBoard.moveto(selectedPiece, e.x - SQUARE_WIDTH / 2, e.y - SQUARE_WIDTH / 2)

    def deselect(self, e):
        Chess.movePiece(e.x, e.y)

    def movePiece(self, x, y):
        Chess.unhighlightSquares(legalMoves)
        global selectedPiece
        global enPassantOpportunity
        global reachedPositions
        global castlingRights
        global gameEnded
        global moveNumber
        capture = False
        origin = pieces[pieceIdToNumberTranslation[selectedPiece]].location

        if not promotingPawn and not gameEnded:
            destination = math.floor(y / SQUARE_WIDTH) * 8 + math.floor(x / SQUARE_WIDTH)
            if destination >= 0 and destination < 64 and legalMoves.count(destination) != 0:
                chessBoard.moveto(selectedPiece, SQUARE_WIDTH * (destination % 8), SQUARE_WIDTH * math.floor(destination / 8))
                pieces[pieceIdToNumberTranslation[selectedPiece]].location = destination
                if position[destination] != 0:
                    chessBoard.moveto(idPositions[destination], -200, -200)
                position[origin] = 0
                if position[destination] != 0:
                    capture = True
                position[destination] = PIECE_TYPE_TRANSLATION[(pieces[pieceIdToNumberTranslation[selectedPiece]].type, pieces[pieceIdToNumberTranslation[selectedPiece]].color)]
                idPositions[origin] = 0
                idPositions[destination] = selectedPiece

                Chess.castling(destination)
                
                Chess.pawnPromotion(destination)
                
                Chess.enPassant(pieces[pieceIdToNumberTranslation[selectedPiece]].type, pieces[pieceIdToNumberTranslation[selectedPiece]].color, destination)
                if pieces[pieceIdToNumberTranslation[selectedPiece]].type == "P" and abs(origin - destination) == 16:
                    enPassantOpportunity = math.floor((origin + destination) / 2)
                else:
                    enPassantOpportunity = -1
                
                Chess.switchTurn()

                for location in range(len(position)):
                    if PIECE_ID_TRANSLATION[position[location]] == ("P", currentTurn):
                        if Chess.findLegalMoves(location, "P", currentTurn, position).count(enPassantOpportunity) == 0:
                            enPassantOpportunity = -1
                        else:
                            enPassantOpportunity = math.floor((origin + destination) / 2)
                            break

                if currentTurn == "w":
                    moveNumber += 1

                if not promotingPawn:
                    if pieces[pieceIdToNumberTranslation[selectedPiece]].type == "P" or capture:
                        reachedPositions.clear()
                    reachedPositions.append([copy(position), copy(currentTurn), copy(castlingRights), copy(enPassantOpportunity)])
                    Chess.gameEndLogic()
                    if not gameEnded:
                        Chess.printMoveNumberPhrase(currentTurn)
            else:
                chessBoard.moveto(selectedPiece, SQUARE_WIDTH * (origin % 8), SQUARE_WIDTH * math.floor(origin / 8))
        else:
            chessBoard.moveto(selectedPiece, SQUARE_WIDTH * (origin % 8), SQUARE_WIDTH * math.floor(origin / 8))
        selectedPiece = 0

    def castling(self, destination):
        global reachedPositions
        if castlingPossible[0][0] and destination == 62:
            position[63] = 0
            position[61] = PIECE_TYPE_TRANSLATION[("R", "w")]
            idPositions[63] = 0
            idPositions[61] = 10
            chessBoard.moveto(10, SQUARE_WIDTH * (61 % 8), SQUARE_WIDTH * math.floor(61 / 8))
            pieces[10 - 1].location = 61
            castlingRights[0] = [False, False]
        elif castlingPossible[0][1] and destination == 58:
            position[56] = 0
            position[59] = PIECE_TYPE_TRANSLATION[("R", "w")]
            idPositions[56] = 0
            idPositions[59] = 9
            chessBoard.moveto(9, SQUARE_WIDTH * (59 % 8), SQUARE_WIDTH * math.floor(59 / 8))
            pieces[9 - 1].location = 59
            castlingRights[0] = [False, False]
        elif castlingPossible[1][0] and destination == 6:
            position[7] = 0
            position[5] = PIECE_TYPE_TRANSLATION[("R", "b")]
            idPositions[7] = 0
            idPositions[5] = 26
            chessBoard.moveto(26, SQUARE_WIDTH * (5 % 8), SQUARE_WIDTH * math.floor(5 / 8))
            pieces[26 - 1].location = 5
            castlingRights[1] = [False, False]
        elif castlingPossible[1][1] and destination == 2:
            position[0] = 0
            position[3] = PIECE_TYPE_TRANSLATION[("R", "b")]
            idPositions[0] = 0
            idPositions[3] = 25
            chessBoard.moveto(25, SQUARE_WIDTH * (3 % 8), SQUARE_WIDTH * math.floor(3 / 8))
            pieces[25 - 1].location = 3
            castlingRights[1] = [False, False]
            
        if pieces[pieceIdToNumberTranslation[selectedPiece]].type == "K":
            if pieces[pieceIdToNumberTranslation[selectedPiece]].color == "w":
                castlingRights[0] = [False, False]
            elif pieces[pieceIdToNumberTranslation[selectedPiece]].color == "b":
                castlingRights[1] = [False, False]
            
        if position[63] != PIECE_TYPE_TRANSLATION[("R", "w")]:
            castlingRights[0][0] = False
        if position[56] != PIECE_TYPE_TRANSLATION[("R", "w")]:
            castlingRights[0][1] = False
        if position[7] != PIECE_TYPE_TRANSLATION[("R", "b")]:
            castlingRights[1][0] = False
        if position[0] != PIECE_TYPE_TRANSLATION[("R", "b")]:
            castlingRights[1][1] = False

    def pawnPromotion(self, destination):
        global promotingPawn
        baseX = SQUARE_WIDTH * (destination % 8)
        baseY = SQUARE_WIDTH * math.floor(destination / 8)
        offsetXWhite = [0, 0, 0, 0, 0]
        offsetYWhite = [75, 75, 150, 225, 300]
        offsetXBlack = [0, 0, 0, 0, 0]
        offsetYBlack = [-305, -77, -152, -227, -302]
        if pieces[pieceIdToNumberTranslation[selectedPiece]].type == "P":
            if pieces[pieceIdToNumberTranslation[selectedPiece]].color == "w" and destination < 8:
                promotingPawn = True
                for id in chessBoard.find_withtag("white_promotion_UI"):
                    chessBoard.moveto(id, baseX + offsetXWhite[id - 105], baseY + offsetYWhite[id - 105])
                    chessBoard.tag_raise(id)
            elif pieces[pieceIdToNumberTranslation[selectedPiece]].color == "b" and destination >= 56:
                promotingPawn = True
                for id in chessBoard.find_withtag("black_promotion_UI"):
                    chessBoard.moveto(id, baseX + offsetXBlack[id - 110], baseY + offsetYBlack[id - 110])
                    chessBoard.tag_raise(id)

    def promoteTo(self, pieceType, pieceColor, pieceValue):
        global enPassantOpportunity
        global reachedPositions
        global castlingRights
        promotionLocation = -1
        if pieceColor == "w":
            for location in range(0, 8):
                if position[location] == PIECE_TYPE_TRANSLATION[("P", "w")]:
                    promotionLocation = location
                    break
        elif pieceColor == "b":
            for location in range(56, 64):
                if position[location] == PIECE_TYPE_TRANSLATION[("P", "b")]:
                    promotionLocation = location
                    break
        
        chessBoard.moveto(idPositions[promotionLocation], -200, -200)
        promotedPieceId = chessBoard.create_image(SQUARE_WIDTH * (promotionLocation % 8), SQUARE_WIDTH * math.floor(promotionLocation / 8), image = PIECE_TYPE_TO_IMAGE_TRANSLATION[(pieceType, pieceColor)], anchor = "nw")
        pieces.append(Piece(pieceType, pieceColor, promotionLocation, pieceValue, PIECE_TYPE_TO_SUFFICIENCY_VALUE_TRANSLATION[(pieceType, pieceColor)], PIECE_TYPE_TO_IMAGE_TRANSLATION[(pieceType, pieceColor)]))
        chessBoard.tag_bind(promotedPieceId, "<Button-1>", lambda x: Chess.setSelectedPiece(promotedPieceId))

        position[promotionLocation] = PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
        idPositions[promotionLocation] = promotedPieceId
        pieceIdToNumberTranslation[promotedPieceId] = len(pieces) - 1

        if pieceColor == "w":
            for id in chessBoard.find_withtag("white_promotion_UI"):
                chessBoard.moveto(id, -800, -800)
        elif pieceColor == "b":
            for id in chessBoard.find_withtag("black_promotion_UI"):
                chessBoard.moveto(id, -800, -800)

        reachedPositions.clear()
        reachedPositions.append([copy(position), copy(currentTurn), copy(castlingRights), copy(enPassantOpportunity)])
        Chess.gameEndLogic()
        if not gameEnded:
           Chess.printMoveNumberPhrase(currentTurn)
        
        global promotingPawn
        promotingPawn = False

    def enPassant(self, pieceType, pieceColor, destination):
        if pieceType == "P" and enPassantOpportunity == destination:
            if pieceColor == "w":
                chessBoard.moveto(idPositions[destination + 8], -200, -200)
                position[destination + 8] = 0
                idPositions[destination + 8] = 0
            elif pieceColor == "b":
                chessBoard.moveto(idPositions[destination - 8], -200, 200)
                position[destination - 8] = 0
                idPositions[destination - 8] = 0

    def gameEndLogic(self):
        global reachedPositions
        global gameEnded
        movablePieces = False
        for location in range(len(position)):
            if Chess.color(position[location]) == currentTurn:
                if len(Chess.findLegalMoves(location, pieces[pieceIdToNumberTranslation[idPositions[location]]].type, currentTurn, position)) != 0:
                    movablePieces = True
                    break
        if Chess.inCheck(position, currentTurn) and not movablePieces:
            if currentTurn == "w":
                print("Black wins by checkmate.")
                gameEnded = True
                pass
            elif currentTurn == "b":
                print("White wins by checkmate.")
                gameEnded = True
                pass
        elif not movablePieces:
            print("The game is a draw by stalemate.")
            gameEnded = True
            pass
        
        if len(reachedPositions) > 100:
            print("The game is a draw by the 50-move rule.")
            gameEnded = True
            pass

        repetitionCounter = 0
        for absolutePosition in reachedPositions:
            if absolutePosition == reachedPositions[len(reachedPositions) - 1]:
                repetitionCounter += 1
                if repetitionCounter == 3:
                    print("The game is a draw by threefold repetition.")
                    gameEnded = True
                    pass
        
        totalSufficiencyMaterial = 0
        bishopColors = ["", ""]
        for location in range(len(idPositions)):
            if idPositions[location] != 0:
                if pieces[pieceIdToNumberTranslation[idPositions[location]]].type == "B":
                    if bishopColors == ["", ""]:
                        totalSufficiencyMaterial += pieces[pieceIdToNumberTranslation[idPositions[location]]].sufficiencyValue
                    if (location % 2 + math.floor(location / 8)) % 2 == 0:
                        bishopColors[0] = "l"
                    else:
                        bishopColors[1] = "d"
                    if bishopColors == ["l", "d"]:
                        totalSufficiencyMaterial += pieces[pieceIdToNumberTranslation[idPositions[location]]].sufficiencyValue
                else:
                    totalSufficiencyMaterial += pieces[pieceIdToNumberTranslation[idPositions[location]]].sufficiencyValue
                
                if totalSufficiencyMaterial >= 100:
                    break
        if totalSufficiencyMaterial < 100:
            print("The game is a draw by insufficient material.")
            gameEnded = True
            pass

    def findLegalMoves(self, origin, pieceType, pieceColor, position):
        global castlingPossible
        castlingPossible = [[False, False], [False, False]]
        global initiateCastling
        initiateCastling = [[False, False], [False, False]]
        global selectedPiece
        global enPassantOpportunity
        possibleDestinationSquares = []

        if pieceColor != currentTurn:
            return []
        if pieceType == "P":
            if pieceColor == "w":
                if position[origin - 8] == 0:
                    possibleDestinationSquares.append(origin - 8)
                    if Chess.rank(origin) == 2 and position[origin - 16] == 0:
                        possibleDestinationSquares.append(origin - 16)
                if Chess.file(origin) + 1 <= 8 and (Chess.color(position[origin - 7]) == "b" or enPassantOpportunity == origin - 7):
                    possibleDestinationSquares.append(origin - 7)
                if Chess.file(origin) - 1 > 0 and (Chess.color(position[origin - 9]) == "b" or enPassantOpportunity == origin - 9):
                    possibleDestinationSquares.append(origin - 9)
            elif pieceColor == "b":
                if position[origin + 8] == 0:
                    possibleDestinationSquares.append(origin + 8)
                    if Chess.rank(origin) == 7 and position[origin + 16] == 0:
                        possibleDestinationSquares.append(origin + 16)
                if Chess.file(origin) - 1 > 0 and (Chess.color(position[origin + 7]) == "w" or enPassantOpportunity == origin + 7):
                    possibleDestinationSquares.append(origin + 7)
                if Chess.file(origin) + 1 <= 8 and (Chess.color(position[origin + 9]) == "w" or enPassantOpportunity == origin + 9):
                    possibleDestinationSquares.append(origin + 9)
        elif pieceType == "R" or pieceType == "Q":
            for distanceNorth in range(1, 8):
                if Chess.rank(origin) + distanceNorth <= 8:
                    if position[origin - (8 * distanceNorth)] == 0:
                        possibleDestinationSquares.append(origin - (8 * distanceNorth))
                    elif Chess.color(position[origin - (8 * distanceNorth)]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - (8 * distanceNorth))
                        break
                    elif Chess.color(position[origin - (8 * distanceNorth)]) == pieceColor:
                        break
                else:
                    break
            for distanceEast in range(1, 8):
                if Chess.file(origin) + distanceEast <= 8:
                    if position[origin + distanceEast] == 0:
                        possibleDestinationSquares.append(origin + distanceEast)
                    elif Chess.color(position[origin + distanceEast]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + distanceEast)
                        break
                    elif Chess.color(position[origin + distanceEast]) == pieceColor:
                        break
                else:
                    break
            for distanceSouth in range(1, 8):
                if Chess.rank(origin) - distanceSouth > 0:
                    if position[origin + (8 * distanceSouth)] == 0:
                        possibleDestinationSquares.append(origin + (8 * distanceSouth))
                    elif Chess.color(position[origin + (8 * distanceSouth)]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + (8 * distanceSouth))
                        break
                    elif Chess.color(position[origin + (8 * distanceSouth)]) == pieceColor:
                        break
                else:
                    break
            for distanceWest in range(1, 8):
                if Chess.file(origin) - distanceWest > 0:
                    if position[origin - distanceWest] == 0:
                        possibleDestinationSquares.append(origin - distanceWest)
                    elif Chess.color(position[origin - distanceWest]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - distanceWest)
                        break
                    elif Chess.color(position[origin - distanceWest]) == pieceColor:
                        break
                else:
                    break
        elif pieceType == "N":
            if Chess.rank(origin) + 2 <= 8 and Chess.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin - 17)
            if Chess.rank(origin) + 2 <= 8 and Chess.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin - 15)
            if Chess.rank(origin) + 1 <= 8 and Chess.file(origin) - 2 > 0:
                possibleDestinationSquares.append(origin - 10)
            if Chess.rank(origin) + 1 <= 8 and Chess.file(origin) + 2 <= 8:
                possibleDestinationSquares.append(origin - 6)
            if Chess.rank(origin) - 1 > 0 and Chess.file(origin) - 2 > 0:
                possibleDestinationSquares.append(origin + 6)
            if Chess.rank(origin) - 1 > 0 and Chess.file(origin) + 2 <= 8:
                possibleDestinationSquares.append(origin + 10)
            if Chess.rank(origin) - 2 > 0 and Chess.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin + 15)
            if Chess.rank(origin) - 2 > 0 and Chess.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin + 17)
        if pieceType == "B" or pieceType == "Q":
            for distanceNorthwest in range(1, 8):
                if Chess.rank(origin) + distanceNorthwest <= 8 and Chess.file(origin) - distanceNorthwest > 0:
                    if position[origin - (9 * distanceNorthwest)] == 0:
                        possibleDestinationSquares.append(origin - (9 * distanceNorthwest))
                    elif Chess.color(position[origin - (9 * distanceNorthwest)]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - (9 * distanceNorthwest))
                        break
                    elif Chess.color(position[origin - (9 * distanceNorthwest)]) == pieceColor:
                        break
                else:
                    break
            for distanceNortheast in range(1, 8):
                if Chess.rank(origin) + distanceNortheast <= 8 and Chess.file(origin) + distanceNortheast <= 8:
                    if position[origin - (7 * distanceNortheast)] == 0:
                        possibleDestinationSquares.append(origin - (7 * distanceNortheast))
                    elif Chess.color(position[origin - (7 * distanceNortheast)]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin - (7 * distanceNortheast))
                        break
                    elif Chess.color(position[origin - (7 * distanceNortheast)]) == pieceColor:
                        break
                else:
                    break
            for distanceSoutheast in range(1, 8):
                if Chess.rank(origin) - distanceSoutheast > 0 and Chess.file(origin) + distanceSoutheast <= 8:
                    if position[origin + (9 * distanceSoutheast)] == 0:
                        possibleDestinationSquares.append(origin + (9 * distanceSoutheast))
                    elif Chess.color(position[origin + (9 * distanceSoutheast)]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + (9 * distanceSoutheast))
                        break
                    elif Chess.color(position[origin + (9 * distanceSoutheast)]) == pieceColor:
                        break
                else:
                    break
            for distanceSouthwest in range(1, 8):
                if Chess.rank(origin) - distanceSouthwest > 0 and Chess.file(origin) - distanceSouthwest > 0:
                    if position[origin + (7 * distanceSouthwest)] == 0:
                        possibleDestinationSquares.append(origin + (7 * distanceSouthwest))
                    elif Chess.color(position[origin + (7 * distanceSouthwest)]) == Chess.oppositeColor(pieceColor):
                        possibleDestinationSquares.append(origin + (7 * distanceSouthwest))
                        break
                    elif Chess.color(position[origin + (7 * distanceSouthwest)]) == pieceColor:
                        break
                else:
                    break
        elif pieceType == "K":
            if Chess.rank(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin - 8)
            if Chess.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin + 1)
            if Chess.rank(origin) - 1 > 0:
                possibleDestinationSquares.append(origin + 8)
            if Chess.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin - 1)
            if Chess.rank(origin) + 1 <= 8 and Chess.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin - 9)
            if Chess.rank(origin) + 1 <= 8 and Chess.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin - 7)
            if Chess.rank(origin) - 1 > 0 and Chess.file(origin) + 1 <= 8:
                possibleDestinationSquares.append(origin + 9)
            if Chess.rank(origin) - 1 > 0 and Chess.file(origin) - 1 > 0:
                possibleDestinationSquares.append(origin + 7)

            if not Chess.inCheck(position, currentTurn):
                if pieceColor == "w":
                    if castlingRights[0][0]:
                        if position[61] == 0 and position[62] == 0:
                            testPosition = copy(position)
                            testPosition[origin] = 0
                            testPosition[61] = PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not Chess.inCheck(testPosition, currentTurn):
                                possibleDestinationSquares.append(62)
                                castlingPossible[0][0] = True
                    if castlingRights[0][1]:
                        if position[59] == 0 and position[58] == 0 and position[57] == 0:
                            testPosition = copy(position)
                            testPosition[origin] = 0
                            testPosition[59] = PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not Chess.inCheck(testPosition, currentTurn):
                                possibleDestinationSquares.append(58)
                                castlingPossible[0][1] = True
                elif pieceColor == "b":
                    if castlingRights[1][0]:
                        if position[5] == 0 and position[6] == 0:
                            testPosition = copy(position)
                            testPosition[origin] = 0
                            testPosition[5] = PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not Chess.inCheck(testPosition, currentTurn):
                                possibleDestinationSquares.append(6)
                                castlingPossible[1][0] = True
                    if castlingRights[1][1]:
                        if position[3] == 0 and position[2] == 0 and position[1] == 0:
                            testPosition = copy(position)
                            testPosition[origin] = 0
                            testPosition[3] = PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
                            if not Chess.inCheck(testPosition, currentTurn):
                                possibleDestinationSquares.append(2)
                                castlingPossible[1][1] = True
        
        legalDestinationSquares = copy(possibleDestinationSquares)
        for destination in possibleDestinationSquares:
            testPosition = copy(position)
            selfCaptureAttempt = Chess.color(testPosition[destination]) == currentTurn
            testPosition[origin] = 0
            testPosition[destination] = PIECE_TYPE_TRANSLATION[(pieceType, pieceColor)]
            if enPassantOpportunity == destination:
                if pieceColor == "w":
                    testPosition[destination + 8] = 0
                elif pieceColor == "b":
                    testPosition[destination - 8] = 0
            if selfCaptureAttempt or Chess.inCheck(testPosition, currentTurn):
                legalDestinationSquares.pop(legalDestinationSquares.index(destination))
                if enPassantOpportunity == destination:
                    enPassantOpportunity = -1

        return legalDestinationSquares

    def inCheck(self, testPosition, currentTurn):
        opponentColor = Chess.oppositeColor(currentTurn)
        kingPosition = testPosition.index(PIECE_TYPE_TRANSLATION[("K", currentTurn)])
        
        if currentTurn == "w":
            if Chess.rank(kingPosition) + 1 <= 8 and Chess.file(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 9]] == ("P", opponentColor):
                return True
            if Chess.rank(kingPosition) + 1 <= 8 and Chess.file(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 7]] == ("P", opponentColor):
                return True
        elif currentTurn == "b":
            if Chess.rank(kingPosition) - 1 > 0 and Chess.file(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 9]] == ("P", opponentColor):
                return True
            if Chess.rank(kingPosition) - 1 > 0 and Chess.file(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 7]] == ("P", opponentColor):
                return True
        for distanceNorth in range(1, 8):
            if Chess.rank(kingPosition) + distanceNorth <= 8:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition - (8 * distanceNorth)]] == ("R", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition - (8 * distanceNorth)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - (8 * distanceNorth)] != 0:
                    break
            else:
                break
        for distanceEast in range(1, 8):
            if Chess.file(kingPosition) + distanceEast <= 8:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition + distanceEast]] == ("R", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition + distanceEast]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + distanceEast] != 0:
                    break
            else:
                break
        for distanceSouth in range(1, 8):
            if Chess.rank(kingPosition) - distanceSouth > 0:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition + (8 * distanceSouth)]] == ("R", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition + (8 * distanceSouth)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + (8 * distanceSouth)] != 0:
                    break
            else:
                break
        for distanceWest in range(1, 8):
            if Chess.file(kingPosition) - distanceWest > 0:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition - distanceWest]] == ("R", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition - distanceWest]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - distanceWest] != 0:
                    break
            else:
                break
        for distanceNorthwest in range (1, 8):
            if Chess.rank(kingPosition) + distanceNorthwest <= 8 and Chess.file(kingPosition) - distanceNorthwest > 0:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition - (9 * distanceNorthwest)]] == ("B", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition - (9 * distanceNorthwest)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - (9 * distanceNorthwest)] != 0:
                    break
            else:
                break
        for distanceNortheast in range (1, 8):
            if Chess.rank(kingPosition) + distanceNortheast <= 8 and Chess.file(kingPosition) + distanceNortheast <= 8:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition - (7 * distanceNortheast)]] == ("B", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition - (7 * distanceNortheast)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition - (7 * distanceNortheast)] != 0:
                    break
            else:
                break
        for distanceSoutheast in range (1, 8):
            if Chess.rank(kingPosition) - distanceSoutheast > 0 and Chess.file(kingPosition) + distanceSoutheast <= 8:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition + (9 * distanceSoutheast)]] == ("B", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition + (9 * distanceSoutheast)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + (9 * distanceSoutheast)] != 0:
                    break
            else:
                break
        for distanceSouthwest in range (1, 8):
            if Chess.rank(kingPosition) - distanceSouthwest > 0 and Chess.file(kingPosition) - distanceSouthwest > 0:
                if PIECE_ID_TRANSLATION[testPosition[kingPosition + (7 * distanceSouthwest)]] == ("B", opponentColor) or PIECE_ID_TRANSLATION[testPosition[kingPosition + (7 * distanceSouthwest)]] == ("Q", opponentColor):
                    return True
                elif testPosition[kingPosition + (7 * distanceSouthwest)] != 0:
                    break
            else:
                break

        if Chess.rank(kingPosition) + 2 <= 8 and Chess.file(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 17]] == ("N", opponentColor):
            return True
        if Chess.rank(kingPosition) + 2 <= 8 and Chess.file(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 15]] == ("N", opponentColor):
            return True
        if Chess.rank(kingPosition) + 1 <= 8 and Chess.file(kingPosition) - 2 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 10]] == ("N", opponentColor):
            return True
        if Chess.rank(kingPosition) + 1 <= 8 and Chess.file(kingPosition) + 2 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 6]] == ("N", opponentColor):
            return True
        if Chess.rank(kingPosition) - 1 > 0 and Chess.file(kingPosition) - 2 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 6]] == ("N", opponentColor):
            return True
        if Chess.rank(kingPosition) - 1 > 0 and Chess.file(kingPosition) + 2 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 10]] == ("N", opponentColor):
            return True
        if Chess.rank(kingPosition) - 2 > 0 and Chess.file(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 15]] == ("N", opponentColor):
            return True
        if Chess.rank(kingPosition) - 2 > 0 and Chess.file(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 17]] == ("N", opponentColor):
            return True

        if Chess.rank(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 8]] == ("K", opponentColor):
            return True
        if Chess.file(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 1]] == ("K", opponentColor):
            return True
        if Chess.rank(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 8]] == ("K", opponentColor):
            return True
        if Chess.file(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 1]] == ("K", opponentColor):
            return True
        if Chess.rank(kingPosition) + 1 <= 8 and Chess.file(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 9]] == ("K", opponentColor):
            return True
        if Chess.rank(kingPosition) + 1 <= 8 and Chess.file(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition - 7]] == ("K", opponentColor):
            return True
        if Chess.rank(kingPosition) - 1 > 0 and Chess.file(kingPosition) + 1 <= 8 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 9]] == ("K", opponentColor):
            return True
        if Chess.rank(kingPosition) - 1 > 0 and Chess.file(kingPosition) - 1 > 0 and PIECE_ID_TRANSLATION[testPosition[kingPosition + 7]] == ("K", opponentColor):
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
        global currentTurn
        currentTurn = Chess.oppositeColor(currentTurn)

    def printMoveNumberPhrase(self, currentTurn):
        if currentTurn == "w":
            print("Move " + str(moveNumber) + ". White to move.")
        elif currentTurn == "b":
            print("Move " + str(moveNumber) + ". Black to move.")

    def initializeSquares(self):
        squares = []
        for location in range(64):
            if (location % 2 + math.floor(location / 8)) % 2 == 0:
                complex = "l"
                color = DEFAULT_LIGHT_SQUARE_COLOR
            else:
                complex = "d"
                color = DEFAULT_DARK_SQUARE_COLOR
            squares.append(Square(complex, color, location))
        return squares

    def highlightSquares(self, legalMoves):
        for square in squares:
            if legalMoves.count(square.location) != 0:
                if square.complex == "l":
                    square.color = HIGHLIGHTED_LIGHT_SQUARE_COLOR
                elif square.complex == "d":
                    square.color = HIGHLIGHTED_DARK_SQUARE_COLOR
                chessBoard.itemconfig(square_ids[square.location], fill = square.color, outline = square.color)

    def unhighlightSquares(self, legalMoves):
        for square in squares:
            if legalMoves.count(square.location) != 0:
                if square.complex == "l":
                    square.color = DEFAULT_LIGHT_SQUARE_COLOR
                elif square.complex == "d":
                    square.color = DEFAULT_DARK_SQUARE_COLOR
                chessBoard.itemconfig(square_ids[square.location], fill = square.color, outline = square.color)

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
        chessBoard.tag_bind(1, "<Button-1>", lambda x: Chess.setSelectedPiece(1))
        chessBoard.tag_bind(2, "<Button-1>", lambda x: Chess.setSelectedPiece(2))
        chessBoard.tag_bind(3, "<Button-1>", lambda x: Chess.setSelectedPiece(3))
        chessBoard.tag_bind(4, "<Button-1>", lambda x: Chess.setSelectedPiece(4))
        chessBoard.tag_bind(5, "<Button-1>", lambda x: Chess.setSelectedPiece(5))
        chessBoard.tag_bind(6, "<Button-1>", lambda x: Chess.setSelectedPiece(6))
        chessBoard.tag_bind(7, "<Button-1>", lambda x: Chess.setSelectedPiece(7))
        chessBoard.tag_bind(8, "<Button-1>", lambda x: Chess.setSelectedPiece(8))
        chessBoard.tag_bind(9, "<Button-1>", lambda x: Chess.setSelectedPiece(9))
        chessBoard.tag_bind(10, "<Button-1>", lambda x: Chess.setSelectedPiece(10))
        chessBoard.tag_bind(11, "<Button-1>", lambda x: Chess.setSelectedPiece(11))
        chessBoard.tag_bind(12, "<Button-1>", lambda x: Chess.setSelectedPiece(12))
        chessBoard.tag_bind(13, "<Button-1>", lambda x: Chess.setSelectedPiece(13))
        chessBoard.tag_bind(14, "<Button-1>", lambda x: Chess.setSelectedPiece(14))
        chessBoard.tag_bind(15, "<Button-1>", lambda x: Chess.setSelectedPiece(15))
        chessBoard.tag_bind(16, "<Button-1>", lambda x: Chess.setSelectedPiece(16))
        chessBoard.tag_bind(17, "<Button-1>", lambda x: Chess.setSelectedPiece(17))
        chessBoard.tag_bind(18, "<Button-1>", lambda x: Chess.setSelectedPiece(18))
        chessBoard.tag_bind(19, "<Button-1>", lambda x: Chess.setSelectedPiece(19))
        chessBoard.tag_bind(20, "<Button-1>", lambda x: Chess.setSelectedPiece(20))
        chessBoard.tag_bind(21, "<Button-1>", lambda x: Chess.setSelectedPiece(21))
        chessBoard.tag_bind(22, "<Button-1>", lambda x: Chess.setSelectedPiece(22))
        chessBoard.tag_bind(23, "<Button-1>", lambda x: Chess.setSelectedPiece(23))
        chessBoard.tag_bind(24, "<Button-1>", lambda x: Chess.setSelectedPiece(24))
        chessBoard.tag_bind(25, "<Button-1>", lambda x: Chess.setSelectedPiece(25))
        chessBoard.tag_bind(26, "<Button-1>", lambda x: Chess.setSelectedPiece(26))
        chessBoard.tag_bind(27, "<Button-1>", lambda x: Chess.setSelectedPiece(27))
        chessBoard.tag_bind(28, "<Button-1>", lambda x: Chess.setSelectedPiece(28))
        chessBoard.tag_bind(29, "<Button-1>", lambda x: Chess.setSelectedPiece(29))
        chessBoard.tag_bind(30, "<Button-1>", lambda x: Chess.setSelectedPiece(30))
        chessBoard.tag_bind(31, "<Button-1>", lambda x: Chess.setSelectedPiece(31))
        chessBoard.tag_bind(32, "<Button-1>", lambda x: Chess.setSelectedPiece(32))

        chessBoard.tag_bind(106, "<Button-1>", lambda x: Chess.promoteTo("Q", "w", 9))
        chessBoard.tag_bind(107, "<Button-1>", lambda x: Chess.promoteTo("N", "w", 3))
        chessBoard.tag_bind(108, "<Button-1>", lambda x: Chess.promoteTo("R", "w", 5))
        chessBoard.tag_bind(109, "<Button-1>", lambda x: Chess.promoteTo("B", "w", 3))
        chessBoard.tag_bind(111, "<Button-1>", lambda x: Chess.promoteTo("Q", "b", 9))
        chessBoard.tag_bind(112, "<Button-1>", lambda x: Chess.promoteTo("N", "b", 3))
        chessBoard.tag_bind(113, "<Button-1>", lambda x: Chess.promoteTo("R", "b", 5))
        chessBoard.tag_bind(114, "<Button-1>", lambda x: Chess.promoteTo("B", "b", 3))

    def playMove(move):
        global root

        originCoordinates = move[0] + move[1]
        destinationCoordinates = move[2] + move[3]

        origin = Chess.convertToLocation(originCoordinates)
        destination = Chess.convertToLocation(destinationCoordinates)

        x = SQUARE_WIDTH * (destination % 8) + SQUARE_WIDTH / 2
        y = SQUARE_WIDTH * math.floor(destination / 8) + SQUARE_WIDTH / 2
        
        Chess.setSelectedPiece(idPositions[origin])
        Chess.movePiece(x, y)

    def convertToLocation(self, coordinates):
        fileLabels = "abcdefgh"
        rankLabels = "12345678"

        fileIndex = fileLabels.index(coordinates[0])
        rankIndex = rankLabels.index(coordinates[1])

        location = 8 * (7 - rankIndex) + fileIndex
        return location

Chess.game()