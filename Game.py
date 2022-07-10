from Player import *
from menu import *
from tiledmap import *
from Utilities import *

m = Menu()
vec = pg.math.Vector2


class Game:

    def __init__(self):
        self.lastkill = 0
        self.waiting = False
        self.main_menu = False
        self.save_selection = False
        self.setting = False
        self.save = ""
        pg.init()
        pg.mixer.init()
        self.screen = m.screen
        self.zoom = self.screen.copy()
        # pg.display.set_caption(Title)
        self.clock = pg.time.Clock()
        self.Load_data()
        self.draw_debug = False
        self.running = True
        self.playing = False
        self.inv = False
        self.pause = False

    def Load_data(self):
        self.game_folder = path.dirname(__file__)
        #
        self.map = TiledMap(path.join(self.game_folder, 'map/lvl_1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        #
        self.idle = SpriteSheet(path.join(self.game_folder, 'sprites/character.png'))
        self.slime = SpriteSheet(path.join(self.game_folder, 'sprites/slime.png'))
        self.GUI = SpriteSheet(path.join(self.game_folder, 'sprites/GUI_2x_sliced.png'))
        self.buttonimg = SpriteSheet(path.join(self.game_folder, 'sprites/buttons_2x.png'))
        self.ICON = SpriteSheet(path.join(self.game_folder, 'sprites/icon.png'))
        #
        self.bg = pg.image.load(path.join(self.game_folder, 'img/bg.png'))
        self.bg = pg.transform.scale(self.bg, Size)
        #
        self.LoadSprite()

    def LoadSprite(self):
        self.GUIhp = [self.GUI.get_image(2, 208, 16, 24),
                      self.GUI.get_image(70, 208, 16, 24),
                      self.GUI.get_image(20, 208, 48, 24),
                      self.GUI.get_image(0, 260, 16, 8)]
        for frame in self.GUIhp:
            frame.set_colorkey(Black)
        self.GUImenu = [self.GUI.get_image(162, 2, 16, 16),
                        self.GUI.get_image(180, 2, 16, 16),
                        self.GUI.get_image(198, 2, 16, 16),
                        self.GUI.get_image(162, 20, 16, 16),
                        self.GUI.get_image(198, 20, 16, 16),
                        self.GUI.get_image(162, 38, 16, 16),
                        self.GUI.get_image(180, 38, 16, 16),
                        self.GUI.get_image(198, 38, 16, 16),
                        self.GUI.get_image(234, 20, 16, 16)]
        for frame in self.GUImenu:
            frame.set_colorkey(Black)
        self.GUIButton = [self.buttonimg.get_image(66, 1, 44, 29)]
        for frame in self.GUIButton:
            frame.set_colorkey(Black)

    def New(self):
        # group
        self.projectile = pg.sprite.Group()
        self.sprites = pg.sprite.Group()
        self.block = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.teleport = pg.sprite.Group()
        self.attack_rect = pg.sprite.Group()
        self.collectibles = pg.sprite.Group()
        # camera
        self.camera = Camera(self.map.width, self.map.height)
        # make object
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'wall':
                block(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'spawn':
                self.jumper = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'teleport':
                teleport(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                         tile_object.properties['NextMap'], tile_object.properties['MapEntry'])
            if tile_object.name == 'collectible':
                if tile_object.properties['power'] == 'DoubleJump':
                    if s.load(s.DoubleJump) == 0:
                        self.obj1 = collectible(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                                tile_object.properties['power'])
                        self.obj1.powername = tile_object.properties['power']
                if tile_object.properties['power'] == 'WallSlide':
                    if s.load(s.WallSlide) == 0:
                        self.obj1 = collectible(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                                tile_object.properties['power'])
                        self.obj1.powername = tile_object.properties['power']
        # start loop
        if not self.playing:
            self.Loop()

    def Loop(self):
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.Event()
            self.Draw()
            self.Update()
            self.kill_object()

    def Update(self):
        self.sprites.update()
        self.attack_rect.update()
        self.camera.update(self.jumper)

    def Event(self):
        for event in pg.event.get():
            self.jumper.get_status()
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                m.running = False
            if event.type == VIDEORESIZE:
                self.screen = pg.display.set_mode(event.size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                if self.pause:
                    self.pause = False
                    self.pause = True
            if event.type == pg.KEYDOWN:
                # debug
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.running = False
                    m.running = False
                if event.key == pg.K_1:
                    self.jumper.sword_out = not self.jumper.sword_out
                    self.jumper.bow_out = False
                    self.jumper.magic_out = False
                if event.key == pg.K_2:
                    self.jumper.bow_out = not self.jumper.bow_out
                    self.jumper.sword_out = False
                    self.jumper.magic_out = False
                if event.key == pg.K_3:
                    self.jumper.magic_out = not self.jumper.magic_out
                    self.jumper.sword_out = False
                    self.jumper.bow_out = False
                if event.key == pg.K_q:
                    self.jumper.TakeDamage(-10)
                if event.key == pg.K_z:
                    self.jumper.TakeDamage(10)
                if event.key == pg.K_e:
                    if self.jumper.sword_out:
                        self.jumper.Attack(self, 'sword')
                    if self.jumper.bow_out:
                        self.jumper.Attack(self, 'bow')
                    if self.jumper.magic_out:
                        self.jumper.Attack(self, 'magic')
                    else:
                        pass
                if event.key == pg.K_w:
                    self.jumper.LookUp = True
                if event.key == pg.K_TAB:
                    if not self.pause:
                        self.pause = True
                        self.inv = True
                        self.Pause()
                    else:
                        self.pause = False
                        self.inv = False
                if event.key == pg.K_SPACE:
                    self.jumper.JUMP()

    def Draw(self):
        # make screen
        self.zoom.fill(White)
        # pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        pg.display.set_caption("{:.2f}".format(self.camera.x))
        # self.zoom.blit(self.bg, (0,0))
        self.zoom.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # draw sprite and debug
        for sprite in self.sprites:
            self.zoom.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.zoom, Yellow, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for player in self.player:
                pg.draw.rect(self.zoom, Yellow, self.camera.apply_rect(player.front_rect), 1)
            for wall in self.block:
                pg.draw.rect(self.zoom, Green, self.camera.apply_rect(wall.rect), 1)
            for teleport in self.teleport:
                pg.draw.rect(self.zoom, Blue, self.camera.apply_rect(teleport.rect), 1)
            for attack in self.attack_rect:
                pg.draw.rect(self.zoom, Red, self.camera.apply_rect(attack.rect), 1)
        # draw player hp
        draw_player_health(self.zoom, 10, 10, self.jumper.health / self.jumper.MaxHealth, self.jumper.MaxHealth, self)
        # refresh the screen
        self.screen.blit(pg.transform.scale(self.zoom, self.screen.get_rect().size), (0, 0))
        if self.pause:
            self.Pause()
        pg.display.flip()

    def kill_object(self):
        time = pg.time.get_ticks()
        if time - self.lastkill > 100:
            for rect in self.attack_rect:
                rect.kill()
            self.lastkill = time
        for rect in self.projectile:
            if Collide(rect, self.block):
                rect.kill()
            if rect.x >= self.jumper.x + 400:
                rect.kill()
            if rect.x <= self.jumper.x - 400:
                rect.kill()

    def reload(self):
        # group
        self.projectile = pg.sprite.Group()
        self.sprites = pg.sprite.Group()
        self.block = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.teleport = pg.sprite.Group()
        self.attack_rect = pg.sprite.Group()
        # camera
        self.camera = Camera(self.map.width, self.map.height)
        # make object
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'wall':
                block(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'teleport':
                teleport(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                         tile_object.properties['NextMap'], tile_object.properties['MapEntry'])

            if tile_object.name == 'entry':
                entry = self.jumper.entry
                if tile_object.properties['entry'] == self.jumper.entry:
                    self.jumper = Player(self, tile_object.x, tile_object.y)
                    if tile_object.properties['faceleft']:
                        self.jumper.FaceLeft = True

            if tile_object.name == 'collectible':
                if tile_object.properties['power'] == 'DoubleJump':
                    if s.load(s.DoubleJump) == 0:
                        self.obj1 = collectible(self, tile_object.x, tile_object.y, tile_object.width,
                                                tile_object.height)
                        self.obj1.powername = tile_object.properties['power']
                if tile_object.properties['power'] == 'WallSlide':
                    if s.load(s.WallSlide) == 0:
                        self.obj1 = collectible(self, tile_object.x, tile_object.y, tile_object.width,
                                                tile_object.height)
                        self.obj1.powername = tile_object.properties['power']

    def Pause(self):
        self.clock.tick(fps)
        # btn_setting
        inventoryWidth = int(self.screen.get_width() / 1.3)
        inventoryx = (self.screen.get_width() / 2) - (inventoryWidth / 2)
        inventoryHeight = int(self.screen.get_height() / 1.3)
        inventoryy = (self.screen.get_height() / 2) - (inventoryHeight / 2)
        buttonWidth = (self.screen.get_width() / 3)
        buttonHeight = (self.screen.get_height() / 5)
        buttonX = (self.screen.get_width() / 2) - (buttonWidth / 2)
        buttonFont = buttonHeight / 2
        self.Size = self.screen.get_size()
        # main menu
        if self.inv:
            stretchedinv1 = pg.transform.scale(self.GUImenu[0], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv2 = pg.transform.scale(self.GUImenu[1], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv3 = pg.transform.scale(self.GUImenu[2], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv4 = pg.transform.scale(self.GUImenu[3], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv5 = pg.transform.scale(self.GUImenu[4], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv6 = pg.transform.scale(self.GUImenu[5], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv7 = pg.transform.scale(self.GUImenu[6], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv8 = pg.transform.scale(self.GUImenu[7], (int(inventoryWidth / 3), int(inventoryHeight / 3)))
            stretchedinv9 = pg.transform.scale(self.GUImenu[8], (int(inventoryWidth)-2, int(inventoryHeight)-2))
            self.screen.blit(stretchedinv9, (inventoryx, inventoryy))
            self.screen.blit(stretchedinv1, (inventoryx, inventoryy))
            self.screen.blit(stretchedinv2, (int(inventoryx + (inventoryWidth/3)) -1, inventoryy))
            self.screen.blit(stretchedinv3, (int(inventoryx + 2*(inventoryWidth / 3)) - 1, inventoryy))
            self.screen.blit(stretchedinv4, (int(inventoryx), inventoryy + (inventoryHeight / 3)))
            self.screen.blit(stretchedinv5, (int(inventoryx + 2*(inventoryWidth / 3)) - 1, inventoryy + (inventoryHeight / 3)))
            self.screen.blit(stretchedinv6, (int(inventoryx), inventoryy + 2*(inventoryHeight / 3) - 1))
            self.screen.blit(stretchedinv7, (int(inventoryx + (inventoryWidth / 3)) - 1, inventoryy + 2*(inventoryHeight / 3) - 1))
            self.screen.blit(stretchedinv8, (int(inventoryx + 2*(inventoryWidth / 3)) - 1, inventoryy + 2 * (inventoryHeight / 3) - 1))

            Draw_text(self.screen, "HP : " + str(int(self.jumper.health)) + "/" + str(int(self.jumper.MaxHealth))
                      , int(buttonFont), Yellow, (inventoryx * 2.4), (inventoryy * 2))
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        self.pause = False
                        self.inv = False
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                    m.running = False
