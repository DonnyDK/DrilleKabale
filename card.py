class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
        self.name = f'{self.value}/{self.suit.upper()}'
        self.gfx_front = self.set_gfx_front()
        self.gfx_back = 'gfx/rear.png'
        self.isJoker = self.isJoker()
        self.back = True

    def isJoker(self):
        if self.value > 12:
            return True
        return False

    # def __unicode__(self):
    #     return self.show()
    #
    # def __str__(self):
    #     return self.show()
    #
    # def __repr__(self):
    #     return self.show()

    def set_gfx_front(self):
        return f'{self.value}{self.suit[0].lower()}'

    def show(self):
        if self.value == 1:
            val = "A"
        elif self.value == 11:
            val = "J"
        elif self.value == 12:
            val = "Q"
        elif self.value == 13:
            val = "K"
        elif self.value == 14:
            val = "F"
        else:
            val = self.value

        return "{}/{}".format(val, self.suit)
