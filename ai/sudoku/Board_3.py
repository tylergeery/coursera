import math

class Board:
    def __init__(self, board):
        self.board = board

    def copy(self):
        """
        Gets a copy of this board
        Returns: Board
        """
        return Board(self.board)

    def getAsString(self):
        """
        Gets the board representation as a string
        Returns: string
        """
        return ''.join(map(str, self.board))

    def valid(self, arr):
        """
        Returns whether a given arr has integers 1-10
        this deems it it a valid square/row/column
        """
        for i in range(1,10):
            if i not in arr:
                return False

        return True

    def getAvailableValues(self, pos):
        """
        Controls all game constraints
        Will ensure no duplicates in square/row/column
        """
        available = []
        col_vals = self.getColumn(pos)
        row_vals = self.getRow(pos)
        sq_vals = self.getSquare(pos)

        for i in range(1, 10):
            if i in col_vals:
                continue
            if i in row_vals:
                continue
            if i in sq_vals:
                continue

            # value passes all constraints
            available.append(i)

        return available

    def getColumnStart(self, pos):
        """
        Gets the top most position for the column of given pos
        Returns: int
        """
        return pos % 9

    def getColumn(self, pos):
        """
        Gets the column values for a given position (pos)
        Returns: array
        """
        col_start = self.getColumnStart(pos)

        return list(map(lambda x: self.board[x + col_start], range(0, 81, 9)))

    def getRowStart(self, pos):
        """
        Gets the left most (row beginning) position for a given pos
        Returns: int
        """
        return int(math.floor(pos/9) * 9)

    def getRow(self, pos):
        """
        Get the row values for a given position (pos)
        Returns: array
        """
        row_start = self.getRowStart(pos)

        return list(map(lambda x: self.board[row_start + x], range(9)))

    def getSquareStart(self, pos):
        """
        Gets the top left position of the given 3x3 square for provided pos
        Returns: int
        """
        row = math.floor(pos/9)
        col = pos % 9

        return int(9 * (row - (row % 3))) + (col - (col % 3))

    def getSquare(self, pos):
        """
        Get the square values for a given position (pos)
        Returns: array
        """
        square_start = self.getSquareStart(pos)

        return list(map(lambda x: self.board[square_start + x], [0, 1, 2, 9, 10, 11, 18, 19, 20]))

    def getValue(self, pos):
        """
        Get the value at a position on the board
        """
        return self.board[pos]

    def setValue(self, pos, value):
        """
        Set a pos on the board to a given value
        """
        self.board[pos] = value

    def pretty(self):
        """
        Print a pretty version of the sudoku board
        """
        for i in range(9):
            if i % 3 == 0:
                print('           ')

            row_str = ''
            for j in range(9):
                if j % 3 == 0:
                    row_str += '|'
                row_str += str(self.board[i*9 + j])
            row_str += '|'

            print(row_str.replace('0', ' '))
        print('           ')

    def solved(self):
        """
        Is the current board state solved?
        Returns: bool
        """
        for i in range(9):
            # go through horizontals
            if not self.valid(self.getRow(i*9)):
                return False

            # go through verticals
            if not self.valid(self.getColumn(i)):
                return False

            # go through each square
            if not self.valid(self.getSquare(i * 9 + (i % 3) * 3)):
                return False

        return True

    def getHeuristic(self):
        """
        What is the current value of the board?
        Heuristic: spaces filled out
        """
        value = len(self.board)

        for i in self.board:
            if int(i) == 0:
                value -= 1

        return value
