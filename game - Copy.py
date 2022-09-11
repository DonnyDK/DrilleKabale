import pygame as pg
import random
from table import Table
from deck import Deck


class Game:
    def __init__(self, ID, table):
        self.ID = ID
        self.table = table
        self.HEIGHT = 900
        self.WIDTH = self.HEIGHT
        self.CARD_SIZE = self.scale_relativ(self.WIDTH / 10, 1.452)
        self.backside = self.scaler('gfx/Back_Red_2.png', self.CARD_SIZE)
        self.x_pad = int(self.CARD_SIZE[0] / 20)
        self.y_pad = int(self.CARD_SIZE[1] / 20)

        self.placeholder = self.scaler('gfx/placeholder.png', self.CARD_SIZE)
        self.player = self.table.players[self.ID]

        self.main_window = self.define_window()
        self.BG = self.scaler('gfx/wood1.png', (self.WIDTH, self.HEIGHT))

        self.clock = pg.time.Clock()

        self.numbers = self.load_numbers()

        self.play_order = list(self.table.players.keys())
        while not self.play_order[0] == self.ID:
            self.play_order.insert(0, self.play_order.pop())




        for i in range(15):
            for player in self.table.players:
                data = (1, random.randint(1, 5), 3, random.randint(1, 3), 10)

                if self.table.players[player].hasTurn:
                    #self.table.draw(self.table.players[player].id, 5)
                    self.table.move(player, data)


        self.main_loop()

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
        for i in range(0, 10):
            numbers[i] = self.scaler(f'gfx/{i}.png', self.CARD_SIZE, 0.5)

        return numbers

    def define_window(self):
        pg.init()
        main_window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption(f'DrilleKabale')
        pic = self.scaler('gfx/placeholder_joker.png', (32, 32))
        pg.display.set_icon(pic)
        return main_window

    def draw_window(self):
        self.main_window.blit(self.BG, [0, 0])

    def other_player_stack(self, x, y, W, player, scale):
        y = y + (self.CARD_SIZE[1] / 10)
        x = x + W - self.CARD_SIZE[1] + self.x_pad
        for card in self.table.players[player].hand:

            pic = self.scaler(card.gfx_front, (self.CARD_SIZE[0], self.CARD_SIZE[1]), scale)
            pic = pg.transform.rotate(pic, 90)
            self.main_window.blit(pic, (x, y))

    def other_player_buffer(self, x, y, W, ID, scale=1):

        placeholder = self.scaler('gfx/placeholder.png', (self.CARD_SIZE[0], self.CARD_SIZE[1]), scale)
        pad = self.x_pad * scale
        padding = pad * 3
        x = x + (pad * 1.5)
        CW = (W - padding) / 3
        y = y + (pad * 1.5)

        # Running through players buffers
        for buffer in self.table.players[ID].buffer:

            NY = y
            # Draws placeholder if buffer is empty
            if len(buffer) == 0:
                pic = placeholder
                pic.set_alpha(50)
                self.main_window.blit(pic, (x, y))
                #NY += self.CARD_SIZE[1] / 9

            else:
                # Draws card in buffer if less than 11
                if len(buffer) < 11:
                    for buf in buffer:
                        pic = self.scaler(buf.gfx_front, (self.CARD_SIZE[0], self.CARD_SIZE[1]), scale)
                        self.main_window.blit(pic, (x, NY))
                        NY += self.CARD_SIZE[1] / 9
                # Draws first 10 cards in buffer
                else:
                    for buf in buffer[-10:]:
                        pic = self.scaler(buf.gfx_front, (self.CARD_SIZE[0], self.CARD_SIZE[1]), scale)
                        self.main_window.blit(pic, (x, NY))
                        NY += self.CARD_SIZE[1] / 9


            x += CW + pad

        return y + (self.CARD_SIZE[1] / 9 * 10) + self.CARD_SIZE[1] * scale

    def other_player_area(self):
        scale = 0.8
        CW = self.CARD_SIZE[0] * scale
        pad = ((len(self.table.players)) * (self.x_pad * 2))
        W = pad + (3 * CW)
        #W = (self.WIDTH / 3) - 2 * self.x_pad
        H = (self.HEIGHT - (self.HEIGHT / 6) - 30) / 2 - 10
        y = 10

        # Defines X from length for player list
        if len(self.table.players) == 2:
            x = (self.WIDTH / 2) - (W / 2)

        if len(self.table.players) == 3:
            pad = 3 * self.x_pad
            x = (self.WIDTH / 2) - W - (self.x_pad / 2)

        if len(self.table.players) == 4:
            pad = 4 * self.x_pad
            x = (self.WIDTH / 2) - (W * 1.5) - self.x_pad


        for player in self.play_order:
            #
            if self.table.players[player].id != self.ID:
                ###To be changed to actual player area###
                # area = pg.Surface((W, H))
                # self.main_window.blit(area, (x, y))
                #########################################

                # Set  x & y for just below buffer and draws the players 3 buffers
                NY = self.other_player_buffer(x, y, W, player, scale)
                NX = x + ((self.x_pad * scale) * 1.5)

                # #########################################
                # # shows player id NOT TO BE USED WITH REST OF FUNCTION
                # hand_number = [int(x) for x in str(self.table.players[player].id)]
                # Mx = NX + (self.CARD_SIZE[0] * 0.4)
                # My = NY - self.y_pad
                #
                # for i in hand_number:
                #     pic = self.numbers[i]
                #     self.main_window.blit(pic, (Mx, My))
                #     Mx += self.CARD_SIZE[0]
                # #########################################

                # Hand icon
                pic = self.scaler('gfx/hand.png', (self.CARD_SIZE[0], self.CARD_SIZE[0]), 0.5)
                self.main_window.blit(pic, (NX, NY))
                # Joker icon
                pic = self.scaler('gfx/placeholder_joker.png', (self.CARD_SIZE[0], self.CARD_SIZE[0]), 0.4)
                self.main_window.blit(pic, (NX, NY + self.CARD_SIZE[0] * 0.6))

                # Draws stack
                self.other_player_stack(x, NY, W, player, scale)

                # Displays hand count
                hand_number = [int(x) for x in str(len(self.table.players[player].hand))]
                Mx = NX + (self.CARD_SIZE[0] * 0.4)
                My = NY - self.y_pad

                for i in hand_number:
                    pic = self.numbers[i]
                    self.main_window.blit(pic, (Mx, My))
                    Mx += self.CARD_SIZE[0] / 4

                # Displays joker count
                joker_number = [int(x) for x in str(len(self.table.players[player].jokers))]
                Mx = NX + (self.CARD_SIZE[0] * 0.4)
                My = NY + self.CARD_SIZE[0] * 0.4

                for i in joker_number:
                    pic = self.numbers[i]
                    self.main_window.blit(pic, (Mx, My))
                    Mx += self.CARD_SIZE[0] / 4


                # Moves to next player area
                x += W + self.x_pad

    def table_area(self):
        rows = 2
        cols = int(len(self.table.fields) / rows)
        W = (self.CARD_SIZE[0] + self.x_pad) * cols + self.x_pad
        H = (self.CARD_SIZE[1] + self.y_pad) * rows + self.y_pad
        TABLE = ((self.WIDTH / 2) - (W / 2), (self.HEIGHT - (self.HEIGHT / 5)) / 2)
        x, y = TABLE
        x, y = x + self.x_pad, y + self.y_pad

        area = pg.Surface((W, H))

        count = 0
        for i in range(rows):
            for j in range(cols):
                pic = self.placeholder
                pic.set_alpha(50)
                self.main_window.blit(pic, (x, y))


                x += self.CARD_SIZE[0] + self.x_pad

                count += 1

            y += self.CARD_SIZE[1] + self.y_pad
            x = TABLE[0] + self.x_pad

    def hand_area(self):
        W = int((self.CARD_SIZE[0] + (self.CARD_SIZE[0] / 20)) * 5  + self.x_pad)
        H = int(self.CARD_SIZE[1] + (self.CARD_SIZE[1] / 20) + self.y_pad)
        HAND = ((self.WIDTH / 2) - (W / 2), (self.HEIGHT - H - 10))
        x, y = HAND
        x, y = x + self.x_pad, y + self.y_pad
        area = pg.Surface((W, H))
        area.set_alpha(100)
        self.main_window.blit(area, list(HAND))


        W = int((self.CARD_SIZE[0] + (self.CARD_SIZE[0] / 20)) * len(self.player.hand) + self.x_pad)
        H = int(self.CARD_SIZE[1] + (self.CARD_SIZE[1] / 20) + self.y_pad)
        x = (self.WIDTH / 2) - (W / 2) + self.x_pad

        if self.player.hand:
            for card in self.player.hand:
                pic = pg.image.load(card.gfx_front)
                pic = pg.transform.scale(pic, self.CARD_SIZE)

                self.main_window.blit(pic, (x, y))
                x += self.CARD_SIZE[0] + (self.CARD_SIZE[0] / 20)

    def main_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.quit()
                    pg.quit()
                    exit()

            self.draw_window()
            self.other_player_area()
            self.table_area()
            self.hand_area()
            # NY = 15
            # for buf in self.table.players[self.ID].buffer[0]:
            #     pic = self.scaler(buf.gfx_front, self.CARD_SIZE)
            #     self.main_window.blit(pic, (15, NY))
            #     NY += 10

            pg.display.update()
            self.clock.tick(60)


#player_names = [('Ronny', 10)]
#player_names = [('Ronny', 10), ('Dyring', 20)]
#player_names = [('Ronny', 10), ('Dyring', 20), ('Kurt', 30)]
player_names = [('Ronny', 10), ('Dyring', 20), ('Kurt', 30), ('Ronny', 40)]
choice = 4
table = Table(player_names, Deck(choice))
table.ides()



game = Game(30, table)