#!/usr/bin/python

import sys
import resource
import time
import heapq

# convenience
def i_arr_to_s(i_arr): return ''.join(map(str, i_arr))
def s_to_i_arr(s): return map(int, list(s))
def cs_to_i_arr(cs): return map(int, cs.split(','))


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
    board = cs_to_i_arr(sys.argv[2])

    #TODO validate numbers in board
    if len(board) != 9:
        print '\nBoard must be of length 9. (e.g "0,2,5,6,3,1,8,7,4")\n'
        exit()

    Solver(method, i_arr_to_s(board))

class State:
    def __init__(self, board_path_tuple):
        self.board = Board(s_to_i_arr(board_path_tuple[0]))
        self.path = board_path_tuple[1]

    def get_path(self):
        path_output = {
            'U': "'Up'",
            'D': "'Down'",
            'L': "'Left'",
            'R': "'Right'"
        }
        path_arr = []
        for c in self.path:
            path_arr.append(path_output[c])

        return '[{0}]'.format(', '.join(path_arr))

class Board:
    def __init__(self, board):
        self.board = board

    def is_complete(self):
        for i in range(8):
            if self.board[i] != i:
                return False

        return True

    def move_allowed(self, move):
        zero_index = self.board.index(0)
        #print "Adding move ({0}) found 0-index ({1}):".format(move, zero_index)

        if move == 'L':
            return (zero_index % 3) != 0
        if move == 'R':
            return (zero_index % 3) != 2
        if move == 'U':
            return (zero_index > 2)
        if move == 'D':
            return (zero_index < 6)

        print 'Move', move, 'not allowed!'
        exit()

    def get_board_after_move(self, move):
        zero_index = self.board.index(0)
        swap_index = zero_index + 3 # default 'D'

        if move == 'L':
            swap_index = zero_index - 1
        if move == 'R':
            swap_index = zero_index + 1
        if move == 'U':
            swap_index = zero_index - 3

        board = list(self.board) # mutable
        board[zero_index] = board[swap_index]
        board[swap_index] = 0

        return i_arr_to_s(board)

    def get_municipal_priority(self):
        m_sum = 0

        for i in range(8):
            m_sum += abs(int(self.board[i]) - i)

        return m_sum


"""
Solver class will solve and output
"""
class Solver:
    time_started = time.clock()
    frontier = []
    solution = False
    nodes_expanded = 0
    max_fringe_size = 0
    max_search_depth = 0

    def __init__(self, method, board):
        if method == 'bfs':
            self.solve_bfs(board)
        elif method == 'dfs':
            self.solve_dfs(board)
        elif method == 'ast':
            self.solve_ast(board)
        elif method == 'ida':
            self.solve_ida(board)
        else:
            raise RuntimeError("Method '{0}' is unknown".format(method))

        self.output()

    def solve_bfs(self, board):
        self.frontier.append((board, '')) # add initial state
        states_visited = [board] #dont requeue states (states are boards stringified)

        while len(self.frontier):
            #pop from List and create state
            self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
            state_tuple = self.frontier.pop(0)
            state = State(state_tuple)
            self.nodes_expanded += 1
            self.max_search_depth = max(self.max_search_depth, len(state_tuple[1]) + 1)
            states_visited.append(state_tuple[0])
            #print "State Board:", state.board.board
            #print "State Path:", state.path

            #decide if new board solves problem
            if state.board.is_complete():
                self.solution = state
                break

            #queue neighbor states, if applicable
            for move in 'UDLR':
                if state.board.move_allowed(move):
                    next_state = (state.board.get_board_after_move(move), state.path + move)
                    if next_state[0] not in states_visited and next_state[0] not in self.frontier:
                        #print "Adding state to frontier:", next_state[0], move
                        self.frontier.append(next_state)
                    #else:
                        #print "Cant add move ({0}) for state ({1}):".format(move, next_state[0])
                #else:
                    #print "Move not allowed ({0}) for state ({1}):".format(move, state_tuple[0])

    def solve_dfs(self, board):
        self.frontier.append((board, '')) # add initial state
        states_visited = [] #dont requeue states (states are boards stringified)

        while len(self.frontier):
            #pop from List and create state
            self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
            state_tuple = self.frontier.pop()
            state = State(state_tuple)
            states_visited.append(state_tuple[0])

            self.nodes_expanded += 1
            self.max_search_depth = max(self.max_search_depth, len(state_tuple[1]))
            #print "State Board:", state.board.board
            #print "State Path:", state.path

            #decide if new board solves problem
            if state.board.is_complete():
                self.solution = state
                break

            #queue neighbor states, if applicable
            for move in 'RLDU':
                if state.board.move_allowed(move):
                    next_state = (state.board.get_board_after_move(move), state.path + move)
                    if next_state[0] not in states_visited and next_state[0] not in self.frontier:
                        #print "Adding state to frontier:", next_state[0], move
                        self.frontier.append(next_state)
                    #else:
                        #print "Cant add move ({0}) for state ({1}):".format(move, next_state[0])
                #else:
                    #print "Move not allowed ({0}) for state ({1}):".format(move, state_tuple[0])

    """
    Comes with the benefit that states will always have same scores for priority queue
    This means that we don't need to worry about updates, just duplicates
    """
    def solve_ast(self, board):
        frontier_map = {} # to avoid keeping track of tuples
        frontier_map[board] = 0
        heapq.heappush(self.frontier, (0, board, ''))
        states_visited = []

        while len(self.frontier):
            self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
            state_tuple = heapq.heappop(self.frontier)
            state = State(state_tuple[1:])
            states_visited.append(state_tuple[1])
            #print "State tuple:", state_tuple

            self.nodes_expanded += 1
            self.max_search_depth = max(self.max_search_depth, len(state_tuple[2]))

            #print "State Board:", state.board.board
            #print "State Path:", state.path

            #decide if new board solves problem
            if state.board.is_complete():
                self.solution = state
                break

            #queue neighbor states, if applicable
            for move in 'UDLR':
                if state.board.move_allowed(move):
                    next_board = state.board.get_board_after_move(move)
                    board = Board(next_board)
                    next_state = (board.get_municipal_priority(), next_board, state.path + move)
                    if next_board not in states_visited and next_board not in frontier_map:
                        #print "Adding state to frontier:", next_state[0], move
                        self.frontier.append(next_state)
                        states_visited.append(next_state[0])
                    #else:
                        #print "Cant add move ({0}) for state ({1}):".format(move, next_board)
                #else:
                    #print "Move not allowed ({0}) for state ({1}):".format(move, state_tuple[1])

    def solve_ida(self, board):
        frontier_map = {} # to avoid keeping track of tuples
        frontier_map[board] = 0
        heapq.heappush(self.frontier, (0, board, ''))
        states_visited = []

        while len(self.frontier):
            self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
            state_tuple = heapq.heappop(self.frontier)
            state = State(state_tuple[1:])
            states_visited.append(state_tuple[1])
            #print "State tuple:", state_tuple

            self.nodes_expanded += 1
            self.max_search_depth = max(self.max_search_depth, len(state_tuple[2]))

            #print "State Board:", state.board.board
            #print "State Path:", state.path

            #decide if new board solves problem
            if state.board.is_complete():
                self.solution = state
                break

            #queue neighbor states, if applicable
            for move in 'RLDU':
                if state.board.move_allowed(move):
                    next_board = state.board.get_board_after_move(move)
                    board = Board(next_board)

                    #same as ast, but uses 100* as cost for longer paths
                    next_state = (board.get_municipal_priority() + (100 * len(state.path)), next_board, state.path + move)
                    if next_board not in states_visited and next_board not in frontier_map:
                        #print "Adding state to frontier:", next_state[0], move
                        self.frontier.append(next_state)
                        states_visited.append(next_state[0])
                    #else:
                        #print "Cant add move ({0}) for state ({1}):".format(move, next_board)
                #else:
                    #print "Move not allowed ({0}) for state ({1}):".format(move, state_tuple[1])


    def output(self):
        if self.solution == False:
            raise RuntimeError('Unable to complete given board')

        output = [
         'path_to_goal: ' + self.solution.get_path(),
         'cost_of_path: ' + str(len(self.solution.path)),
         'nodes_expanded: ' + str(self.nodes_expanded - 1),
         'search_depth: ' + str(len(self.solution.path)),
         'max_search_depth: ' + str(self.max_search_depth),
         'running_time: ' + str(time.clock() - self.time_started),
         'max_ram_usage:' + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/ 1000000.0)
        ]

        target = open('output.txt', 'w')
        target.truncate()
        target.write('\n'.join(output) + "\n")


if __name__ == "__main__":
    main()
