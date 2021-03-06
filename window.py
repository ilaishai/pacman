import pygame, sys, random
from pygame.locals import *
import time
from player import Player
from ghost import Ghost
from map import Map


class Window:

    def __init__(self, surface, player, inky, blinky, pinky, clyde, map, size = 10):
        self.surface = surface
        self.player = player
        self.inky = inky
        self.blinky = blinky
        self.pinky = pinky
        self.clyde = clyde
        self.map = map
        self.size = size

    def switch_color(self, mode):
        inky = self.inky
        blinky = self.blinky
        pinky = self.pinky
        clyde = self.clyde
        if mode:
            inky.color = (0, 0, 255)
            blinky.color = (0, 0, 255)
            pinky.color = (0, 0, 255)
            clyde.color = (0, 0, 255)
        else:
            self.player.eats = False
            inky.color = (0, 255, 255)
            blinky.color = (255, 0, 0)
            pinky.color = (255, 102, 255)
            clyde.color = (255, 128, 0)

    # finds the type of key that was pressed and assigns a function
    def keytype(self, keys):
        player = self.player
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.turnnext = "up"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.turnnext = "lft"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.turnnext = "dn"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.turnnext = "rt"
        if keys[pygame.K_0]:
            print("(" + str(player.xloc) + "," + str(player.yloc) + ")")
        if keys[pygame.K_o]:
            player.score += 1000
        return player.turnnext

    def endgame(self):
        self.player.yloc = 10
        cover = pygame.rect.Rect(0, 0, 38 * self.size, 48 * self.size)
        pygame.draw.rect(self.surface, (0, 0, 0), cover)
        font = pygame.font.SysFont("franklingothicbook", int(self.size) * 5)
        if not self.player.dead:
            scoreboard = font.render("YOU WON," + str(self.player.score), True, (255, 255, 255))
        else:
            scoreboard = font.render("YOU ARE DEAD", True, (255, 255, 255))
        return scoreboard, 1

    def event(self, event):
        if event.type == QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            self.player.turnnext = self.keytype(keys)

    def action(self, ghosts, pointgrid):
        from main import collide
        if self.player.turn == "lft" and self.player.xloc <= 10:
            self.player.xloc = 380
        elif self.player.turn == "rt" and self.player.xloc >= 370:
            self.player.xloc = 0
        if self.player.turnnext in collide(self.surface, self.player.xloc, self.player.yloc):
            self.player = self.player.move(self.player.turnnext, self.size)
            self.player.turn = self.player.turnnext
        else:
            self.player = self.player.move(self.player.turn, self.size)
        ghosts[3].chase = True
        for i in range(4):
            ghosts[i].ghost_touch(self.player)
            if 170 <= ghosts[i].xloc <= 210 and 210 <= ghosts[i].yloc <= 250 and ghosts[i].chase:
                ghosts[i].ghost_start(self.size)
        ghosts[3] = ghosts[3].ghost_randpath(self.size)
        if self.player.ate_all(pointgrid) <= 120:
            if random.randint(1, 50) < 25:
                ghosts[2] = ghosts[2].ghost_randpath(self.size)
            else:
                ghosts[2] = ghosts[2].ghost_path(self.player, self.size)
            ghosts[2].chase = True
        if self.player.ate_all(pointgrid) <= 100:
            ghosts[0].chase = True
            if random.randint(1, 50) < 25:
                ghosts[0] = ghosts[0].ghost_randpath(self.size)
            else:
                ghosts[0] = ghosts[0].ghost_path(self.player, self.size)
        if self.player.ate_all(pointgrid) <= 75:
            ghosts[1].chase = True
            ghosts[1] = ghosts[1].ghost_path(self.player, self.size)

        return ghosts
