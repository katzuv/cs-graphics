from copy import deepcopy
from random import shuffle

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


class Card(ButtonBehavior, Image):
    def __init__(self, number, board):
        super(Card, self).__init__()
        self.number = number
        self.board = board

        self._exposed = True
        self._invert_card()
        self.solved = False

    # def __repr__(self):
    #     return '{}(number={})'.format(self.__class__.__name__, self.number)

    def _invert_card(self):
        self._exposed = not self._exposed
        if self._exposed:
            self.source = 'match_match\\{}.png'.format(self.number)
        else:
            self.source = 'match_match\\9.png'

    def on_press(self):
        if self.solved:
            return
        self.board.tries += 1
        if self.board.card_revealed.number == self.number:
            self.solved = True
            self.board.card_revealed.solved = True


class Board(GridLayout):
    def __init__(self):
        super(Board, self).__init__()
        self.cols = 4

        cards = [Card(number, self) for number in xrange(1, 9)]
        cards.extend(deepcopy(cards))
        shuffle(cards)
        for card in cards:
            self.add_widget(card)
        self.exposed_card = None
        self.tries = 0


class MatchMatch(App):
    def build(self):
        return Board()


if __name__ == '__main__':
    MatchMatch().run()
