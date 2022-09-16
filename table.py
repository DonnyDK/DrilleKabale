import random

from player import Player


class Table(object):

    def __init__(self, names, deck):
        self.names = names
        self.players = self.add_players()
        self.fields = []
        self.usedCards = []
        self.deck = deck
        self.ids = []
        self.build()
        self.running = False

    def add_players(self):
        new_players = {}
        for i in self.names:
            new_players[int(i[1])] = Player(i[0], i[1])

        return new_players

    def ides(self):
        ids = []
        for player in self.players:
            ids.append(player)
            self.ids = ids

        turn = random.choice(self.ids)
        self.players[turn].hasTurn = True
        self.draw(turn, 5)

    def build(self):

        # Build table stacks
        for _ in self.players:
            for _ in range(4):
                self.fields.append([])

        # Build deck.
        self.deck.shuffle()

        # Build player stacks
        for j, player in enumerate(self.players.values()):
            for i in range(15):
                player.stack.append(self.deck.deal())

    def draw(self, player, num=1):

        while len(self.players[player].hand) < num:

            card = self.deck.deal()

            if card.value < 13:
                self.players[player].hand.append(card)
            else:
                self.players[player].jokers.append(card)

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

    def showFields(self):
        count = 1
        for i in self.fields:
            print(f'Field {count}: {i}')
            count += 1

        return self

    def show_stacks(self, name2):
        names = []
        stacks = []

        for i in self.players.values():
            if not i.name == name2:
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

    def from_hand(self, player, dist, source, local):

        card = player.stack.pop(source - 1)

        if dist == 'table':
            if not self.addToField(local - 1, card):
                player.hand.insert(source - 1, card)
        elif dist == 'stack':
            pass
        elif dist == 'buffer':
            pass

    def return_card(self, ide, card, src):
        self.players[ide].hand.insert(src - 1, card)

    # noinspection PyUnboundLocalVariable
    def next(self, ide):
        count = 0

        for player in self.players.values():

            if player.hasTurn:
                next_player = count + 1
                break
            count += 1

        self.players[ide].hasTurn = False

        while True:
            try:
                self.players[self.ids[next_player]].hasTurn = True
                self.draw(self.ids[next_player], 5)
                break
            except IndexError:
                next_player = 0

    def move(self, ide, data):

        source, src, dest, augment, ID = data

        if not self.players[ide].hasTurn:
            return False

        # #### Playing
        #self.draw(self.players[ide].id, 5)
        # Play from hand
        if source == 1:
            card = self.players[ID].hand.pop(src - 1)

            if dest == 1:
                if not self.addToField(augment - 1, card):
                    self.return_card(ide, card, src)

            if dest == 2:
                if ide in self.players.values():
                    for i in self.players.values():
                        if i.name == augment:
                            if not self.add_to_player_stack(card, augment):
                                self.return_card(ide, card, src)
                else:
                    self.return_card(ide, card, src)

            if dest == 3:
                self.players[ID].buffer[int(augment) - 1].append(card)
                self.next(ide)

            if len(self.players[ide].hand) < 1:
                self.draw(self.players[ide].id, 5)

        # Play from Joker
        if source == 2:
            card = self.players[ide].jokers.pop()
            if not self.addToField(augment - 1, card):
                self.players[ide].jokers.append(card)


        # Play from buffer
        if source == 3:
            card = self.players[ide].buffer[int(dest) - 1].pop()
            if not self.addToField(augment - 1, card):
                self.players[ide].buffer[int(dest) - 1].append(card)

        # Play from stack
        if source == 4:
            card = self.players[ide].stack.pop()
            if dest == 1:
                if not self.addToField(augment - 1, card):
                    self.players[ide].stack.append(card)

            if dest == 2:
                for i in self.players.values():
                    if i.name == augment:
                        if not self.add_to_player_stack(card, augment):
                            self.players[ide].stack.append(card)
