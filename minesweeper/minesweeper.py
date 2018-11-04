import random
from itertools import product

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Cell(ButtonBehavior, Image):
    def __init__(self, line, column, number=0):
        # num = -1  is a bomb in the cell , if not the number in the cell is the number of the bombs around the cell.

        ButtonBehavior.__init__(self)
        Image.__init__(self)
        line = line
        hidden = True
        column = column
        number = number
        normal = 'dolphin.png'
        bomb = 'bomb.jpg'
        self.source = normal

    def on_press(self):
        print "love"
        self.source = 'bomb.jpg'


class Board(GridLayout):
    def __init__(self, number_of_lines=10):
        # constructor of the board
        super(Board, self).__init__()
        self.bombs = 0  # count how many bombs R in the Board .
        self.counters = 0  # counting the num of bombs to tell later to the player
        self.cols = number_of_lines  # number of columns in the gridLayout
        self.board = list()  # all the cells in the board

        self.random_bombs()  # choose the bombs in the game
        # for i in self.board:
        #   self.add_widget(i)#add the cells on the board (the View board)'''
        l = Label(text='num bombs', font_size='20sp')
        l1 = Label(text=str(self.bombs), font_size='20sp')
        self.add_widget(l)
        self.add_widget(l1)

    def random_bombs(self):  # we have written this but the students won't get this
        for row, column in product(range(self.cols), range(self.cols)):
            if random.randint(0, 6) == 1:  # statistics of bombs
                cell = Cell(row, column, -1)
                # self.bind(on_press=self.change_cell(cell))
                self.bombs += 1
            else:
                cell = Cell(row, column)
                # self.bind(on_press=self.change_cell(cell))
            self.board.append(cell)
            self.add_widget(cell)

    def change_cell(self, cell):
        print "Hello, World!"
        # cell.num = 1000

    def changeNumInCell(self):
        """Needs to check what is the number that suppose to be in the cell"""
        pass


class TestApp(App):
    def build(self):
        self.title = 'based graphics'
        return Board()


if __name__ == '__main__':
    TestApp().run()
