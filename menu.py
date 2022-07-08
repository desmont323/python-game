from pygame.locals import *
from Import import SpriteSheet
from os import path
from SaveManager import *
from Utilities import *


class Menu:

    def __init__(self):
        self.Size = Size
        self.playing = False
        self.waiting = False
        self.main_menu = False
        self.save_selection = False
        self.option_menu = False
        self.exit_confirm = False
        self.setting = False
        self.save = ""
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(Size, RESIZABLE)
        self.zoom = self.screen.copy()
        self.clock = pg.time.Clock()
        self.game_folder = path.dirname(__file__)
        self.buttonimg = SpriteSheet(path.join(self.game_folder, 'sprites/buttons_2x.png'))
        self.GUIButton = [self.buttonimg.get_image(66, 2, 44, 28)]
        for frame in self.GUIButton:
            frame.set_colorkey(Black)

    def wait_key(self):
        while self.waiting:
            self.clock.tick(fps)
            self.screen.fill(White)
            # btn_setting
            buttonWidth = (self.screen.get_width() / 3)
            buttonHeight = (self.screen.get_height() / 5)
            buttonX = (self.screen.get_width() / 2) - (buttonWidth / 2)
            buttonFont = buttonHeight / 2
            self.Size = self.screen.get_size()
            # main menu
            if self.main_menu:
                # TODO draw game name still need to find and replace by stretching sprite
                Draw_text(self.screen, 'GAME NAME', 50, Yellow, (self.screen.get_width() / 2), 0)
                btn_play = Button('play', buttonX, (self.screen.get_height() / 5.5), buttonWidth, buttonHeight, Yellow,
                                  self)
                btn_option = Button('option', buttonX, (self.screen.get_height() / 2.5), buttonWidth, buttonHeight,
                                    Yellow, self)
                btn_exit = Button('exit', buttonX, (self.screen.get_height() / 1.61), buttonWidth, buttonHeight,
                                  Yellow, self)
                Button.draw(btn_play, self.screen, int(buttonFont))
                Button.draw(btn_option, self.screen, int(buttonFont))
                Button.draw(btn_exit, self.screen, int(buttonFont))
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        if btn_play.click(pos):
                            self.main_menu = False
                            self.save_selection = True
                        if btn_option.click(pos):
                            self.main_menu = False
                            self.option_menu = True
                        if btn_exit.click(pos):
                            self.main_menu = False
                            self.exit_confirm = True
                    if event.type == pg.QUIT:
                        self.waiting = False
                        self.running = False
            # save selection
            if self.save_selection:
                btn_save1 = Button('save 1', buttonX, (self.screen.get_height() / 5.5), buttonWidth, buttonHeight,
                                   Yellow, self)
                btn_save2 = Button('save 2', buttonX, (self.screen.get_height() / 2.5), buttonWidth, buttonHeight,
                                   Yellow, self)
                btn_save3 = Button('save 3', buttonX, (self.screen.get_height() / 1.61), buttonWidth, buttonHeight,
                                   Yellow, self)
                btn_return = Button('return', buttonX / 3, (self.screen.get_height() / 1.2), buttonWidth / 2,
                                    buttonHeight / 2, Yellow, self)
                Button.draw(btn_save1, self.screen, int(buttonFont))
                Button.draw(btn_save2, self.screen, int(buttonFont))
                Button.draw(btn_save3, self.screen, int(buttonFont))
                Button.draw(btn_return, self.screen, int(buttonFont))
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        if btn_save1.click(pos):
                            save1(saves, 'save_1.xml')
                            save()
                            self.save_selection = False
                            self.waiting = False
                            self.playing = True
                        if btn_save2.click(pos):
                            save1(saves, 'save_2.xml')
                            save()
                            self.save_selection = False
                            self.waiting = False
                            self.playing = True
                        if btn_save3.click(pos):
                            save1(saves, 'save_3.xml')
                            save()
                            self.save_selection = False
                            self.waiting = False
                            self.playing = True
                        if btn_return.click(pos):
                            self.main_menu = True
                            self.save_selection = False
                    if event.type == pg.QUIT:
                        self.waiting = False
                        self.running = False

            if self.option_menu:
                # TODO same as game name in main menu need to stretch
                Draw_text(self.screen, 'there is no option yet', 50, Black, (self.screen.get_width() / 2), 20)
                btn_ok = Button('OK', buttonX, (self.screen.get_height() / 2.5), buttonWidth, buttonHeight,
                                Yellow, self)
                Button.draw(btn_ok, self.screen, int(buttonFont))
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        if btn_ok.click(pos):
                            self.option_menu = False
                            self.main_menu = True
                    if event.type == pg.QUIT:
                        self.waiting = False
                        self.running = False

            if self.exit_confirm:
                # TODO same as game name in main menu need to stretch
                Draw_text(self.screen, 'are you sure you want to quit ?', 50, Black, (self.screen.get_width() / 2), 20)
                btn_yes = Button('YES', (buttonX - buttonX / 1.5), (self.screen.get_height() / 2.5), buttonWidth,
                                 buttonHeight, Yellow,
                                 self)
                btn_no = Button('NO', (buttonX + buttonX / 1.5), (self.screen.get_height() / 2.5), buttonWidth,
                                buttonHeight, Yellow,
                                self)
                Button.draw(btn_yes, self.screen, int(buttonFont))
                Button.draw(btn_no, self.screen, int(buttonFont))
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        if btn_yes.click(pos):
                            self.exit_confirm = False
                            self.waiting = False
                            self.running = False
                        if btn_no.click(pos):
                            self.exit_confirm = False
                            self.main_menu = True
                    if event.type == pg.QUIT:
                        self.waiting = False
                        self.running = False

            pg.display.flip()
