
class Player(object):
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.jokers = []
        self.hand = []
        self.stack = []
        self.buffer = [[], [],[]]
        self.won = False
        self.hasTurn = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def showHand(self):
        return self.hand

    def showJoker(self, show=False):
        if show:
            return self.jokers
        else:
            return len(self.jokers)

    def showStack(self, show=False):
        if len(self.stack) > 0:
            if show:
                return self.stack
            else:
                return self.stack[-1]
        else:
            return 'Stack is empty.'

    def addToStack(self, card):

        top_card = self.stack[-1]
        if top_card.suit == card.suit and top_card.value == card.value - 1:
            self.stack.append(card)
            return True

        return False

    def checkWon(self):

        for i in self.buffer:
            if i:
                return False
        if self.stack:
            return False
        if self.jokers:
            return False

        return True