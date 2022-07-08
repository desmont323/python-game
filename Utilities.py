import pygame as pg
from Setting import *
pg.font.init()


class Button:
    def __init__(self, text, x, y, width, height, color, game):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.game = game

    def draw(self, win, fontsize):
        #pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        self.width = int(self.width)
        self.height = int(self.height)
        stretchedbutton = pg.transform.scale(self.game.GUIButton[0], (self.width, self.height))

        font = pg.font.SysFont("comicsans", fontsize)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(stretchedbutton, (self.x, self.y))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def Draw_text(screen, text, size, color, x, y):
    font = pg.font.SysFont("comicsans", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def draw_player_health(surf, x, y, pct, maxhp, game):

    if pct < 0:
        pct = 0
    BAR_LENGTH = maxhp * 0.5
    BAR_HEIGHT = 20
    stretchedbar = pg.transform.scale(game.GUIhp[2], (int(BAR_LENGTH) - 16, 24))
    stretchedhp = pg.transform.scale(game.GUIhp[3], (int(pct * BAR_LENGTH), 8))
    game.zoom.blit(stretchedhp, (x + 8, y + 8))
    game.zoom.blit(game.GUIhp[0], (x, y))
    game.zoom.blit(game.GUIhp[1], (x + BAR_LENGTH, y))
    game.zoom.blit(stretchedbar, (x + 16, y))
    # self.zoom.blit(sprite.image, self.camera.apply(sprite))
