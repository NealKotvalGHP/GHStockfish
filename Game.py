from ChessSim import ChessSim
from Agent import Agent
from App import Chess

simTest = ChessSim(INITIAL_POSITION, "w", [[True, True], [True, True]], -1)

print(simTest.position)

simTest.playMove("e2e4")
simTest.playMove("e7e5")

simTest.playMove("f1c4")
simTest.playMove("b8c6")

simTest.playMove("d1h5")
simTest.playMove("g8f6")

simTest.playMove("h5f7")

# Agent will be initialized with the position it is analyzing. To evaluate positions branching from this,
# run the simulator to update self.game.position. The position to analyze is stored inside of self.position.
# I will add a restart function inside of the simulator that returns to the initial self.position.
agent = Agent(simTest.position, simTest.currentTurn, simTest.castlingRights, simTest.enPassantOpportunity)
print(agent.evaluate())