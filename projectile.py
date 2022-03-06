import pygame
from CONST import *


class Laser(pygame.Rect):
    # img = pygame.image.load(PATH_TO_LASER)
    # img = pygame.transform.scale(img, (self.w, self.h))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 10
        self.w = 40
        self.speed = 20
        self.img = pygame.image.load(PATH_TO_LASER)
        self.img = pygame.transform.scale(self.img, (self.w, self.h))

    def move_projectile(self):
        self.x -= self.speed

class Bullet(pygame.Rect):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 10
        self.w = 40
        self.speed = 20
        self.img = pygame.image.load(PATH_TO_BULLET)
        self.img = pygame.transform.scale(self.img, (self.w, self.h))

    def move_projectile(self):
        self.x += self.speed
