import pygame as pg


class SpriteSheet:
    def __init__(self, filename):
        self.spriteSheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spriteSheet, (0, 0), (x, y, 100, 100))
        return image
