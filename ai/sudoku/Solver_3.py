import math
from Board_3 import Board
from Domain_3 import Domain

class Solver:
    def AC3(self, board):
        """
        Implements the AC3 algorithm
        Returns: Board
        """
        queue = self.initializeConstraints(board)

        print(len(queue))
        while len(queue) > 0:
            pos1, pos2 = queue.pop(0)
            #print(pos1, pos2)

        return board

    def BTS(self, board):
        """
        Implements Backtracking Search algorithm
        Returns: Board
        """
        return board

    def inSameSquare(self, pos1, pos2):
        """
        Are the two positions in the same square?
        Returns: bool
        """
        sameColThird = (math.floor((pos1 % 9) / 3) == math.floor((pos2 % 9) / 3))
        sameRowThird = (math.floor(pos1/27) == math.floor(pos2/27))

        return sameRowThird and sameColThird

    def initializeConstraints(self, board):
        constraints = []

        for i in range(9):
            for j in range(9):
                for k in range(j+1, 9):
                    # initialize row constraints
                    constraints.append((i*9 + j, i*9 + k))
                    # initialize col constraints
                    constraints.append((j*9 + i, k*9 + i))

                # initialize square constraints
                pos1 = i * 9 + j
                pos2 = i * 9 + j + 10
                if self.inSameSquare(pos1, pos2):
                    constraints.append((pos1, pos2))

        return constraints
