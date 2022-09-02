import random

from player import Player

class Table(object):

    def __init__(self, names, deck):
        self.names = names
        self.players = self.add_players()
        self.ids = self.ids()
        self.fields = []
        self.usedCards = []
        self.deck = deck
        self.build()
        self.running = False

    def add_players(self):
        new_players = {}
        for i in self.names:
            new_players[int(i[1])] = Player(i[0], i[1])

        return new_players

    def ids(self):
        ids = []
        for player in self.players.values():
            ids.append(player.id)
            return ids

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

    # CLI ONLY
    def showFields(self):
        count = 1
        for i in self.fields:
            print(f'Field {count}: {i}' )
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

    def next(self, ide):
        self.players[ide].hasTurn = False
        for i, j in enumerate(self.ids):
            if j == ide:
                turn = i + 1

        try:
            next_player = self.ids[turn]
        except IndexError:
            next_player = self.ids[0]

        self.players[next_player].hasTurn = True
        self.draw(self.players[next_player].id, 5)

    def move(self, ide, data):

        source, src, dest, augment, ID = data
        source, src, dest, augment = int(source), int(src), int(dest), int(augment)

        if not self.players[ide].hasTurn:
            return False

        print(source, src, dest, augment)
        print(type(source), type(src), type(dest), type(augment), type(ide))
        print(self.players[ide].hand)
        ### Playing

        # Play from hand
        if source == 1:
            card = self.players[ide].hand.pop(src - 1)

            if dest == 1:

                if not self.addToField(augment - 1, card):
                    self.return_card(ide, card, src)

            if dest == 2:
                for i in self.players.values():
                    if i.name == augment:
                        if not self.add_to_player_stack(card, augment):
                            self.return_card(card, src)

            if dest == 3:
                self.players[ide].buffer[augment - 1].append(card)
                self.next(ide)

            if len(self.players[ide].hand) < 1:
                self.draw(self.players[ide], 5)

        # Play from Joker
        if source == 2:
            card = self.players[ide].jokers.pop()
            if not self.addToField(augment - 1, card):
                self.players[ide].jokers.append(card)

        # Play from buffer
        if source == 3:
            card = self.players[ide].buffer[dest - 1].pop()
            if not self.addToField(augment - 1, card):
                self.players[ide].buffer[dest].append(card)

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