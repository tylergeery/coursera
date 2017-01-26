#!/usr/bin/python

import sys

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

"""
Read/Validate CLI arguments
Create Board
Call solve with method
"""
def main():
    if len(sys.argv) != 3:
        print '\nUsage:', sys.argv[0], '<method> <board>\n'
        exit()

    method = sys.argv[1]
    board = map(int, sys.argv[2].split(','))

    if len(board) != 9:
        print '\nBoard must be of length 9. (e.g "0,2,5,6,3,1,8,7,4")\n'
        exit()

    solve(method, board)


"""
Solve given board by expected search method
"""
def solve(method, board):
    search_methods = {
        'dfs': solve_dfs,
        'bfs': solve_bfs
    }

    if method not in search_methods:
        print '\nMethod must be in (', ', '.join(search_methods.keys()) , ')\n'
        exit()

    search_methods[method](board)


#TODO
def solve_dfs(board):
    return
def solve_bfs(board):
    return
def output():
    return

if __name__ == "__main__":
    main()
