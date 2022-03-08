import pygame
from CONST import *
import random
from projectile import Laser

class Enemy(pygame.Rect):
    img = pygame.image.load(PATH_TO_ENEMY)
    img = pygame.transform.scale(img, (200, 100))
    def __init__(self, game, img = img):
        self.x = 2000
        self.y = int(random.uniform(0, 700))
        self.h = 100
        self.w = 200
        self.game = game
        # self.enemy = pygame.image.load(PATH_TO_KURVINOX)
        # self.enemy = pygame.transform.scale(self.enemy, (self.h, self.w))
        self.enemy = img
        self.moving_speed = random.uniform(3, 10)
        self.projectiles = []
        self.wait = 0

    def move_enemy(self):
        self.x -= self.moving_speed

    def shoot(self):
        if self.wait > 0:
            self.wait -=1
        else:
            self.game.projectiles.append(Laser(self.x, self.y+25))
            self.wait = 90
