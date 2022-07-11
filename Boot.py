import pygame as pg

from menu import Menu

m = Menu()

m.waiting = True
m.main_menu = True
m.wait_key()
if m.playing:
    from Game import Game

    g = Game()
    screen = (m.screen.get_width(), m.screen.get_height())
    while g.running:
        g.New(screen)
pg.quit()
