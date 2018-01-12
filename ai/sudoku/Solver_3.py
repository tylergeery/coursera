import math
from Board_3 import Board
from Domain_3 import Domain

class Solver:
    def __init__(self, board):
        self.best = board
        #self.queue = self.initializeConstraints()

    # def AC3(self):
    #     """
    #     Implements the AC3 algorithm
    #     Returns: Board
    #     """
    #     while len(self.queue) > 0:
    #         constraint = self.queue.pop(0)
    #
    #         if self.revised(constraint):
    #             domain_values = self.domain.getDomainValues(constraint[0])
    #
    #             if len(domain_values) == 0:
    #                 print('could not be solved, stopping at: ', constraint[0])
    #                 break
    #             if len(domain_values) == 1:
    #                 self.board.setValue(constraint[0], domain_values[0])
    #
    #             self.addPositionConstraints(constraint[0])
    #
    #     for i in range(81):
    #         if self.board.getValue(i) == 0:
    #             values = self.board.getAvailableValues(i)
    #
    #             if (len(values) == 1):
    #                 self.board.setValue(i, values[0])
    #
    #     return self.board
    #
    # def revised(self, constraint):
    #     if self.board.getValue(constraint[0]) != 0:
    #         return False
    #
    #     revised = False
    #     available_values = self.board.getAvailableValues(constraint[0])
    #
    #     for value in self.domain.getDomainValues(constraint[0]):
    #         neighbor_has_available_values = True
    #         neighbor_domain_values = self.domain.getDomainValues(constraint[1])
    #
    #         if len(neighbor_domain_values) == 0:
    #             neighbor_has_available_values = False
    #         elif len(neighbor_domain_values) == 1 and neighbor_domain_values[0] == value:
    #             neighbor_has_available_values = False
    #
    #         if not neighbor_has_available_values or value not in available_values:
    #             self.domain.removeValue(constraint[0], value)
    #             revised = True
    #
    #     return revised

    def BTS(self, board, depth=1):
        """
        Implements Backtracking Search algorithm
        Returns: Board
        """
        if (board.solved()):
            return board

        domain = Domain(board)
        unassigned = domain.getOpenPos()

        for value in board.getAvailableValues(unassigned):
            # print domain.domains[unassigned];
            # print str(unassigned) + "\n\n";
            board.setValue(unassigned, value)
            domain.updateNeighbors(unassigned)

            if depth < 80:
                copy = self.BTS(board.copy(), depth + 1)

                if copy.solved():
                    return copy
                elif copy.getHeuristic() > self.best.getHeuristic():
                    self.best = copy

            #board.pretty();
            # print domain.domains[unassigned];
            # print "\n\n";
            board.setValue(unassigned, 0)
            domain.updateNeighbors(unassigned)

        return self.best

    # def inSameSquare(self, pos1, pos2):
    #     """
    #     Are the two positions in the same square?
    #     Returns: bool
    #     """
    #     sameColThird = (math.floor((pos1 % 9) / 3) == math.floor((pos2 % 9) / 3))
    #     sameRowThird = (math.floor(pos1/27) == math.floor(pos2/27))
    #
    #     return sameRowThird and sameColThird

    # def addPositionConstraints(self, pos):
    #     row_start = self.board.getRowStart(pos)
    #     col_start = self.board.getColumnStart(pos)
    #     sq_start = self.board.getSquareStart(pos)
    #
    #     for i in range(9):
    #         if (row_start + i) != pos:
    #             self.queue.append((row_start + i, pos))
    #         if ((col_start + 9*i) != pos):
    #             self.queue.append((col_start + 9*i, pos))
    #
    #     for offset in [0,1,2,9,10,11,18,19,20]:
    #         if (sq_start + offset) != pos:
    #             self.queue.append((sq_start + offset, pos))

    # def initializeConstraints(self):
    #     """
    #     Get sudoku global game contstraints as binary constraints.
    #     This means creating a constraint for all connected nodes
    #     Returns: array
    #     """
    #     constraints = []
    #
    #     for i in range(9):
    #         for j in range(9):
    #             for k in range(j+1, 9):
    #                 # initialize row constraints
    #                 constraints.append((i*9 + j, i*9 + k))
    #                 # initialize col constraints
    #                 constraints.append((j*9 + i, k*9 + i))
    #
    #             # initialize square constraints
    #             pos1 = i * 9 + j
    #             for diff in [7, 8, 10, 11, 16, 17, 19, 20]:
    #                 pos2 = i * 9 + j + diff
    #                 if self.inSameSquare(pos1, pos2):
    #                     constraints.append((pos1, pos2))
    #
    #     return constraints
