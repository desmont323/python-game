from Setting import *


class Heal(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self.game.item)
        self.damage = 10
        self.kb = 0
        self.x = game.jumper.x


class Damage(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self.game.item)
        self.damage = 10
        self.kb = 0
        self.x = game.jumper.x

