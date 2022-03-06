import pygame
from CONST import *
from projectile import Bullet

class Player(pygame.Rect):

    def __init__(self):
        self.x = STARTING_X
        self.y = STARTING_Y
        self.h = 200
        self.w = 200
        self.kapitan = pygame.image.load(PATH_TO_KAPITAN_BOMBA)
        self.kapitan = pygame.transform.scale(self.kapitan, (self.h, self.w))
        self.moving_up = 0
        self.moving_down = 0
        self.moving_left = 0
        self.moving_right = 0
        self.projectiles = []
        self.rect = self.kapitan.get_rect()

    def update_position(self):
        if self.moving_up:
            if self.y >= 10:
                self.y -= 20
        if self.moving_down:
            if self.y <= 700:
                self.y += 20
        if self.moving_right:
            if self.x <= 700:
                self.x += 20
        if self.moving_left:
            if self.x >= 50:
                self.x -= 20

    def shoot(self):
        if len(self.projectiles) < 5:
            self.projectiles.append(Bullet(self.x+150, self.y+50))
            return True
        return False