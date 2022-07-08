from Setting import *

vec = pg.math.Vector2


class block(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.block
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, paths, entry):
        self.groups = game.teleport
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.map = paths
        self.entry = entry


class attack_rect(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.attack_rect, game.sprites
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y
        self.load_img()
        self.image = self.idle[0]

    def load_img(self):
        self.idle = [self.game.idle.get_image(250, 0, self.w, self.h)]
        for frame in self.idle:
            frame.set_colorkey(White)
        self.idle_l = []
        for frame in self.idle:
            frame.set_colorkey(White)
            self.idle_l.append(pg.transform.flip(frame, True, False))

    def update(self):
        pass


class projectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, vel):
        self.groups = game.projectile, game.sprites
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = vel
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.load_img()
        self.image = self.idle[0]

    def load_img(self):
        self.idle = [self.game.idle.get_image(250, 0, 20, 10)]
        for frame in self.idle:
            frame.set_colorkey(White)
        self.idle_l = []
        for frame in self.idle:
            frame.set_colorkey(White)
            self.idle_l.append(pg.transform.flip(frame, True, False))

    def update(self):
        if self.speed != 0:
            self.acc = vec(0, 0)
            self.vel.x = self.speed
            #
            self.vel.x += self.acc.x
            self.x += self.vel.x + 0.5 * self.acc.x
            #
            self.hit_rect.x = self.x
            self.rect.x = self.hit_rect.x


class collectible(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.collectibles, game.sprites
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.load_img(w, h)
        self.image = self.idle[0]
        self.powername = "a"

    def load_img(self, w, h):
        self.idle = [self.game.idle.get_image(250, 0, w, h)]
        for frame in self.idle:
            frame.set_colorkey(White)
        self.idle_l = []
        for frame in self.idle:
            frame.set_colorkey(White)
            self.idle_l.append(pg.transform.flip(frame, True, False))

    def update(self):
        pass
