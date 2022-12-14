import pygame as pg
import random
from table import Table
from deck import Deck


class Game:
    def __init__(self, ID, table):
        # Game essentials
        self.ID = ID
        self.table = table
        self.player = self.table.players[self.ID]

        # Game windows settings
        self.WIDTH = 900
        self.HEIGHT = self.WIDTH
        self.PAD = self.WIDTH / 180
        self.clock = pg.time.Clock()
        self.source = 0
        self.src = 0
        self.dest = 0
        self.augment = 0
        self.locations = []
        self.counter = 0


        # Game rule settings
        self.play_order = self.play_order_func()

        # Card settings
        self.CARD_WIDTH, self.CARD_HEIGHT = self.scale_relativ(self.WIDTH / 12, 1.452)
        self.CARD_X_PAD = int(self.CARD_WIDTH / 20)
        self.CARD_y_PAD = int(self.CARD_HEIGHT / 20)
        self.CARD_TUP = (self.CARD_WIDTH, self.CARD_HEIGHT)
        self.CARD_OVERLAY = self.CARD_HEIGHT / 9
        self.CARD_PADDING = int(self.CARD_WIDTH / 10)
        self.CARD_BACK = self.scaler('gfx/Back_Red_2.png', self.CARD_TUP)

        # Opponent area settings

        self.OPPONENT_AREA_WIDTH = (3 * self.CARD_WIDTH) + (4 * self.CARD_PADDING)

        self.OPPONENT_AREA_BUFFER_SIZE = 10
        self.OPPONENT_AREA_ICON_TUP = (self.OPPONENT_AREA_WIDTH / 5, self.OPPONENT_AREA_WIDTH / 5)

        # Table area settings
        self.TABLE_AREA_DECK_WIDTH = self.CARD_WIDTH + (2 * self.CARD_PADDING)
        self.TABLE_AREA_STACKS_WIDTH = self.WIDTH - self.TABLE_AREA_DECK_WIDTH
        self.TABLE_AREA_STACKS_SIDE_WIDTH = self.TABLE_AREA_STACKS_WIDTH / 2
        self.TABLE_AREA_STACKS_SIDE_DRAW_WIDTH = ((len(self.table.fields) / 4) * self.CARD_WIDTH) + ((len(self.table.fields) / 4) - 1) * self.CARD_PADDING
        self.TABLE_AREA_STACKS_SIDE_HEIGHT = (self.CARD_HEIGHT * 2) + self.CARD_PADDING


        # Player area settings
        self.PLAYER_AREA_BUFFER_STACKS_SIZE = self.OPPONENT_AREA_WIDTH = (self.CARD_WIDTH * 3) + (self.CARD_X_PAD * 4)
        self.PLAYER_AREA_BUFFER_SIZE = self.OPPONENT_AREA_BUFFER_SIZE
        self.PLAYER_AREA_HAND_AREA_SIZE = (5 * self.CARD_WIDTH) + (self.CARD_X_PAD * 6)

        # Hand area settings
        self.HAND_WIDTH = (5 * self.CARD_WIDTH) + (5 * self.CARD_PADDING)
        self.HAND_HEIGHT = self.CARD_HEIGHT + (2 * self.CARD_PADDING)

        # Window settings
        self.BG = self.scaler('gfx/wood1.png', (self.WIDTH, self.HEIGHT))
        self.main_window = self.define_window()


        # GFX Loading
        self.icons = self.load_icons()
        self.placeholder = self.scaler('gfx/placeholder.png', self.CARD_TUP)
        self.placeholder.set_alpha(100)
        self.numbers = self.load_numbers()
        self.cards = self.load_cards()

        for i in range(5):
            for player in self.play_order:
                data = (1, random.randint(1, 5), 3, random.randint(1, 3), player)
                #data = (1, random.randint(1, 5), 3, 2, player)

                if self.table.players[player].hasTurn:
                    #self.table.draw(self.table.players[player].id, 5)
                    self.table.move(player, data)




        self.main_loop()


    def play_order_func(self):
        play_order = list(self.table.players.keys())

        while not play_order[0] == self.ID:
            play_order.insert(0, play_order.pop())

        return play_order

    def scale_relativ(self, W, scale):
        H = W * scale
        return W, H

    def scaler(self, img, size, mul=1):
        n_size = [size[0] * mul, size[1] * mul]

        pic = pg.image.load(img)
        pic = pg.transform.scale(pic, tuple(n_size))
        return pic

    def load_numbers(self):
        numbers = {}
        for i in range(0, 9):
            numbers[i] = self.scaler(f'gfx/icon/{i}.png', self.OPPONENT_AREA_ICON_TUP)

        return numbers

    def load_cards(self):
        cards = {}

        for suit in ['C', 'S', 'D', 'H']:
            for val in range(1, 15):
                card = self.scaler(f'gfx/deck/{val}{suit.lower()}.png', self.CARD_TUP)
                cards[f'{(val)}/{suit.upper()}'] = card

        return cards


    def load_icons(self):
        icon_strings = [
            'hand.png',
            'joker.png'
        ]

        icons = {}
        for i in range(len(icon_strings)):
            icons[icon_strings[i][:-4]] = self.scaler(f'gfx/icon/{icon_strings[i]}', self.OPPONENT_AREA_ICON_TUP)

        return icons

    def draw_numbers(self, x, y, num):

        list = [int(u) for u in str(len(num))]

        for i in list:

            self.main_window.blit(self.numbers[i], (x, y))
            x += self.OPPONENT_AREA_ICON_TUP[0]

    def define_window(self):
        pg.init()
        main_window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        # Setting Window title and icon
        pg.display.set_caption(f'DrilleKabale')
        pic = self.scaler('gfx/icon/joker.png', (32, 32))
        pg.display.set_icon(pic)
        return main_window

    def draw_background(self):
        self.main_window.blit(self.BG, [0, 0])

    def card_padding(self):
        paddings = 4
        padding = (self.CARD_WIDTH / 15) - (self.CARD_WIDTH * 3)
        pad = padding / paddings

        return pad

    def other_player_buffer(self, x, y, ID):

        x += self.CARD_PADDING / 2
        y += self.CARD_PADDING
        NY = y
        for buffer in self.table.players[ID].buffer:
            if len(buffer) < 1:
                pic = self.placeholder
                pic.set_alpha(100)
                self.main_window.blit(pic, (x, y))

            elif len(buffer) <= self.OPPONENT_AREA_BUFFER_SIZE:
                for buf in buffer:
                    self.main_window.blit(self.cards[buf.name], (x, y))
                    y += self.CARD_OVERLAY

            else:
                for buf in buffer[-self.OPPONENT_AREA_BUFFER_SIZE:]:
                    self.main_window.blit(self.cards[buf.name],(x, y))
                    y += self.CARD_OVERLAY

            y = NY
            x += self.CARD_WIDTH + self.CARD_PADDING

    def other_player_stack(self, x, y, player):

        pad = self.CARD_PADDING
        # x += pad

        for card in self.table.players[player].stack:

            #pic = pg.transform.rotate(self.cards[card.name], 90)
            self.main_window.blit(self.cards[card.name], (x, y))

    def other_player_area(self):
        paddings = len(self.table.players)
        padding = self.WIDTH - (self.OPPONENT_AREA_WIDTH * (len(self.table.players) - 1))
        pad = padding / paddings
        x = pad
        y = self.PAD
        for player in self.play_order:
            FX = x
            FY = y
            if self.table.players[player].id != self.ID:

                ###To be changed to actual player area###
                area = pg.Surface((self.OPPONENT_AREA_WIDTH + self.CARD_PADDING, self.OPPONENT_AREA_WIDTH * 1.5))
                area.set_alpha(150)
                self.main_window.blit(area, (FX, FY))
                #########################################

                # Draws opponents buffers
                self.other_player_buffer(x, y, player)

                # sets y to right under buffer
                y += (self.OPPONENT_AREA_BUFFER_SIZE * self.CARD_OVERLAY) + self.CARD_HEIGHT
                NY = y

                # Hand and jokers (symbols and numbers)
                self.main_window.blit(self.icons['hand'], (x, y))
                y += self.OPPONENT_AREA_ICON_TUP[0]
                self.main_window.blit(self.icons['joker'], (x, y))
                y = NY
                x += self.OPPONENT_AREA_ICON_TUP[1]
                self.draw_numbers(x, y, self.table.players[player].hand)
                y += self.OPPONENT_AREA_ICON_TUP[0]
                self.draw_numbers(x, y, self.table.players[player].jokers)
                y -= (self.OPPONENT_AREA_ICON_TUP[0] + self.CARD_PADDING)


                # Draws opponents stack
                stack_x = x + self.OPPONENT_AREA_WIDTH - self.OPPONENT_AREA_ICON_TUP[0] -(self.CARD_WIDTH + self.CARD_PADDING)
                y += self.CARD_PADDING
                self.other_player_stack(stack_x, y, player)
                x = FX
                y = FY
                # Moves to next player area
                x += self.OPPONENT_AREA_WIDTH + pad

    def draw_table_stack(self, x, y, count=0):
        rows = 2
        cols = int((len(self.table.fields) / 2) / rows)
        NX = x
        counter = 0
        for rows in range(rows):
            for col in range(cols):
                self.locations[self.counter] = [NX, NX + self.CARD_WIDTH, y, y + self.CARD_HEIGHT, 2, 0]
                self.counter += 1
                if len(self.table.fields[count]) > 0:
                    for card in self.table.fields[count]:
                        self.main_window.blit(self.cards[card.gfx_front], (NX, y))
                else:
                    self.main_window.blit(self.placeholder, (NX, y))
                counter += 1
                NX += self.CARD_WIDTH + self.CARD_PADDING
            NX = x
            y += self.CARD_HEIGHT + self.CARD_PADDING

        return count


    def table_area(self):
        NX = 0
        NY = (self.HEIGHT / 2) - (self.CARD_HEIGHT / 1.3)

        # Draws the deck
        x = (self.WIDTH / 2) - (self.CARD_WIDTH /2)
        y = NY + (self.CARD_HEIGHT / 2)
        for _ in table.deck.cards:
            self.main_window.blit(self.CARD_BACK, (x, y))

        # Draws table stacks
        y = NY
        x = NX + (self.TABLE_AREA_STACKS_SIDE_WIDTH / 2) - (self.TABLE_AREA_STACKS_SIDE_DRAW_WIDTH / 2)
        count = self.draw_table_stack(x, y)
        x = self.WIDTH - (self.TABLE_AREA_STACKS_SIDE_WIDTH / 2) - (self.TABLE_AREA_STACKS_SIDE_DRAW_WIDTH / 2)
        self.draw_table_stack(x, y,count)

    def player_buffer(self, x, y, ID):

        x += self.PAD
        NY = y

        for buffer in self.table.players[ID].buffer:
            if len(buffer) < 1:
                pic = self.placeholder
                pic.set_alpha(100)
                self.main_window.blit(pic, (x, y))

            elif len(buffer) <= self.OPPONENT_AREA_BUFFER_SIZE:
                for buf in buffer:
                    self.main_window.blit(self.cards[buf.name], (x, y))
                    y -= self.CARD_OVERLAY

            else:
                for buf in buffer[-self.OPPONENT_AREA_BUFFER_SIZE:]:
                    self.main_window.blit(self.cards[buf.name], (x, y))
                    y -= self.CARD_OVERLAY
            y = NY
            x += self.CARD_WIDTH + (self.CARD_PADDING / 2)


    def hand_area(self):
        x = (self.WIDTH / 2) - (self.HAND_WIDTH / 2)
        y = self.HEIGHT - self.HAND_HEIGHT
        bg = pg.Surface((self.HAND_WIDTH, self.HAND_HEIGHT))
        bg.set_alpha(100)
        self.main_window.blit(bg, (x, y))

        # Hand
        x += self.CARD_PADDING / 2
        y += self.CARD_PADDING
        for card in self.table.players[self.ID].hand:
            self.main_window.blit(self.cards[card.name], (x, y))



            x += self.CARD_PADDING + self.CARD_WIDTH

        # Stack
        self.player_buffer(0, y, self.ID)
        new = (self.WIDTH / 2) + (self.HAND_WIDTH / 2)
        new = self.WIDTH - new
        new = new / 2

        x = (self.WIDTH / 2) + (self.HAND_WIDTH / 2) + (new / 6)

        if self.table.players[self.ID].stack:
            for card in self.table.players[self.ID].stack:

                self.main_window.blit(self.cards[card.name], (x, y))
        else:
            self.main_window.blit(self.placeholder, (x, y))

        # Joker stack
        x += new
        if self.table.players[self.ID].jokers:
            for card in self.table.players[self.ID].jokers:
                self.main_window.blit(self.cards[card.name], (x, y))
                self.locations[self.counter] = [x, x + self.CARD_WIDTH, y, y + self.CARD_HEIGHT, 2, 0]
                self.counter += 1

        else:
            self.main_window.blit(self.placeholder, (x, y))


    def mouse_click(self, location):
        for i in self.locations:
            if location[0] >= i[0] and not location[0] >= i[1]:
                if location[1] >= i[2] and not location[1] >= i[3]:
                    if self.source == 0:
                        self.source = i[4]
                        self.augment = i[5]
                        #print(i[4])
                    else:
                        self.dest = i[4]
                        self.src = i[5]


    def main_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.quit()
                    pg.quit()
                    exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos()
                    self.mouse_click(location)
                    #print(location)

            self.draw_background()
            self.other_player_area()
            self.table_area()
            self.hand_area()
            # NY = 15
            # for buf in self.table.players[self.ID].buffer[0]:
            #     pic = self.scaler(buf.gfx_front, self.CARD_SIZE)
            #     self.main_window.blit(pic, (15, NY))
            #     NY += 10
            print(self.source, self.augment)
            pg.display.update()
            self.clock.tick(60)


# player_names = [('Ronny', 10)]
#player_names = [('Ronny', 10), ('Dyring', 20)]
#player_names = [('Ronny', 10), ('Dyring', 20), ('Kurt', 30)]
player_names = [('Ronny', 10), ('Dyring', 20), ('Kurt', 30), ('Ronny', 40)]
choice = 4
table = Table(player_names, Deck(choice))
table.ides()



game = Game(10, table)