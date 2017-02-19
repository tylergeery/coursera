import time
import math
from random import randint
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
    def __init__(self):
        self.iter = 0

    def getMove(self, grid):
        """
        Ensures that the best available move is found in a reasonable time.

        Makes calls to the recursive minimax algorithm
        """
        time_started = time.time()
        best_move = 0
        depth = 1
        max_utility = 0

        while ((time.time() - time_started) < .002):
            # keep incrementings depths until we run out of time
            move, utility = self.minimax(grid, depth, float("-inf"), float("-inf"))

            if (utility > max_utility):
                max_utility = utility
                best_move = move

            depth += 1

        print("max depth {}".format(depth))
        return move

    def minimax(self, grid, depth, alpha, beta, maximize = True):
        """
        Recursive function that finds the best grid state out of available moves
        Will call itsself with a decrementing depth, until depth is 0
        """
        best_move = 0
        if depth == 0:
            return (0, self.eval(grid))

        if (maximize):
            highest = float("-inf")
            for move in grid.getAvailableMoves():
                new_grid = grid.clone()
                new_grid.move(move)

                m, u = self.minimax(new_grid, depth-1, alpha, beta, False)

                if u > highest:
                    best_move = move
                    highest = u

            return (best_move, highest)
        else:
            lowest = float("inf")
            for move in grid.getAvailableMoves():
                new_grid = grid.clone()
                new_grid.move(move)

                m, u = self.minimax(new_grid, depth-1, alpha, beta, True)

                if u < beta:
                    continue

                if u < lowest:
                    best_move = move
                    lowest = u

            return (best_move, lowest)

    def eval(self, grid):
        """
        Evaluate the current grid state

        This is the heuristic function that evaluates board states
        """
        max_tile = grid.getMaxTile()
        smoothing_sum, matching_count = self.getGridStats(grid)
        max_tile_factor = math.log(max_tile, 2)
        cell_factor = len(grid.getAvailableCells())
        smoothing_factor = 10*max_tile/smoothing_sum
        matching_factor = matching_count * matching_count

        #print("max: {}, cell: {}, smoothing: {}, matching: {}".format(max_tile_factor, cell_factor, smoothing_factor, matching_factor))
        return (max_tile_factor + cell_factor + smoothing_factor + matching_factor)

    def getGridStats(self, grid):
        """
        Get the sum of absolute value of differences between grid members and neighbors
        """
        abs_sum = 1
        matching_count = 0

        for i in range(len(grid.map) - 1):
            for j in range(len(grid.map[i]) - 1):
                value = grid.getCellValue((i, j))
                right_value = grid.getCellValue((i, j+1))
                lower_value = grid.getCellValue((i+1, j))

                if (value == right_value):
                    matching_count += 1
                if (value == lower_value):
                    matching_count += 1

                abs_sum += abs(value - right_value) + abs(value - lower_value)

        return (abs_sum, matching_count)
