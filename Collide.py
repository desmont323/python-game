from os import path

import pygame as pg

from tiledmap import TiledMap
from SaveManager import *

s = save()


def collide_front_rect(one, two):
    return one.front_rect.colliderect(two.rect)


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def CollideWall(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.x
            sprite.Wall_Collide = True
        else:
            sprite.Wall_Collide = False
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.OnGround = True
                sprite.y = hits[0].rect.top - sprite.hit_rect.height
            if sprite.vel.y < 0:
                sprite.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.hit_rect.y = sprite.y
        if not hits:
            sprite.OnGround = False


def Collide_teleport(sprite, game, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        teleport = pg.sprite.spritecollide(sprite, group, False)
        tp1 = teleport[0]
        sprite.entry = tp1.entry
        location = tp1.map
        game.map = TiledMap(path.join(game.game_folder, location))
        game.map_img = game.map.make_map()
        game.map_rect = game.map_img.get_rect()
        game.reload()
        return True


def power(sprite, game, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        object = pg.sprite.spritecollide(sprite, group, True)
        powerup = object[0]
        if powerup.powername == 'DoubleJump':
            s.save(s.DoubleJump, 1, load1(saves))
            sprite.canDoubleJump = True
        if powerup.powername == 'WallSlide':
            s.save(s.WallSlide, 1, load1(saves))
            sprite.canWallSlide = True


def WallSlide(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_front_rect)
    keys = pg.key.get_pressed()
    if keys[pg.K_a] or keys[pg.K_d]:
        if hits and sprite.vel.y > 0:
            sprite.Wall_Slide = True
        else:
            sprite.Wall_Slide = False
    else:
        sprite.Wall_Slide = False


def Collide(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        return True
    else:
        return False
