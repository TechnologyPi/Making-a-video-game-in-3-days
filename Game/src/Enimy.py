import random
import pygame
import math

class Enimy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("../assets/player/EnemyONE.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 0.5
        self.past_rect = self.rect
        self.enemy_health = 12
        self.xp = 8

    def damage_enemy(self, damage):
        self.enemy_health -= damage

    def update(self, player_rect, enemies):
        if self.enemy_health <= 0:
            self.kill()
            return "xp" + str(self.xp)
        dx, dy = player_rect.x - self.rect.x, player_rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        for other in enemies:
            if other is not self and self.rect.colliderect(other.rect):
                overlap_x = (self.rect.width + other.rect.width) / 2 - abs(self.rect.centerx - other.rect.centerx)
                overlap_y = (self.rect.height + other.rect.height) / 2 - abs(self.rect.centery - other.rect.centery)

                if overlap_x > 0 and overlap_y > 0:
                    # Push apart in the axis of least penetration
                    if overlap_x < overlap_y:
                        if self.rect.centerx < other.rect.centerx:
                            self.rect.x -= overlap_x / 2
                            other.rect.x += overlap_x / 2
                        else:
                            self.rect.x += overlap_x / 2
                            other.rect.x -= overlap_x / 2
                    else:
                        if self.rect.centery < other.rect.centery:
                            self.rect.y -= overlap_y / 2
                            other.rect.y += overlap_y / 2
                        else:
                            self.rect.y += overlap_y / 2
                            other.rect.y -= overlap_y / 2
        if dist > 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * (self.speed + random.uniform(0.25,3))
            self.rect.y += dy * (self.speed + random.uniform(0.25,3))
        self.past_rect = self.rect
        if self.rect.colliderect(player_rect):
            return "damage"
        else:
            return None

class Enemy_Spawners(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("../assets/player/EnemyONE_gen.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.enemy_health = 36
        self.xp = 24

    def damage_enemy(self, damage):
        self.enemy_health -= damage

    def update(self):
        if self.enemy_health <= 0:
            self.kill()
            return "xp" + str(self.xp)
        else:
            return None