from random import randint
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
    def __init__(self):
        self.iter = 0

    def getMove(self, grid):
        self.iter += 1
        self.eval(grid)

        return self.iter % 4

    def eval(self, grid):
        """
        Evaluate the current grid state
        """
        print(self, grid.map)
