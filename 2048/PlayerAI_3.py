import time
import math
from random import randint
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
    def __init__(self):
        self.iter = 0
        self.lastMove = 0
        self.lastVertical = 0
        self.lastHorizontal = 0

    def getMove(self, grid):
        """
        Ensures that the best available move is found in a reasonable time.

        Makes calls to the recursive minimax algorithm
        """
        time_started = time.time()
        best_move = None
        depth = 1
        max_utility = 0

        while ((time.time() - time_started) < .03):
            # keep incrementings depths until we run out of time
            move, utility = self.maximize(grid, depth, float("-inf"), float("inf"))

            if (utility > max_utility):
                max_utility, best_move = (utility, move)

            depth += 1

        self.registerMove(best_move)

        print("max depth {}, moving {}".format(depth, best_move))
        return move

    def getOrderedMoves(self, grid, maxi = True):
        """
        Get the grid moves ordered for best branch prediction
        """
        moves = grid.getAvailableMoves()
        moves_ordered = []

        horizontals = []
        verticals = []

        for i in [2,3]:
            if i in moves:
                horizontals.append(i)

        for i in [0,1]:
            if i in moves:
                verticals.append(i)

        if self.lastVertical == 2:
            horizontals.reverse()

        if self.lastHorizontal == 0:
            verticals.reverse()

        if self.lastMove is not None and self.lastMove >> 1:
            # last move was horizontal
            moves_ordered = verticals + horizontals
        else:
            moves_ordered = horizontals + verticals

        # reverse order for lowest expected values first
        if maxi == False:
            moves_ordered.reverse()

        return moves_ordered

    def registerMove(self, move):
        """
        Keep the last move recorded for branch prediction
        """
        self.lastMove = move

        if move is not None and move >> 1:
            self.lastHorizontal = move
        else:
            self.lastVertical = move

    def minimize(self, grid, depth, alpha, beta):
        """
        Minimize part of minimax function
        Acts as a competitor to the user
        """

        # check for terminal node
        if depth == 0:
            return (None, self.eval(grid))

        best_move, min_utility = (None, float("inf"))

        for move in self.getOrderedMoves(grid, False):
            new_grid = grid.clone()
            new_grid.move(move)

            tmp, utility = self.maximize(new_grid, depth-1, alpha, beta)

            # set new best case
            if utility < min_utility:
                best_move, min_utility = (move, utility)

            # prune branches where maximum utility is under previous min value
            if min_utility <= alpha:
                break

            # set a new possible worst (min) case
            if min_utility < beta:
                beta = min_utility

        return (best_move, min_utility)

    def maximize(self, grid, depth, alpha, beta):
        """
        Maximize part of minimax function
        Acts in the user's best interest to win the game
        """

        # check for terminal node
        if depth == 0:
            return (None, self.eval(grid))

        best_move, max_utility = (None, float("-inf"))

        for move in self.getOrderedMoves(grid):
            new_grid = grid.clone()
            new_grid.move(move)

            tmp, utility = self.minimize(new_grid, depth-1, alpha, beta)

            # set new best case
            if utility > max_utility:
                best_move, max_utility = (move, utility)

            # prune branches where minimal utility is under previous maximized value
            if max_utility >= beta:
                break

            # set a new possible best case
            if max_utility > alpha:
                alpha = max_utility


        return (best_move, max_utility)

    # def eval2(self, grid):
    #     """
    #     Evaluate the current grid state
    #
    #     This is the heuristic function that evaluates board states
    #     """
    #     max_tile, max_on_side, smoothing_sum, matching_count, outer_score, closeness, utility = self.getGridStats(grid)
    #     #max_tile, outer_score = self.getSimpleStats(grid)
    #     max_tile_factor = 50 * math.log(max_tile, 2)
    #     cell_factor = 100 * max_tile * len(grid.getAvailableCells())
    #     smoothing_factor = 15 * math.log(smoothing_sum, 2)
    #     matching_factor = 5 * math.log(matching_count, 2)
    #     outer_factor = 10 * math.log(outer_score)
    #     closeness_factor = 10 * closeness
    #     utility_factor = -4 * math.log(max(utility, 1))
    #     max_in_corner_factor = 20 * max_tile * max_on_side
    #
    #     #print("max: {}, cell: {}, outer: {}".format(max_tile_factor, cell_factor, outer_factor))
    #     #return max_tile_factor + cell_factor + outer_factor
    #     #print("max: {}, cell: {}, smoothing: {}, matching: {}, outer: {}, closeness: {}, utility: {}".format(max_tile_factor, cell_factor, smoothing_factor, matching_factor, outer_factor, closeness_factor, utility_factor))
    #     return (max_tile_factor + cell_factor + smoothing_factor + matching_factor + outer_factor + closeness_factor + max_in_corner_factor + utility_factor)

    def eval(self, grid):
        mx = grid.getMaxTile()
        log_mx = math.log(mx, 2)
        sm_diff = 1
        corner_diff = 1
        max_pos = (0,0)
        found = False
        low_count = 0
        totals = [0,0,0,0]

        # get max tile pos
        for i in range(len(grid.map) - 1):
            for j in range(len(grid.map[i]) - 1):
                if (mx == grid.getCellValue((i, j))):
                    max_pos = (i,j)
                    found = True
                    break

            if found:
                break

        max_in_corner = found and ((max_pos[0] == 0 or max_pos[0] == 3) and (max_pos[1] == 0 or max_pos[1] == 3))
        for i in range(len(grid.map) - 1):
            for j in range(len(grid.map[i]) - 1):
                value = grid.getCellValue((i, j))
                right_value = self.findRightCellValue(grid, [i, j])
                lower_value = self.findLowerCellValue(grid, [i, j])

                log_value = math.log(max(value, 1), 2)
                log_right = math.log(max(right_value, 1), 2)
                log_lower = math.log(max(lower_value, 1), 2)

                if value > 0 and right_value > 0:
                    sm_diff -= abs(log_value - log_right)
                if value > 0 and lower_value > 0:
                    sm_diff -= abs(log_value - log_lower)

                if right_value > 0 and value > right_value:
                    totals[0] += abs(log_value - log_right)
                elif value > 0 and right_value > value:
                    totals[1] += abs(log_right - log_value)

                if lower_value > 0 and value > lower_value:
                    totals[2] += abs(log_value - log_lower)
                elif value > 0 and lower_value > value:
                    totals[3] += abs(log_lower - log_value)

                if log_value < (log_mx - 2):
                    low_count -= 1

        # build heuristic factors
        sm = 0.5 * sm_diff
        available = 3 * len(grid.getAvailableCells())
        corner = (1/corner_diff) * log_mx
        max_corner = 10 * int(max_in_corner)
        monotonicity = max(totals[0], totals[1]) + max(totals[2], totals[3])
        low = low_count

        print("sm: {}, available: {}, monotonicity: {}".format(int(sm), int(available), int(monotonicity)))

        return available + sm + monotonicity + mx

    def findRightCellValue(self, grid, pos):
        pos[0] += 1

        while (pos[0] < 4):
            value = grid.getCellValue(pos)
            if value > 0:
                return value

            pos[0] += 1
        return 0

    def findLowerCellValue(self, grid, pos):
        pos[1] += 1

        while (pos[1] < 4):
            value = grid.getCellValue(pos)
            if value > 0:
                return value

            pos[1] += 1
        return 0
    # def getGridStats(self, grid):
    #     """
    #     Get the sum of absolute value of differences between grid members and neighbors
    #     """
    #     smoothing_sum = 1
    #     matching_count = 1
    #     outer_stats = 0
    #     closeness = 0
    #     utility = 0
    #     max_pos = (0,0)
    #     max_tile = grid.getMaxTile()
    #     found = False
    #
    #     # get max tile pos
    #     for i in range(len(grid.map) - 1):
    #         for j in range(len(grid.map[i]) - 1):
    #             if (max_tile == grid.getCellValue((i, j))):
    #                 max_pos = (i,j)
    #                 found = True
    #                 break
    #
    #         if found:
    #             break
    #
    #     max_on_side = (max_pos[0] == 0 or max_pos[0] == 3 or max_pos[1] == 0 or max_pos[1] == 3)
    #     for i in range(len(grid.map) - 1):
    #         for j in range(len(grid.map[i]) - 1):
    #             value = grid.getCellValue((i, j))
    #             right_value = grid.getCellValue((i, j+1))
    #             lower_value = grid.getCellValue((i+1, j))
    #
    #             if value != max_tile:
    #                 utility += self.calculateUtility(value, (i,j), max_tile, max_pos)
    #
    #             if value == right_value and value > 0:
    #                 matching_count += right_value
    #             if value == lower_value and value > 0:
    #                 matching_count += lower_value
    #
    #             if value > 0 and right_value > 0 and abs(math.log(value, 2) - math.log(right_value, 2)) == 1:
    #                 closeness += 1
    #             if value > 0 and lower_value > 0 and abs(math.log(value, 2) - math.log(lower_value, 2)) == 1:
    #                 closeness += 1
    #
    #             if i == 0:
    #                 smoothing_sum += abs(value - grid.getCellValue((3, j)))
    #                 outer_stats += value - grid.getCellValue((1, j))
    #             if j == 0:
    #                 smoothing_sum += abs(value - grid.getCellValue((i, 3)))
    #                 outer_stats += value - grid.getCellValue((i, 1))
    #
    #             if i == 3:
    #                 outer_stats += value - grid.getCellValue((2, j))
    #             if j == 3:
    #                 outer_stats += value - grid.getCellValue((i, 2))
    #
    #
    #     return (max_tile, max_on_side, smoothing_sum, matching_count, max(outer_stats, 1), closeness, utility)

    # def isMaxInCorner(self, grid, max_value):
    #     """
    #     Is the max grid value in the corner??
    #     Returns: 1 or 0
    #     """
    #     if grid.getCellValue((0,0)) == max_value or grid.getCellValue((0,3)) == max_value or grid.getCellValue((3,0)) == max_value or grid.getCellValue((3,3)) == max_value:
    #         return 1
    #
    #     return 0

    # def calculateUtility(self, value, pos, max_value, max_pos):
    #     """
    #     Get the utility of a spot
    #
    #     Higher is worse
    #     """
    #     if value <= 0 or max_value <= 0:
    #         return 0
    #
    #     distance = abs(max_pos[0] - pos[0]) + abs(max_pos[1] - pos[1])
    #     log_diff = math.log(max_value, 2) - math.log(value, 2)
    #
    #     return math.log(value, 2) * abs(distance - log_diff)
