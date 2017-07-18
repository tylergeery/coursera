import sys
import os.path
from Board_3 import Board
from Solver_3 import Solver

def get_board(input_string):
    return Board(list(map(int, input_string)))

def solve(board):
    """
    Solves the given sudoku board,
    first attempting the AC3 algorithm, then backtracking (BTS)
    """
    solver = Solver()
    solution = solver.AC3(board)

    if (solution.solved()):
        return (solution, 'AC3')

    return (solver.BTS(board), 'BTS')

def output(solution, method):
    """
    Write the completed board solution to output.txt
    Will also include the method that completed the board
    """
    output_file = open('output.txt', 'w')
    output_file.write(solution.get_as_string() + " " + method)
    output_file.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <input_string>")
        sys.exit()

    if len(sys.argv[1]) != 81:
        print("Usage: {} <input_string | 81 char board representation>")
        sys.exit()

    # create board respresentation
    board = get_board(sys.argv[1])

    # solve
    solution, method = solve(board)

    # output
    output(solution, method)
