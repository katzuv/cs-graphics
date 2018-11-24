class Cell:
    def __init__(self, line, column, num):
        self.line = line
        self.column = column
        self.options = set(xrange(1, 7))
        self.number = num


class Board:
    def __init__(self):
        """Instantiate a Sudoku board with 6 * 6 cells."""
        # 0 represent unknown
        self.problem = [[0, 3, 0, 0, 0, 0], [0, 0, 5, 0, 2, 1], [0, 0, 1, 0, 6, 0], [0, 6, 0, 5, 0, 0],
                        [5, 1, 0, 6, 0, 0], [0, 0, 0, 0, 3, 0]]
        self.board = [Cell(i, j, self.problem[i - 1][j - 1]) for i in xrange(1, 7) for j in xrange(1, 7)]

    def find_first_empty(self):
        """Return the first cell which is unknown."""
        for cell in self.board:
            if cell.number == 0:
                return cell

    ''' check if the last opthion the algoritm placed match soduko in the line in the colom and in the square'''

    def possible_placing(self, cell):
        """Check whether the last option the algorithm placed match Sudoku in the line in the column and in the
        square. """
        op_in_same_line = list()
        op_in_same_column = list()
        op_in_same_square = list()
        for x in self.board:
            if x.line == cell.line and x.number != 0:
                op_in_same_line = op_in_same_line + [x.number]
            if x.column == cell.column and x.number != 0:
                op_in_same_column = op_in_same_column + [x.number]
            if ((x.line - 1) / 2 == (cell.line - 1) / 2) and (
                    (x.column - 1) / 3 == (cell.column - 1) / 3) and x.number != 0:
                op_in_same_square = op_in_same_square + [x.number]
        if op_in_same_square.count(cell.number) != 1:
            return False
        if op_in_same_line.count(cell.number) != 1:
            return False
        if op_in_same_column.count(cell.number) != 1:
            return False
        return True

    def brute_force(self):
        cell = self.find_first_empty()
        if cell:
            return True
        for option in cell.options:
            cell.number = option
            if self.possible_placing(cell):
                if self.brute_force():
                    return True
            cell.number = 0
        return False

    def print_sudoku(self):
        """Print every cell in new line number if known and list of possibilities if unknown"""
        for i in xrange(1, 7):
            for cell in self.board:
                if cell.line == i:
                    print (cell.line, cell.column),
                    if cell.number != 0:
                        print cell.number
                    else:
                        print list(cell.options), " "

    def print_solution(self):
        for i, x in enumerate(self.board):
            print x.number,
            if (i + 1) % 6 == 0:
                print


if __name__ == '__main__':
    a = Board()
    a.print_sudoku()
    a.brute_force()
    a.print_solution()
