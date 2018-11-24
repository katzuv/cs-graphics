from itertools import product

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


class Cell(ButtonBehavior, Image):
    def __init__(self, line, column, num):
        super(Cell, self).__init__()
        self.line = line
        self.column = column
        self.options = set(xrange(1, 7))
        self.number = num


class Board(GridLayout):
    def __init__(self, columns=9):
        """Instantiate a Sudoku board with 6 * 6 cells."""
        # 0 represent unknown
        super(Board, self).__init__()
        self.problem = [[0, 3, 0, 0, 0, 0], [0, 0, 5, 0, 2, 1], [0, 0, 1, 0, 6, 0], [0, 6, 0, 5, 0, 0],
                        [5, 1, 0, 6, 0, 0], [0, 0, 0, 0, 3, 0]]
        self.cols = columns
        self.rows = [[Cell(row, column, self.problem[row - 1][column - 1])] for row, column in
                     product(xrange(1, self.cols + 1), xrange(1, self.cols + 1))]
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            self.add_widget(self.rows[row][column])

    def find_first_empty(self):
        """Return the first cell which is empty, or None if all cells are filled."""
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            cell = self.rows[row][column]
            if cell.number == 0:
                return cell

    def possible_placing(self, cell):
        """Check whether the last option the algorithm placed match Sudoku in the line in the column and in the
        square. """
        op_in_same_line = list()
        op_in_same_column = list()
        op_in_same_square = list()
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            current_cell = self.rows[row][column]
            if current_cell.line == cell.line and row.number != 0:
                op_in_same_line = op_in_same_line + [current_cell.number]
            if current_cell.column == cell.column and row.number != 0:
                op_in_same_column = op_in_same_column + [current_cell.number]
            if ((current_cell.line - 1) / 2 == (cell.line - 1) / 2) and (
                    (current_cell.column - 1) / 3 == (current_cell.column - 1) / 3) and current_cell.number != 0:
                op_in_same_square = op_in_same_square + [current_cell.number]
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
        """Print every cell in new line number if known and list of possibilities if unknown."""
        for i in xrange(1, 7):
            for cell in self.rows:
                if cell.line == i:
                    print (cell.line, cell.column),
                    if cell.number != 0:
                        print cell.number
                    else:
                        print list(cell.options), " "

    def print_solution(self):
        for i, x in enumerate(self.rows):
            print x.number,
            if (i + 1) % 6 == 0:
                print


class TestApp(App):
    def build(self):
        self.title = 'Sudoku'
        return Board(6)


if __name__ == '__main__':
    TestApp().run()
    # a = Board()
    # a.print_sudoku()
    # a.brute_force()
    # a.print_solution()
