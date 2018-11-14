import random
from itertools import product
import logging
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Cell(ButtonBehavior, Image):
    BOMB_NUMBER = -1
    BOMB_PRESSED = False

    def __init__(self, line, column, board, number=0):
        # num = -1  is a bomb in the cell , if not the number in the cell is the number of the bombs around the cell.

        ButtonBehavior.__init__(self)
        Image.__init__(self)
        self.row = line
        self.board = board
        self.column = column
        self.number = number
        normal = 'dolphin.png'
        bomb = 'bomb.jpg'
        self.source = normal
        self.pressed = False

    def is_bomb(self):
        return self.number == self.BOMB_NUMBER

    def expose(self):
        if self.pressed:
            return
        if self.is_bomb():
            self.source = 'bomb.jpg'
            self.__class__.BOMB_PRESSED = True
        else:
            self.source = 'numbers\{}.png'.format(self.number)
            for row, column in self.board.surrounding_cells(self):
                if self.board.board[row][column].number == 0:
                    self.board.board[row][column].expose()

    def on_press(self):
        if self.BOMB_PRESSED or self.pressed:
            return
        logging.info('{}, {} pressed - number {}'.format(self.row, self.column, self.number))
        if self.is_bomb():
            self.board.end_game_lost()
            self.__class__.BOMB_PRESSED = True
        self.pressed = True
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
        # for i in self.board:
        #   self.add_widget(i)#add the cells on the board (the View board)'''
        self.number_of_bombs_label = Label(text='number of bombs {}'.format(self.bombs), font_size='20sp')
        self.add_widget(self.number_of_bombs_label)

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
            # for inner_row, inner_column in product(range(self.cols), range(self.cols)):
            current_cell = self.board[row][column]
            if current_cell.is_bomb():
                for inner_row, inner_column in self.surrounding_cells(current_cell):
                    self.board[inner_row][inner_column].number += 1

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
        for row, column in product(range(self.cols), range(self.cols)):
            self.board[row][column].expose()
        self.add_widget(Label(text='{}{}'.format(' ' * 50, message), font_size='50sp'))
        self.remove_widget(self.number_of_bombs_label)


class TestApp(App):
    def build(self):
        self.title = 'Minesweeper'
        return Board()


if __name__ == '__main__':
    TestApp().run()
