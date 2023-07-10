from ChessSim import ChessSim

simTest = ChessSim()

position = simTest.position

legalMoves = simTest.generateAllLegalMoves(position)
print(legalMoves)