class Domain:
    def __init__(self, board):
        self.domains = []
        self.board = board

        for i in range(81):
            self.domains.append([])
            self.updateDomainValues(i)

    def getDomainValues(self, pos):
        """
        Get possible domain values for a variable
        Returns: array ints
        """
        return self.domains[pos]

    def removeValue(self, pos, value):
        """
        Remove a value from the domain possiblities for a variable
        """
        self.domains[pos].remove(value)

    def getOpenPos(self):
        """
        Get the first open pos on a board
        Use minimum remaining values as a heuristic

        Returns: int
        """
        for i in range(1, 10):
            for j in range(81):
                if self.board.getValue(j) != 0:
                    continue;

                if len(self.domains[j]) == i:
                    return j

        return -1

    def updateDomainValues(self, pos):
        """
        Updates the allowable domain values for a given pos
        """
        if self.board.getValue(pos) == 0:
            self.domains[pos] = self.board.getAvailableValues(pos)
        else:
            self.domains[pos] = [self.board.getValue(pos)]

    def updateNeighbors(self, pos):
        """
        Updates all neighboring area domain values after assignment
        """
        row_start = self.board.getRowStart(pos)
        col_start = self.board.getColumnStart(pos)
        sq_start = self.board.getSquareStart(pos)

        for i in range(9):
            neighbor_in_row = row_start + i
            neighbor_in_col = col_start + 9*i

            self.updateDomainValues(neighbor_in_row)
            self.updateDomainValues(neighbor_in_col)

        for offset in [0,1,2,9,10,11,18,19,20]:
            neighbor_in_sq = sq_start + offset

            self.updateDomainValues(neighbor_in_sq)
