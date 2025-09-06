import pygame
import math

class Enimy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("../assets/player/EnemyONE.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1

    def update(self, player_rect):
        dx, dy = player_rect.x - self.rect.x, player_rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed