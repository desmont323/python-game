import pygame as pg

from menu import Menu

m = Menu()

m.waiting = True
m.main_menu = True
m.wait_key()
if m.playing:
    from Game import Game

    g = Game()
    while g.running:
        g.New()
pg.quit()
