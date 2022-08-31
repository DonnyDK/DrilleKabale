import random

from player import Player



class Table(object):

    def __init__(self, names, deck):
        self.names = names
        self.players = self.add_players()
        self.fields = []
        self.usedCards = []
        self.deck = deck
        self.build()
        self.running = False

    def add_players(self):
        new_players = {}
        for i in self.names:
            new_players[i[1]] = Player(i[0], i[1])

        return new_players

    def build(self):

        # Build table stacks
        for i in self.players:
            for _ in range(4):
                self.fields.append([])

        # Build deck.
        self.deck.shuffle()

        turn = random.randint(0, len(self.players.values()) - 1)
        print(turn)
        # Build player stacks
        for j, player in enumerate(self.players.values()):
            for i in range(15):
                player.stack.append(self.deck.deal())

            if j == turn:
                player.hasTurn = True




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

        for i in self.players.values():
            if not i.hasTurn:
                names.append(i.name)
                stacks.append(i.showStack())

        return names, stacks

    def add_to_player_stack(self, card, playerName):
        for player in self.players.values():
            if player.name == playerName:
                if card.suit == player.showStack().suit and card.value == player.showStack().value + 1:
                    player.stack.append(card)
                    return True
        return False