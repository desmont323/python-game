import pygame as pg

Title = 'jumper'
Width = 500
Height = 300
Size = (Width, Height)
#
fps = 60
tilesize = 32
gridwidth = Width / tilesize
gridheight = Height / tilesize
#
Player_acc = 0.3
Player_friction = -0.12
Player_jump = 15
Player_grav = 0.9
Player_hit_rect = pg.Rect(0, 0, 10, 29)
Front_Hit_rect = pg.Rect(0, 0, 10, 29)
#
sword_damage = 25
sword_kb = 150
#
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Lightgray = (100, 100, 100)
Yellow = (255, 255, 0)
