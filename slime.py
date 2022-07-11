from Collide import *
from Setting import *

vec = pg.math.Vector2


class Slime(pg.sprite.Sprite):

    def __init__(self, Game, x, y):
        self.groups = Game.sprites, Game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = Game
        self.current_frame = 0
        self.last_update = 0
        self.load_img()
        self.image = self.idle_l[0]
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 30, 15)
        self.hit_rect.center = self.rect.center
        self.front_rect = pg.Rect(0, 0, 1, 20)
        self.front_rect.center = self.rect.center
        self.x = x
        self.y = y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.Slime_acc = 0.5
        self.Slime_friction = -0.6
        self.Slime_grav = 0.9
        self.Slime_speed = 0.3
        self.kb = 5
        self.damage = 10

        self.Wall_Collide = False
        self.FaceLeft = True
        self.idle = True
        self.walking = False

    def load_img(self):
        self.idle_l = [self.game.slime.get_image(0, 0, 32, 25),
                       self.game.slime.get_image(32, 0, 32, 25),
                       self.game.slime.get_image(64, 0, 32, 25),
                       self.game.slime.get_image(96, 0, 32, 25)]
        for frame in self.idle_l:
            frame.set_colorkey(Black)
        self.idle_r = []
        for frame in self.idle_l:
            frame.set_colorkey(Black)
            self.idle_r.append(pg.transform.flip(frame, True, False))

        self.walking_l = [self.game.slime.get_image(0, 25, 32, 25),
                          self.game.slime.get_image(32, 25, 32, 25),
                          self.game.slime.get_image(64, 25, 32, 25),
                          self.game.slime.get_image(96, 25, 32, 25)]
        for frame in self.walking_l:
            frame.set_colorkey(Black)
        self.walking_r = []
        for frame in self.walking_l:
            frame.set_colorkey(Black)
            self.walking_r.append(pg.transform.flip(frame, True, False))

    def update(self):
        if self.Wall_Collide or not pg.sprite.spritecollide(self, self.game.block, False, collide_front_rect):
            self.FaceLeft = not self.FaceLeft
            self.last_update = 0
        self.animate()
        self.getStatue()
        self.acc = vec(0, self.Slime_grav)
        if self.FaceLeft:
            self.acc.x = -self.Slime_speed
        else:
            self.acc.x = self.Slime_speed
        #
        self.acc.x += self.vel.x * self.Slime_friction
        #
        self.vel.x += self.acc.x
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.x += self.vel.x + 0.5 * self.acc.x
        #
        if self.vel.y <= 150:
            self.vel.y += self.acc.y
        self.y += self.vel.y + 0.5 * self.acc.y
        # hit box x
        self.hit_rect.centerx = self.x
        CollideWall(self, self.game.block, 'x')
        self.rect.x = self.hit_rect.x
        # hit box y
        self.hit_rect.centery = self.y + 17
        CollideWall(self, self.game.block, 'y')
        self.rect.y = self.hit_rect.y - 9
        # fall rect
        if self.FaceLeft:
            self.front_rect.centerx = self.x - 16
        else:
            self.front_rect.centerx = self.x + 16
        self.front_rect.centery = self.y + 10

    def getStatue(self):
        if self.vel.x == 0:
            self.walking = False
            self.idle = True
        else:
            self.idle = False
            self.walking = True

    def animate(self):
        now = pg.time.get_ticks()
        if self.idle:
            if self.FaceLeft:
                if now - self.last_update >= 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_l)
                    bottom = self.rect.bottom
                    self.image = self.idle_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            else:
                if now - self.last_update >= 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_r)
                    bottom = self.rect.bottom
                    self.image = self.idle_r[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        if self.walking:
            if self.FaceLeft:
                if now - self.last_update >= 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walking_l)
                    bottom = self.rect.bottom
                    self.image = self.walking_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            else:
                if now - self.last_update >= 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walking_r)
                    bottom = self.rect.bottom
                    self.image = self.walking_r[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
