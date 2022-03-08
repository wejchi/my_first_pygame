import pygame
import sys
from CONST import *
from player import Player
from enemy import Enemy
from explosion import Explosion
#from model import get_model
#import numpy as np
#import pandas as pd
#import tensorflow as tf
#import matplotlib.pyplot as plt


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.dt = 1
        pygame.init()
        pygame.mixer.init()
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.player = Player()
        # load background
        self.background = pygame.image.load(PATH_TO_BACKGROUND)
        self.background = pygame.transform.scale(self.background, RESOLUTION)
        # load kpt
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption('Kapitan')
        self.buffer = None
        self.score = 0
        self.enemies = []
        self.explosions = []
        self.score_round = 0
        self.projectiles = []
        # self.input_as_numpy = np.array([0, 0, 0, 0, 0])

    def play_music(self):
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)

    def ai_input(self):
        self.score_round = 0 
        screen = pygame.surfarray.array3d(self.buffer)
        screen = screen.swapaxes(0, 1)
        # screen = pygame.image.tostring(self.buffer, 'RGB', False)
        # screen = Image.frombytes('RGB', self.buffer.get_size(), screen)
        # screen = tf.keras.utils.img_to_array(screen)
        screen = tf.image.resize(screen, (512, 512))
        # screen = (screen - tf.math.reduce_mean(screen))/255
        # print(screen)
        
        rand = self.model.predict(screen[tf.newaxis])
        rand = rand[0]
        print(rand)
        # print(screen.shape)
        # print(type(screen))
        self.player.moving_up = rand[0] > 0.5
        self.player.moving_down = rand[1] > 0.5
        self.player.moving_right = rand[2] > 0.5
        self.player.moving_left = rand[3] > 0.5
        if rand[4] > 0.5:
            if self.player.shoot():
                self.score_round -= 10
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
        # self.player.update_position()

    def play_with_ai(self):
        self.model = tf.keras.models.load_model('kapitan_model')
        self.play_music()
        i = 0
        while True:
            if len(self.enemies) < 2:
                self.enemies.append(Enemy(self))
            self.draw()
            self.refresh_screen(2000)
            self.ai_input()
            self.logic()

    def play_and_record(self, max_length: int):
        self.moving_left = []
        self.moving_up = []
        self.moving_right = []
        self.moving_down = []
        self.shooting = []
        self.play_music()
        self.img_names = []
        for i in range(max_length):
            if len(self.enemies) < 2:
                self.enemies.append(Enemy(self))
            self.draw()
            self.refresh_screen(60)
            self.prepare_input_to_save()
            name = f'training/img{i}.jpg'
            pygame.image.save(self.buffer, name)
            self.img_names.append(name)
            self.logic()
        data = {'img': self.img_names, 'moving_left': self.moving_left,
                'moving_up': self.moving_up, 'moving_right': self.moving_right,
                'moving_down': self.moving_down, 'shooting': self.shooting}
        pd.DataFrame(data).to_csv('training/df')

    def prepare_input_to_save(self):
        shooting = 0
        self.score_round = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.moving_up = 1
                  #  self.moving_up.append(1)
                elif event.key == pygame.K_DOWN:
                    self.player.moving_down = 1
                   # self.moving_down.append(1)
                elif event.key == pygame.K_RIGHT:
                    self.player.moving_right = 1
                    #self.moving_right.append(1)
                elif event.key == pygame.K_LEFT:
                    self.player.moving_left = 1
                   # self.moving_left.append(1)
                elif event.key == pygame.K_ESCAPE:
                    self.close()
                elif event.key == pygame.K_SPACE:
                    if self.player.shoot():
                        shooting = 1
                        self.score_round -= 10

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player.moving_up = 0
                   # self.moving_up.append(0)
                elif event.key == pygame.K_DOWN:
                    self.player.moving_down = 0
                    #self.moving_down.append(0)
                elif event.key == pygame.K_RIGHT:
                    self.player.moving_right = 0
                    #self.moving_right.append(0)
                elif event.key == pygame.K_LEFT:
                    self.player.moving_left = 0
                    #self.moving_left.append(0)
        self.shooting.append(shooting)
        self.moving_left.append(self.player.moving_left)
        self.moving_up.append(self.player.moving_up)
        self.moving_right.append(self.player.moving_right)
        self.moving_down.append(self.player.moving_down)

    def play_game(self):
        # self.play_music()
        while True:
            if len(self.enemies) < 2:
                self.enemies.append(Enemy(self))
            self.draw()
            self.refresh_screen(FRAMERATE)
            self.check_events()
            self.logic()

    def logic(self):
        self.player.update_position()
        for enemy in self.enemies:
            enemy.move_enemy()
            enemy.shoot()
            if enemy.x < -100:
                self.enemies.remove(enemy)
                continue
        for projectile in self.projectiles.copy():
            if projectile.colliderect(self.player):
                self.score_round -= 50
                self.explosions.append(Explosion(projectile.x - 20,
                                                 projectile.y - 20))
                self.projectiles.remove(projectile)
            projectile.move_projectile()
            if projectile.x < -100:
                self.projectiles.remove(projectile)
        for bullet in self.player.projectiles:
            bullet.move_projectile()
            if bullet.x > 1800:
                self.player.projectiles.remove(bullet)
                continue
            for enemy in self.enemies:
                if bullet.colliderect(enemy):
                    self.score_round += 100
                    self.explosions.append(Explosion(bullet.x + 20,
                                                     bullet.y - 20))
                    self.enemies.remove(enemy)
                    self.player.projectiles.remove(bullet)
        for explosion in self.explosions:
            if explosion.frames < 0:
                self.explosions.remove(explosion)
            else:
                explosion.frames -= 1
        self.score += self.score_round

    def refresh_screen(self, FPS):
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.update()
        self.dt = self.clock.tick(FPS) * FPS / 1000

    def draw(self):
        self.buffer = pygame.Surface(RESOLUTION)
        self.buffer.blit(self.background, (0, 0))
        self.buffer.blit(self.player.kapitan, self.player)
        for enemy in self.enemies:
            self.buffer.blit(enemy.enemy,
                             enemy)
        for projectile in self.projectiles:
            self.buffer.blit(projectile.img,
                             projectile)
        for projectile in self.player.projectiles:
            self.buffer.blit(projectile.img,
                             projectile)
        for explosion in self.explosions:
            self.buffer.blit(explosion.img,
                             explosion)
        score_str = f'wynik : {self.score}'
        label = self.myfont.render(score_str, 2, (255, 255, 0))
        self.buffer.blit(label, (0, 0))

    @staticmethod
    def close():
        pygame.quit()
        sys.exit(0)

    def check_events(self):
        self.score_round = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.moving_up = 1
                elif event.key == pygame.K_DOWN:
                    self.player.moving_down = 1
                elif event.key == pygame.K_RIGHT:
                    self.player.moving_right = 1
                elif event.key == pygame.K_LEFT:
                    self.player.moving_left = 1
                elif event.key == pygame.K_ESCAPE:
                    self.close()
                elif event.key == pygame.K_SPACE:
                    self.player.shoot()
                    self.score_round -= 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player.moving_up = 0
                elif event.key == pygame.K_DOWN:
                    self.player.moving_down = 0
                elif event.key == pygame.K_RIGHT:
                    self.player.moving_right = 0
                elif event.key == pygame.K_LEFT:
                    self.player.moving_left = 0
        # self.player.update_position()


if __name__ == '__main__':
    game = Game()
    #game.play_and_record(10000)
    game.play_game()
