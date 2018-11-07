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

    def __init__(self, line, column, number=0):
        # num = -1  is a bomb in the cell , if not the number in the cell is the number of the bombs around the cell.

        ButtonBehavior.__init__(self)
        Image.__init__(self)
        self.row = line
        hidden = True
        self.column = column
        self.number = number
        normal = 'dolphin.png'
        bomb = 'bomb.jpg'
        self.source = normal

    def is_bomb(self):
        return self.number == self.BOMB_NUMBER

    def on_press(self):
        if self.BOMB_PRESSED:
            return
        logging.info('{}, {} pressed - number {}'.format(self.row, self.column, self.number))
        if self.number == self.BOMB_NUMBER:
            self.source = 'bomb.jpg'
            self.BOMB_PRESSED = True
        else:
            self.source = 'numbers\{}.png'.format(self.number)


class Board(GridLayout):
    def __init__(self, number_of_lines=10):
        # constructor of the board
        super(Board, self).__init__()
        self.bombs = 0  # count how many bombs R in the Board .
        self.counters = 0  # counting the num of bombs to tell later to the player
        self.cols = number_of_lines  # number of columns in the gridLayout
        self.board = [[None] * self.cols for _ in range(self.cols)]  # all the cells in the board
        self.exposed = [[False] * self.cols for _ in range(self.cols)]

        self.insert_bombs()  # choose the bombs in the game
        self.insert_numbers()
        # for i in self.board:
        #   self.add_widget(i)#add the cells on the board (the View board)'''
        l = Label(text='num bombs', font_size='20sp')
        l1 = Label(text=str(self.bombs), font_size='20sp')
        self.add_widget(l)
        self.add_widget(l1)

    def insert_bombs(self):  # we have written this but the students won't get this
        for row, column in product(range(self.cols), range(self.cols)):
            if random.randint(0, 6) == 1:  # statistics of bombs
                cell = Cell(row, column, -1)
                # self.bind(on_press=self.change_cell(cell))
                self.bombs += 1
            else:
                cell = Cell(row, column)
                # self.bind(on_press=self.change_cell(cell))
            self.board[row][column] = cell
            self.add_widget(cell)

    def insert_numbers(self):
        for row, column in product(range(self.cols), range(self.cols)):
            # for inner_row, inner_column in product(range(self.cols), range(self.cols)):
            current_cell = self.board[row][column]
            if not current_cell.is_bomb():
                for inner_row, inner_column in product(range(max(0, current_cell.row), min(self.cols, current_cell.row + 3)),
                                                       range(max(0, current_cell.column), min(self.cols, current_cell.column + 3))):
                    if self.board[inner_row][inner_column].is_bomb():
                        current_cell.number += 1

    def change_cell(self, cell):
        print "Hello, World!"
        # cell.num = 1000

    def changeNumInCell(self):
        """Needs to check what is the number that suppose to be in the cell"""
        pass


class TestApp(App):
    def build(self):
        self.title = 'Minesweeper'
        return Board()


if __name__ == '__main__':
    try:
        TestApp().run()
    except SystemExit:
        print 'Game over :('
