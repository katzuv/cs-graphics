import logging

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image


class Cell(Image):
    def __init__(self, row, column, number, x, y):
        super(Cell, self).__init__()
        self.row = row
        self.column = column
        self.number = number

        self.source = 'numbers\\0.png'
        self.x = x
        self.y = y


class Board(FloatLayout):
    def __init__(self):
        super(Board, self).__init__()
        self.background_color = (95, 0, 0),

        self.image1 = Image(source='minesweeper\\numbers\\4.png', x=100, y=100)
        self.image2 = Image(source='minesweeper\\numbers\\2.png', x=0, y=0)
        self.image3 = Image(source='minesweeper\\numbers\\3.png', x=200, y=200)

        self.image1.size_hint = (0.2, 0.2)
        self.image2.size_hint = (0.2, 0.2)
        self.image3.size_hint = (0.2, 0.2)

        self.add_widget(self.image1)
        self.add_widget(self.image2)
        self.add_widget(self.image3)

    @staticmethod
    def swap_images(image, new_source):
        image.source = new_source

    def on_touch_down(self, touch):
        if self.image1.collide_point(touch.x, touch.y):
            self.swap_images(self.image1, 'minesweeper\\numbers\\5.png')
        elif self.image2.collide_point(touch.x, touch.y):
            logging.info(2)
        elif self.image3.collide_point(touch.x, touch.y):
            logging.info(3)
        else:
            self.add_widget(Image(source='minesweeper\\numbers\\3.png', x=150, y=150))


class YourApp(App):
    def build(self):
        return Board()


if __name__ == '__main__':
    YourApp().run()
