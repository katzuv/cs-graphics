import logging
import random
from itertools import product

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Cell(ButtonBehavior, Image):
    BOMB_NUMBER = -1
    GAME_OVER = False

    def __init__(self, line, column, board, number=0):
        # num = -1  is a bomb in the cell , if not the number in the cell is the number of the bombs around the cell.

        ButtonBehavior.__init__(self)
        Image.__init__(self)
        self.row = line
        self.board = board
        self.column = column
        self.number = number
        self.source = 'dolphin.png'
        self._pressed = False

    def is_bomb(self):
        return self.number == self.BOMB_NUMBER

    def expose(self):
        if self.board.exposed == self.board.cols ** 2 - self.board.bombs:
            self.board.end_game('YOU WON! :)')
        if self._pressed:
            return
        if self.is_bomb():
            self.source = '-1.png'
            self._pressed = True
            self.__class__.GAME_OVER = True
            return

        self.source = 'numbers\{}.png'.format(self.number)
        self._pressed = True
        self.board.exposed += 1
        self.board.update_info_label()

        if self.number == 0:
            for row, column in self.board.surrounding_cells(self):
                cell = self.board.board[row][column]
                if cell.number == 0:
                    cell.expose()
                elif not cell.is_bomb():
                    cell.source = 'numbers\{}.png'.format(cell.number)
                    cell.pressed = True
                    self.board.exposed += 1
        self.board.update_info_label()

    def on_press(self):
        if self.GAME_OVER or self._pressed:
            return
        logging.info('{}, {} pressed - number {}'.format(self.row, self.column, self.number))
        if self.is_bomb():
            self.board.end_game('GAME OVER :(')
            self.__class__.GAME_OVER = True
        else:
            self.expose()


class Board(GridLayout):
    def __init__(self, number_of_lines=10):
        # constructor of the board
        super(Board, self).__init__()
        self.bombs = 0  # count how many bombs R in the Board .
        self.counters = 0  # counting the num of bombs to tell later to the player
        self.cols = number_of_lines  # number of columns in the gridLayout
        self.board = [[None] * self.cols for _ in range(self.cols)]  # all the cells in the board
        self.exposed = 0

        self.insert_bombs()  # choose the bombs in the game
        self.insert_numbers()
        self.info_label = Label(
            text='{} bombs {} exposed {} unexposed'.format(30 * ' ' + str(self.bombs), self.exposed,
                                                           self.cols ** 2 - self.exposed),
            font_size='20sp')
        self.add_widget(self.info_label)

    def insert_bombs(self):  # we have written this but the students won't get this
        """Insert bombs inside the board."""
        for row, column in product(range(self.cols), range(self.cols)):
            if random.randint(0, 6) == 1:  # statistics of bombs
                cell = Cell(row, column, self, -1)
                # self.bind(on_press=self.change_cell(cell))
                self.bombs += 1
            else:
                cell = Cell(row, column, self)
                # self.bind(on_press=self.change_cell(cell))
            self.board[row][column] = cell
            self.add_widget(cell)

    def insert_numbers(self):
        """Insert the numbers of the cells which are not bombs."""
        for row, column in product(range(self.cols), range(self.cols)):
            cell = self.board[row][column]
            if cell.is_bomb():
                for inner_row, inner_column in self.surrounding_cells(cell):
                    current_cell = self.board[inner_row][inner_column]
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
        temp = list(product(range(start_row, end_row), range(start_column, end_column)))
        temp.remove((cell.row, cell.column))
        return temp

    def end_game(self, message):
        """
        Expose all the cells in the board and print the message.
        :param message: message to print on the board
        :type message: str
        """
        self._expose_all_cells()
        self.add_widget(Label(text='{}{}'.format(' ' * 50, message), font_size='50sp'))
        # self.remove_widget(self.info_label)

    def update_info_label(self):
        """Update the information label, which contains amounts of bombs, exposed and unexposed cells."""
        self.info_label.text = '{} bombs {} exposed {} unexposed'.format(30 * ' ' + str(self.bombs), self.exposed,
                                                                         self.cols ** 2 - self.exposed)

    def _expose_all_cells(self):
        """Expose all the cells in the board."""
        Cell.GAME_OVER = True
        for row, column in product(range(self.cols), range(self.cols)):
            current_cell = self.board[row][column]
            current_cell.source = 'numbers\{}.png'.format(current_cell.number)


class TestApp(App):
    def build(self):
        self.title = 'Minesweeper'
        return Board()


if __name__ == '__main__':
    TestApp().run()
