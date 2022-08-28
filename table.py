from player import Player
import time


class Table(object):

    def __init__(self, names, deck):
        self.names = names
        self.players = self.add_players()
        self.fields = []
        self.usedCards = []
        self.deck = deck
        self.build()

    def add_players(self):
        new_players = []
        for i in self.names:
            new_players.append(Player(i))
        return new_players

    def build(self):

        # Build table stacks
        for i in range(len(self.players * 4)):
            self.fields.append([])

        # Build deck.
        self.deck.shuffle()

        # Build player stacks
        for player in self.players:
            for i in range(15):
                player.stack.append(self.deck.deal())

    def draw(self, player, num=1):

        while len(player.hand) < num:

            card = self.deck.deal()

            if card.value < 13:
                player.hand.append(card)
            else:
                player.jokers.append(card)

        return True

    def checkField(self, field):
        if len(self.fields[field]) >= 12:
            self.usedCards = self.usedCards + self.fields[field]
            self.fields[field] = []

    def checkJoker(self, field, card):
        if card.isJoker:
            if len(self.fields[field]) == 0:
                return False
            if len(self.fields[field]) == 11:
                return False

            return True

        return False

    def addToField(self, field, card):

        if card.value == len(self.fields[field]) + 1 or self.checkJoker(field, card):
            self.fields[field].append(card)
            self.checkField(field)
            return True

        print('Wrong move!!')
        time.sleep(.5)
        return False

    # CLI ONLY
    def showFields(self):
        count = 1
        for i in self.fields:
            print(f'Field {count}: {i}' )
            count += 1

        return self

    def show_stacks(self):
        names = []
        stacks = []

        for i in self.players:
            if not i.hasTurn:
                names.append(i.name)
                stacks.append(i.showStack())

        return names, stacks

    def add_to_player_stack(self, card, playerName):
        for player in self.players:
            if player.name == playerName:
                if card.suit == player.showStack().suit and card.value == player.showStack().value + 1:
                    player.stack.append(card)
                    return True
        return False