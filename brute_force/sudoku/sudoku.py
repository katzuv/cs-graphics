import logging
from itertools import product

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Cell(ButtonBehavior, Image):
    def __init__(self, line, column, number, board):
        super(Cell, self).__init__()
        self.line = line
        self.column = column

        self.number = number
        self.options = range(1, 7)
        self.board = board

        self.update(number)

    def on_press(self):
        logging.info('Pressed')
        self.board.solve()

    def update(self, number):
        """
        Update the cell's number and image.
        :param number: number to change to
        :type number: int
        """
        logging.info('({}, {}) updated to {}'.format(self.line, self.column, number))
        self.number = number
        self.source = 'match_match/{}.png'.format(self.number)


class Board(GridLayout):
    def __init__(self, columns=6):
        """Instantiate a Sudoku board with 6 * 6 cells."""
        # 0 represent unknown
        super(Board, self).__init__()
        self.label = Label(text='{}Click anywhere to solve'.format(' ' * 93), font_size=30)
        self.initial_board = [[0, 3, 0, 0, 0, 0], [0, 0, 5, 0, 2, 1], [0, 0, 1, 0, 6, 0], [0, 6, 0, 5, 0, 0],
                              [5, 1, 0, 6, 0, 0], [0, 0, 0, 0, 3, 0]]
        self.cols = columns
        self.board = [[Cell(row, column, self.initial_board[row][column], self) for column in xrange(self.cols)] for row
                      in xrange(self.cols)]

        for row, column in product(xrange(self.cols), xrange(self.cols)):
            self.add_widget(self.board[row][column])
        self.add_widget(self.label)

    def _find_first_empty(self):
        """Return the first cell which is empty, or None if all cells are filled."""
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            cell = self.board[row][column]
            if cell.number == 0:
                return cell

    def _is_cell_location_valid(self, cell):
        """
        Check whether the location of :cell: is valid.

        The checking is done by checking the cell's number is not repeated in its row, column and box.
        """
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            if (row, column) == (cell.line, cell.column):
                continue
            current_cell = self.board[row][column]
            if current_cell.number == cell.number:
                if any((current_cell.line == cell.line,  # check if there are two identical match_match in a row
                        current_cell.column == cell.column,  # column
                        current_cell.line / 2 == cell.line / 2 and current_cell.column / 3 == cell.column / 3)):  # box
                    return False
        return True

    def solve(self):
        """Solve the game."""
        cell = self._find_first_empty()
        if cell is None:
            return True
        self.label.text = '{}Smarter than you!'.format(' ' * 93)
        for option in cell.options:
            cell.update(option)
            if self._is_cell_location_valid(cell):
                if self.solve():
                    return True
            cell.update(0)
        return False


class Sudoku(App):
    def build(self):
        self.title = 'Sudoku'
        return Board(6)


if __name__ == '__main__':
    Sudoku().run()
