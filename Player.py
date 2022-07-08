from Collide import *
from Entity import *
from SaveManager import *
from menu import Menu

vec = pg.math.Vector2
m = Menu()


class Player(pg.sprite.Sprite):

    def __init__(self, Game, x, y):
        self.s = save()
        self.groups = Game.sprites, Game.player
        pg.sprite.Sprite.__init__(self, self.groups)
        self.Player_grav = Player_grav
        #
        self.MaxHealth = self.s.load(self.s.MaxHP)
        self.health = self.s.load(self.s.HP)
        self.entry = self.s.load(self.s.curent_entry)
        #
        self.powerDoubleJump = self.s.load(self.s.DoubleJump)
        if self.powerDoubleJump == 1:
            self.canDoubleJump = True
        else:
            self.canDoubleJump = False
        #
        self.powerWallSlide = self.s.load(self.s.WallSlide)
        if self.powerWallSlide == 1:
            self.canWallSlide = True
        else:
            self.canWallSlide = False
        #
        self.Wall_Collide = False
        self.Wall_Slide = False
        self.FaceLeft = False
        self.LookUp = False
        self.LookDown = False
        self.OnGround = False
        self.Idle = True
        self.walking = False
        self.jumping = False
        self.falling = False
        #
        self.sword_out = False
        self.bow_out = False
        self.magic_out = False
        #
        self.game = Game
        self.current_frame = 0
        self.last_update = 0
        self.load_img()
        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        self.hit_rect = Player_hit_rect
        self.hit_rect.center = self.rect.center
        self.front_rect = Front_Hit_rect
        self.x = x
        self.y = y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_img(self):
        # idle
        self.idle = [self.game.idle.get_image(0, 0, 50, 37),
                     self.game.idle.get_image(50, 0, 50, 37),
                     self.game.idle.get_image(100, 0, 50, 37),
                     self.game.idle.get_image(150, 0, 50, 37)]
        for frame in self.idle:
            frame.set_colorkey(Black)
        self.idle_l = []
        for frame in self.idle:
            frame.set_colorkey(Black)
            self.idle_l.append(pg.transform.flip(frame, True, False))
        # walk
        self.walk = [self.game.idle.get_image(0, 37, 50, 37),
                     self.game.idle.get_image(50, 37, 50, 37),
                     self.game.idle.get_image(100, 37, 50, 37),
                     self.game.idle.get_image(150, 37, 50, 37),
                     self.game.idle.get_image(200, 37, 50, 37),
                     self.game.idle.get_image(250, 37, 50, 37)]
        for frame in self.walk:
            frame.set_colorkey(Black)
        self.walk_l = []
        for frame in self.walk:
            frame.set_colorkey(Black)
            self.walk_l.append(pg.transform.flip(frame, True, False))
        # run
        self.run = [self.game.idle.get_image(0, 74, 50, 37),
                    self.game.idle.get_image(50, 74, 50, 37),
                    self.game.idle.get_image(100, 74, 50, 37),
                    self.game.idle.get_image(150, 74, 50, 37),
                    self.game.idle.get_image(200, 74, 50, 37),
                    self.game.idle.get_image(250, 74, 50, 37)]
        for frame in self.run:
            frame.set_colorkey(Black)
        self.run_l = []
        for frame in self.run:
            frame.set_colorkey(Black)
            self.run_l.append(pg.transform.flip(frame, True, False))
        # slide
        self.slide = [self.game.idle.get_image(0, 111, 50, 37),
                      self.game.idle.get_image(50, 111, 50, 37)]
        for frame in self.slide:
            frame.set_colorkey(Black)
        self.slide_l = []
        for frame in self.slide:
            frame.set_colorkey(Black)
            self.slide_l.append(pg.transform.flip(frame, True, False))
        # crouch
        self.crouch = [self.game.idle.get_image(0, 148, 50, 37),
                       self.game.idle.get_image(50, 148, 50, 37),
                       self.game.idle.get_image(100, 148, 50, 37),
                       self.game.idle.get_image(150, 148, 50, 37)]
        for frame in self.crouch:
            frame.set_colorkey(Black)
        self.crouch_l = []
        for frame in self.crouch:
            frame.set_colorkey(Black)
            self.crouch_l.append(pg.transform.flip(frame, True, False))
        # crouch_walk
        self.crouch_walk = [self.game.idle.get_image(0, 185, 50, 37),
                            self.game.idle.get_image(50, 185, 50, 37),
                            self.game.idle.get_image(100, 185, 50, 37),
                            self.game.idle.get_image(150, 185, 50, 37),
                            self.game.idle.get_image(200, 185, 50, 37),
                            self.game.idle.get_image(250, 185, 50, 37)]
        for frame in self.crouch_walk:
            frame.set_colorkey(Black)
        self.crouch_walk_l = []
        for frame in self.crouch_walk:
            frame.set_colorkey(Black)
            self.crouch_walk_l.append(pg.transform.flip(frame, True, False))
        # jump
        self.jump = [self.game.idle.get_image(0, 222, 50, 37),
                     self.game.idle.get_image(50, 222, 50, 37),
                     self.game.idle.get_image(100, 222, 50, 37),
                     self.game.idle.get_image(150, 222, 50, 37)]
        for frame in self.jump:
            frame.set_colorkey(Black)
        self.jump_l = []
        for frame in self.jump:
            frame.set_colorkey(Black)
            self.jump_l.append(pg.transform.flip(frame, True, False))
        # double_jump
        self.double_jump = [self.game.idle.get_image(0, 259, 50, 37),
                            self.game.idle.get_image(50, 259, 50, 37),
                            self.game.idle.get_image(100, 259, 50, 37),
                            self.game.idle.get_image(150, 259, 50, 37)]
        for frame in self.double_jump:
            frame.set_colorkey(Black)
        self.double_jump_l = []
        for frame in self.double_jump:
            frame.set_colorkey(Black)
            self.double_jump_l.append(pg.transform.flip(frame, True, False))
        # fall
        self.fall = [self.game.idle.get_image(0, 296, 50, 37),
                     self.game.idle.get_image(50, 296, 50, 37)]
        for frame in self.fall:
            frame.set_colorkey(Black)
        self.fall_l = []
        for frame in self.fall:
            frame.set_colorkey(Black)
            self.fall_l.append(pg.transform.flip(frame, True, False))
        # swrd_draw
        self.swrd_draw = [self.game.idle.get_image(0, 333, 50, 37),
                          self.game.idle.get_image(50, 333, 50, 37),
                          self.game.idle.get_image(100, 333, 50, 37),
                          self.game.idle.get_image(150, 333, 50, 37)]
        for frame in self.swrd_draw:
            frame.set_colorkey(Black)
        self.swrd_draw_l = []
        for frame in self.swrd_draw:
            frame.set_colorkey(Black)
            self.swrd_draw_l.append(pg.transform.flip(frame, True, False))
        # swrd_sheathe
        self.swrd_sheathe = [self.game.idle.get_image(0, 370, 50, 37),
                             self.game.idle.get_image(50, 370, 50, 37),
                             self.game.idle.get_image(100, 370, 50, 37),
                             self.game.idle.get_image(150, 370, 50, 37)]
        for frame in self.swrd_sheathe:
            frame.set_colorkey(Black)
        self.swrd_sheathe_l = []
        for frame in self.swrd_sheathe:
            frame.set_colorkey(Black)
            self.swrd_sheathe_l.append(pg.transform.flip(frame, True, False))
        # idle_sword
        self.idle_sword = [self.game.idle.get_image(0, 407, 50, 37),
                           self.game.idle.get_image(50, 407, 50, 37),
                           self.game.idle.get_image(100, 407, 50, 37),
                           self.game.idle.get_image(150, 407, 50, 37)]
        for frame in self.idle_sword:
            frame.set_colorkey(Black)
        self.idle_sword_l = []
        for frame in self.idle_sword:
            frame.set_colorkey(Black)
            self.idle_sword_l.append(pg.transform.flip(frame, True, False))
        # run_sword
        self.run_sword = [self.game.idle.get_image(0, 444, 50, 37),
                          self.game.idle.get_image(50, 444, 50, 37),
                          self.game.idle.get_image(100, 444, 50, 37),
                          self.game.idle.get_image(150, 444, 50, 37),
                          self.game.idle.get_image(200, 444, 50, 37),
                          self.game.idle.get_image(250, 444, 50, 37)]
        for frame in self.run_sword:
            frame.set_colorkey(Black)
        self.run_sword_l = []
        for frame in self.run_sword:
            frame.set_colorkey(Black)
            self.run_sword_l.append(pg.transform.flip(frame, True, False))
        # atk_1
        self.atk_1 = [self.game.idle.get_image(0, 481, 50, 37),
                      self.game.idle.get_image(50, 481, 50, 37),
                      self.game.idle.get_image(100, 481, 50, 37),
                      self.game.idle.get_image(150, 481, 50, 37),
                      self.game.idle.get_image(200, 481, 50, 37)]
        for frame in self.atk_1:
            frame.set_colorkey(Black)
        self.atk_1_l = []
        for frame in self.atk_1:
            frame.set_colorkey(Black)
            self.atk_1_l.append(pg.transform.flip(frame, True, False))
        # atk_2
        self.atk_2 = [self.game.idle.get_image(0, 518, 50, 37),
                      self.game.idle.get_image(50, 518, 50, 37),
                      self.game.idle.get_image(100, 518, 50, 37),
                      self.game.idle.get_image(150, 518, 50, 37),
                      self.game.idle.get_image(200, 518, 50, 37),
                      self.game.idle.get_image(250, 518, 50, 37)]
        for frame in self.atk_2:
            frame.set_colorkey(Black)
        self.atk_2_l = []
        for frame in self.atk_2:
            frame.set_colorkey(Black)
            self.atk_2_l.append(pg.transform.flip(frame, True, False))
        # atk_3
        self.atk_3 = [self.game.idle.get_image(0, 555, 50, 37),
                      self.game.idle.get_image(50, 555, 50, 37),
                      self.game.idle.get_image(100, 555, 50, 37),
                      self.game.idle.get_image(150, 555, 50, 37),
                      self.game.idle.get_image(200, 555, 50, 37),
                      self.game.idle.get_image(250, 555, 50, 37), ]
        for frame in self.atk_3:
            frame.set_colorkey(Black)
        self.atk_3_l = []
        for frame in self.atk_3:
            frame.set_colorkey(Black)
            self.atk_3_l.append(pg.transform.flip(frame, True, False))
        # air_atk_1
        self.air_atk_1 = [self.game.idle.get_image(0, 592, 50, 37),
                          self.game.idle.get_image(50, 592, 50, 37),
                          self.game.idle.get_image(100, 592, 50, 37),
                          self.game.idle.get_image(150, 592, 50, 37),
                          self.game.idle.get_image(150, 592, 50, 37)]
        for frame in self.air_atk_1:
            frame.set_colorkey(Black)
        self.air_atk_1_l = []
        for frame in self.air_atk_1:
            frame.set_colorkey(Black)
            self.air_atk_1_l.append(pg.transform.flip(frame, True, False))
        # air_atk_2
        self.air_atk_2 = [self.game.idle.get_image(0, 629, 50, 37),
                          self.game.idle.get_image(50, 629, 50, 37),
                          self.game.idle.get_image(100, 629, 50, 37)]
        for frame in self.air_atk_2:
            frame.set_colorkey(Black)
        self.air_atk_2_l = []
        for frame in self.air_atk_2:
            frame.set_colorkey(Black)
            self.air_atk_2_l.append(pg.transform.flip(frame, True, False))
        # air_atk_3
        self.air_atk_3 = [self.game.idle.get_image(0, 666, 50, 37),
                          self.game.idle.get_image(50, 666, 50, 37),
                          self.game.idle.get_image(100, 666, 50, 37),
                          self.game.idle.get_image(150, 666, 50, 37)]
        for frame in self.air_atk_3:
            frame.set_colorkey(Black)
        self.air_atk_3_l = []
        for frame in self.air_atk_3:
            frame.set_colorkey(Black)
            self.air_atk_3_l.append(pg.transform.flip(frame, True, False))
        # bow
        self.bow = [self.game.idle.get_image(0, 703, 50, 37),
                    self.game.idle.get_image(50, 703, 50, 37),
                    self.game.idle.get_image(100, 703, 50, 37),
                    self.game.idle.get_image(150, 703, 50, 37),
                    self.game.idle.get_image(200, 703, 50, 37),
                    self.game.idle.get_image(250, 703, 50, 37),
                    self.game.idle.get_image(300, 703, 50, 37),
                    self.game.idle.get_image(350, 703, 50, 37)]
        for frame in self.bow:
            frame.set_colorkey(Black)
        self.bow_l = []
        for frame in self.bow:
            frame.set_colorkey(Black)
            self.bow_l.append(pg.transform.flip(frame, True, False))
        # bow_air
        self.bow_air = [self.game.idle.get_image(0, 740, 50, 37),
                        self.game.idle.get_image(50, 740, 50, 37),
                        self.game.idle.get_image(100, 740, 50, 37),
                        self.game.idle.get_image(150, 740, 50, 37),
                        self.game.idle.get_image(200, 740, 50, 37),
                        self.game.idle.get_image(250, 740, 50, 37)]
        for frame in self.bow_air:
            frame.set_colorkey(Black)
        self.bow_air_l = []
        for frame in self.bow_air:
            frame.set_colorkey(Black)
            self.bow_air_l.append(pg.transform.flip(frame, True, False))
        # spell
        self.spell = [self.game.idle.get_image(0, 777, 50, 37),
                      self.game.idle.get_image(50, 777, 50, 37),
                      self.game.idle.get_image(100, 777, 50, 37),
                      self.game.idle.get_image(150, 777, 50, 37), ]
        for frame in self.spell:
            frame.set_colorkey(Black)
        self.spell_l = []
        for frame in self.spell:
            frame.set_colorkey(Black)
            self.spell_l.append(pg.transform.flip(frame, True, False))
        # spell_loop
        self.spell_loop = [self.game.idle.get_image(0, 814, 50, 37),
                           self.game.idle.get_image(50, 814, 50, 37),
                           self.game.idle.get_image(100, 814, 50, 37),
                           self.game.idle.get_image(150, 814, 50, 37)]
        for frame in self.spell_loop:
            frame.set_colorkey(Black)
        self.spell_loop_l = []
        for frame in self.spell_loop:
            frame.set_colorkey(Black)
            self.spell_loop_l.append(pg.transform.flip(frame, True, False))
        # hurt
        self.hurt = [self.game.idle.get_image(0, 851, 50, 37),
                     self.game.idle.get_image(50, 851, 50, 37),
                     self.game.idle.get_image(100, 851, 50, 37)]
        for frame in self.hurt:
            frame.set_colorkey(Black)
        self.hurt_l = []
        for frame in self.hurt:
            frame.set_colorkey(Black)
            self.hurt_l.append(pg.transform.flip(frame, True, False))
        # die
        self.die = [self.game.idle.get_image(0, 888, 50, 37),
                    self.game.idle.get_image(50, 888, 50, 37),
                    self.game.idle.get_image(100, 888, 50, 37),
                    self.game.idle.get_image(150, 888, 50, 37),
                    self.game.idle.get_image(200, 888, 50, 37),
                    self.game.idle.get_image(250, 888, 50, 37),
                    self.game.idle.get_image(300, 888, 50, 37), ]
        for frame in self.die:
            frame.set_colorkey(Black)
        self.die_l = []
        for frame in self.die:
            frame.set_colorkey(Black)
            self.die_l.append(pg.transform.flip(frame, True, False))
        # item
        self.item = [self.game.idle.get_image(0, 925, 50, 37),
                     self.game.idle.get_image(50, 925, 50, 37),
                     self.game.idle.get_image(100, 925, 50, 37), ]
        for frame in self.item:
            frame.set_colorkey(Black)
        self.item_l = []
        for frame in self.item:
            frame.set_colorkey(Black)
            self.item_l.append(pg.transform.flip(frame, True, False))
        # ladle
        self.ladle = [self.game.idle.get_image(0, 962, 50, 37),
                      self.game.idle.get_image(50, 962, 50, 37),
                      self.game.idle.get_image(100, 962, 50, 37),
                      self.game.idle.get_image(150, 962, 50, 37)]
        for frame in self.ladle:
            frame.set_colorkey(Black)
        self.ladle_l = []
        for frame in self.ladle:
            frame.set_colorkey(Black)
            self.ladle_l.append(pg.transform.flip(frame, True, False))

    def get_keys(self):

        if self.Wall_Slide and self.vel.y > 0 and self.canWallSlide:
            self.vel = vec(0, 0.1)
        else:
            self.acc = vec(0, self.Player_grav)
        keys = pg.key.get_pressed()
        #
        if not self.game.pause:
            if keys[pg.K_a]:
                self.acc.x = -Player_acc
            if keys[pg.K_d]:
                self.acc.x = Player_acc
            if keys[pg.K_w]:
                self.LookUp = True
            if keys[pg.K_s]:
                self.LookDown = True

    def get_status(self):
        # idle
        if self.acc.x == 0:
            self.Idle = True
        else:
            self.Idle = False
        # direction
        if self.acc.x >= 0.3 or self.vel.x >= 1:
            self.FaceLeft = False
        if self.acc.x <= -0.3 or self.vel.x <= -1:
            self.FaceLeft = True
        # lookup/down
        keys = pg.key.get_pressed()
        if not keys[pg.K_w]:
            self.LookUp = False
        if not keys[pg.K_s]:
            self.LookDown = False

    def update(self):
        self.get_status()
        self.get_keys()
        self.draw()
        #
        self.acc.x += self.vel.x * Player_friction
        #
        self.vel.x += self.acc.x
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.x += self.vel.x + 0.5 * self.acc.x
        #
        if self.vel.y <= 150:
            self.vel.y += self.acc.y
        self.y += self.vel.y + 0.5 * self.acc.y
        # hit box to player
        # hit box x
        self.hit_rect.centerx = self.x
        CollideWall(self, self.game.block, 'x')
        self.rect.x = self.hit_rect.x - 20
        # hit box y
        self.hit_rect.centery = self.y + 17
        CollideWall(self, self.game.block, 'y')
        self.rect.y = self.hit_rect.y - 7
        # other hitbox
        if self.FaceLeft:
            self.front_rect.centerx = self.x - 2
        else:
            self.front_rect.centerx = self.x + 2
        self.front_rect.y = self.y
        # other colide
        WallSlide(self, self.game.block)
        Collide_teleport(self, self.game, self.game.teleport)
        power(self, self.game, self.game.collectibles)
        self.s = save()

    def Save(self, name, data):
        self.s.save(name, data, load1(saves))

    def draw(self):
        now = pg.time.get_ticks()
        if self.idle:
            if self.FaceLeft:
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_l)
                    bottom = self.rect.bottom
                    self.image = self.idle_l[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            else:
                if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle)
                    bottom = self.rect.bottom
                    self.image = self.idle[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        else:
            pass

    def TakeDamage(self, damage):
        self.health += damage
        self.Save(self.s.HP, int(self.health))

    def Attack(self, game, type):
        if type == 'sword':
            if not self.LookUp and not self.LookDown:
                if self.FaceLeft:
                    attack_rect(game, self.x - 25, self.y, 20, 29)
                if not self.FaceLeft:
                    attack_rect(game, self.x + 5, self.y, 20, 29)
            if self.LookUp:
                attack_rect(game, self.x - 10, self.y - 10, 20, 31)
            if self.LookDown:
                attack_rect(game, self.x - 10, self.y + 10, 20, 31)
        if type == 'bow':
            if self.FaceLeft:
                projectile(game, self.x - 32, self.y, 20, 10, -5)
            else:
                projectile(game, self.x + 12, self.y, 20, 10, 5)
        if type == 'magic':
            if self.FaceLeft:
                projectile(game, self.x - 32, self.y, 20, 10, -3)
            else:
                projectile(game, self.x + 12, self.y, 20, 10, 3)
        game.lastkill = pg.time.get_ticks()

    def JUMP(self):
        self.hit_rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.block, False, collide_hit_rect)
        self.hit_rect.y -= 1
        if hits:
            self.current_atk = 1
            self.Player_grav = Player_grav
            self.current_frame = 0
            self.Double_Jump = True
            self.vel.y = -Player_jump
        if self.canDoubleJump:
            if not hits and self.Double_Jump:
                self.Player_grav = Player_grav
                self.current_frame = 0
                self.Jump_2 = True
                self.Double_Jump = False
                self.vel.y = -Player_jump
        if self.canWallSlide:
            if self.Wall_Slide:
                if self.FaceLeft:
                    self.vel.x = 6.5
                else:
                    self.vel.x = -6.5
                self.FaceLeft = not self.FaceLeft
                self.Double_Jump = True
                self.vel.y = -Player_jump

