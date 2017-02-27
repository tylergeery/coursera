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

        while ((time.time() - time_started) < .004):
            # keep incrementings depths until we run out of time
            move, utility = self.minimax(grid, depth, float("-inf"), float("inf"))

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
            highest = alpha
            for move in grid.getAvailableMoves():
                new_grid = grid.clone()
                new_grid.move(move)

                m, u = self.minimax(new_grid, depth-1, highest, beta, False)

                print("util: {}, move: {}, highest: {}, beta: {}".format(u, move, highest, beta))
                if u > highest:
                    best_move = move
                    highest = u

            return (best_move, min(highest, beta))
        else:
            lowest = beta
            for move in grid.getAvailableMoves():
                new_grid = grid.clone()
                new_grid.move(move)

                m, u = self.minimax(new_grid, depth-1, alpha, lowest, True)

                if u < lowest:
                    best_move = move
                    lowest = u

                if lowest < alpha:
                    continue

            return (best_move, max(lowest, alpha))

    def eval(self, grid):
        """
        Evaluate the current grid state

        This is the heuristic function that evaluates board states
        """
        max_tile = grid.getMaxTile()
        smoothing_sum, matching_count, outer_score, closeness = self.getGridStats(grid)
        max_tile_factor = 7 * math.log(max_tile, 2)
        cell_factor = 8 * len(grid.getAvailableCells())
        smoothing_factor = 3 * math.log(smoothing_sum, 2)
        matching_factor = 7 * math.log(matching_count, 2)
        outer_factor = 5 * math.log(outer_score)
        closeness_factor = 2 * closeness
        max_in_corner_factor = 15 * self.isMaxInCorner(grid, max_tile)

        print("max: {}, cell: {}, smoothing: {}, matching: {}, outer: {}, closeness: {}".format(max_tile_factor, cell_factor, smoothing_factor, matching_factor, outer_factor, closeness_factor))
        return (max_tile_factor + cell_factor + smoothing_factor + matching_factor + outer_factor + closeness_factor + max_in_corner_factor)

    def getGridStats(self, grid):
        """
        Get the sum of absolute value of differences between grid members and neighbors
        """
        smoothing_sum = 1
        matching_count = 1
        outer_stats = 0
        closeness = 0

        for i in range(len(grid.map) - 1):
            for j in range(len(grid.map[i]) - 1):
                value = grid.getCellValue((i, j))
                right_value = grid.getCellValue((i, j+1))
                lower_value = grid.getCellValue((i+1, j))

                if value == right_value and value > 0:
                    matching_count += right_value
                if value == lower_value and value > 0:
                    matching_count += lower_value

                if value > 0 and right_value > 0:
                    print("log difference: {}".format(abs(math.log(value, 2) - math.log(right_value, 2))))
                if value > 0 and right_value > 0 and abs(math.log(value, 2) - math.log(right_value, 2)) == 1:
                    closeness += 1
                if value > 0 and lower_value > 0 and abs(math.log(value, 2) - math.log(lower_value, 2)) == 1:
                    closeness += 1

                if i == 0:
                    smoothing_sum += abs(value - grid.getCellValue((3, j)))
                    outer_stats += value - grid.getCellValue((1, j))
                if j == 0:
                    smoothing_sum += abs(value - grid.getCellValue((i, 3)))
                    outer_stats += value - grid.getCellValue((i, 1))

                if i == 3:
                    outer_stats += value - grid.getCellValue((2, j))
                if j == 3:
                    outer_stats += value - grid.getCellValue((i, 2))


        return (smoothing_sum, matching_count, max(outer_stats, 1), closeness)

    def isMaxInCorner(self, grid, max_value):
        """
        Is the max grid value in the corner??
        Returns: 1 or 0
        """
        if grid.getCellValue((0,0)) == max_value or grid.getCellValue((0,3)) == max_value or grid.getCellValue((3,0)) == max_value or grid.getCellValue((3,3)) == max_value:
            return 1

        return 0
