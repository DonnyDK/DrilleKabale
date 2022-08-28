from card import Card
import random

class Deck(object):
    def __init__(self, decks=1):
        self.cards = []
        self.decks = decks
        self.build(self.decks)

    def show(self, leng=False):

        if leng:
            print(int(len(self.cards)))
        else:
            for card in self.cards:
                print(card.show())

    def build(self, decs=1):
        self.cards = []
        self.decks = decs
        for i in range(decs):
            for suit in ['C', 'S', 'D', 'H']:
                for val in range(1, 15):
                    self.cards.append(Card(suit, val))

    def shuffle(self, num=1):
        length = len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length - 1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
            # You can also use the build in shuffle method
            # random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()
