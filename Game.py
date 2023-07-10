from ChessSim import ChessSim
from Agent import Agent

simTest = ChessSim()


simTest.playMove("e2e4")
simTest.playMove("e7e5")

simTest.playMove("f1c4")
simTest.playMove("b8c6")

simTest.playMove("d1h5")
simTest.playMove("g8f6")

simTest.playMove("h5f7")

agent = Agent("w")
print(agent.evaluate(simTest))