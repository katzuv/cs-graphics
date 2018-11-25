import logging
import random
from itertools import product

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Cell(ButtonBehavior, Image):
    """Class representing a Minesweeper cell."""
    BOMB_NUMBER = -1

    def __init__(self, line, column, board, number=0):
        """
        Instantiate a Minesweeper cell.
        :param line: line of the cell
        :type line: int
        :param column: column of the cell
        :type column: int
        :param board: the board
        :type board: Board
        :param number: number inside the cell
        :type number: int
        """
        # num = -1  is a bomb in the cell , if not the number in the cell is the number of the bombs around the cell.
        super(Cell, self).__init__()
        self.row = line
        self.board = board
        self.column = column
        self.number = number
        self.source = 'dolphin.png'
        self._exposed = False

    def is_bomb(self):
        """
        :return: whether the cell is a bomb
        :rtype: bool
        """
        return self.number == self.BOMB_NUMBER

    def expose(self):
        """Expose the cell, and its neighbors if needed."""
        if self._exposed:
            return
        self._exposed = True
        self.board.increase_exposed()
        self.source = 'match_match\{}.png'.format(self.number)

        self.board.update_info_label()

        if self.number == 0:  # expose neighbors
            for cell in self.board.surrounding_cells(self):
                if not cell.is_bomb():
                    cell._invert_card()

    def on_press(self):
        if self.board.game_over or self._exposed:
            return
        logging.info('{}, {} pressed - number {}'.format(self.row, self.column, self.number))

        if self.is_bomb():
            self.board.bomb_pressed()
            return

        self.expose()

        self.board.check_win()


class Board(GridLayout):
    """Class representing a Minesweeper board."""

    def __init__(self, number_of_lines=10):
        # constructor of the board
        super(Board, self).__init__()
        self.bombs = 0  # count how many bombs R in the Board .
        self.cols = number_of_lines  # number of columns in the gridLayout
        self.board = [[None] * self.cols for _ in xrange(self.cols)]  # all the cells in the board
        self._exposed = 0
        self.game_over = False

        self.insert_bombs()  # choose the bombs in the game
        self._insert_numbers()
        self.info_label = Label(
            text='{} bombs {} exposed {} unexposed'.format(30 * ' ' + str(self.bombs), self._exposed,
                                                           self.cols ** 2 - self._exposed),
            font_size='20sp')
        self.add_widget(self.info_label)

    def insert_bombs(self):  # we have written this but the students won't get this
        """Insert bombs inside the board."""
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            if random.randint(0, 6) == 1:  # statistics of bombs
                cell = Cell(row, column, self, -1)
                self.bombs += 1
            else:
                cell = Cell(row, column, self)
            self.board[row][column] = cell
            self.add_widget(cell)

    def _insert_numbers(self):
        """Insert the match_match of the cells which are not bombs."""
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            cell = self.board[row][column]
            if cell.is_bomb():
                for current_cell in self.surrounding_cells(cell):
                    if not current_cell.is_bomb():
                        current_cell.number += 1

    def surrounding_cells(self, cell):
        """
        :param cell: the cell to find its surroundings
        :type cell: Cell
        :return: a list of the indices of the surrounding cells of :cell:
        :rtype: list
        """
        start_row = max(0, cell.row - 1)
        end_row = min(self.cols, cell.row + 2)
        start_column = max(0, cell.column - 1)
        end_column = min(self.cols, cell.column + 2)
        return [self.board[row][column]
                for row, column in product(xrange(start_row, end_row), xrange(start_column, end_column))
                if (row, column) != (cell.row, cell.column)]

    def update_info_label(self):
        """Update the information label, which contains amounts of bombs, exposed and unexposed cells."""
        self.info_label.text = '{} bombs {} exposed {} unexposed'.format(30 * ' ' + str(self.bombs), self._exposed,
                                                                         self.cols ** 2 - self._exposed)

    def increase_exposed(self):
        """Increase the number of exposed cells."""
        self._exposed += 1

    def bomb_pressed(self):
        self._end_game('GAME OVER :(')

    def check_win(self):
        """Print the game has ended if a win occurred."""
        if self.bombs == self.cols ** 2 - self._exposed:
            self._end_game('YOU WON :)')

    def _end_game(self, message):
        """Expose all the cells in the board and print the message."""
        self.game_over = True
        self._expose_all_cells()
        self.info_label.text = message

    def _expose_all_cells(self):
        """Expose all the cells in the board."""
        for row, column in product(xrange(self.cols), xrange(self.cols)):
            self.board[row][column].expose()


class TestApp(App):
    def build(self):
        self.title = 'Minesweeper'
        return Board(6)


if __name__ == '__main__':
    TestApp().run()
