import pygame
from CONST import *


class Explosion(pygame.Rect):
    img = pygame.image.load(PATH_TO_EXPLOSION)
    img = pygame.transform.scale(img, (80, 80))

    def __init__(self, x, y, img = img):
        self.img = img
        self.x = x
        self.y = y
        self.frames = 10
