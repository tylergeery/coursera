class Domain:
    def __init__(self, board):
        self.domains = []
        self.board = board

        for i in range(81):
            if self.board.getValue(i):
                self.domains.append([self.board.getValue(i)])
            else:
                self.domains.append(self.board.getAvailableValues(i))

    def getDomainValues(self, pos):
        return self.domains[pos]

    def removeValue(self, pos, value):
        self.domains[pos].remove(value)
