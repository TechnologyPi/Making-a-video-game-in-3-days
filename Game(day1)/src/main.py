from tarfile import EmptyHeaderError

import pygame, sys, random
from settings import width, height, fps
from map import map_data, TILE_SIZE
from src.map import weights
from text import Text
from Enimy import Enimy

class Main_window:
    def __init__(self):
        pygame.init()

        self.camera_x = 0
        self.camera_y = 0

        self.display = pygame.display.set_mode((width, height), pygame.SCALED)
        pygame.display.set_caption("The survivor")
        self.clock = pygame.time.Clock()

        self.x = 450
        self.y = 450
        self.ply_speed = 4
        self.player_sprite = pygame.image.load("../assets/player.png").convert_alpha()
        self.health = 100
        self.stamina = 160

        self.xp_for_next_level = 40
        self.xp = 0
        self.level = 1
        self.wave = 1
        self.wave_move = -100
        self.wave_verlosity = 3

        self.weapon = "basic_pistol"
        self.weapon_look = "front"

        self.wenMIN = 3
        self.wenMAX = 5
        self.wave_gens = random.randint(self.wenMIN, self.wenMAX)

        self.camera = pygame.Vector2(0,0)

        self.wave_gen_img = pygame.image.load("../assets/player/EnemyONE_gen.png").convert_alpha()

        self.pointer  = pygame.image.load("../assets/pointer.png").convert_alpha()

        self.enimyGEN_pos = []
        for x in range(self.wave_gens):
            self.enimyGEN_pos.append(pygame.Vector2(random.randint(27, 2352*2), random.randint(27, 1003*2)))

        self.tick = 0
        self.secondTick = 0

        self.MAP_WIDTH = len(map_data[0]) * TILE_SIZE
        self.MAP_HEIGHT = len(map_data) * TILE_SIZE

        self.enimies = pygame.sprite.Group()

    def spawn_enemy(self, x, y):
        if 0 <= x <= self.MAP_WIDTH and 0 <= y <= self.MAP_HEIGHT:
            enemy = Enimy(x, y)
            self.enimies.add(enemy)

    def spawn_enemy_random(self):
        x = random.randint(50, self.MAP_WIDTH - 50)
        y = random.randint(50, self.MAP_HEIGHT - 50)
        self.spawn_enemy(x, y)

    def update(self):
        pygame.display.update()
        self.clock.tick(fps)
        #self.display.fill("white")

    def run(self):
        textures = {}
        for i in range(1,13):
            textures[i] = pygame.image.load(f"../assets/map_assets/{i}.png").convert_alpha()
            textures[i] = pygame.transform.scale(textures[i], (TILE_SIZE, TILE_SIZE))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()

            keys = pygame.key.get_pressed()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.y -= self.ply_speed
            if keys[pygame.K_s]:
                self.y += self.ply_speed
            if keys[pygame.K_a]:
                self.x -= self.ply_speed
            if keys[pygame.K_d]:
                self.x += self.ply_speed
            if keys[pygame.K_LSHIFT]:
                if self.stamina > 0:
                    self.ply_speed = 9
                    self.stamina -= 1
                else:
                    self.ply_speed = 4
            else:
                self.ply_speed = 4
                if self.stamina < 160:
                    if self.tick == 4:
                        self.stamina += 2
                if self.stamina == 161:
                    self.stamina = 160

            self.x = max(27, min(self.x, self.MAP_WIDTH + 10))
            self.y = max(27, min(self.y, self.MAP_HEIGHT + 10))

            pygame.mouse.set_visible(False)

            target_camera_x = self.x - width // 2 + 20
            target_camera_y = self.y - height // 2 + 20

            camera_speed = 0.1
            self.camera.x += (target_camera_x - self.camera.x) * camera_speed
            self.camera.y += (target_camera_y - self.camera.y) * camera_speed

            self.camera.x = max(-200, min(self.camera.x, self.MAP_WIDTH - width))
            self.camera.y = max(-200, min(self.camera.y, self.MAP_HEIGHT - height+100))

            self.display.fill((37, 37, 37))

            for y, row in enumerate(map_data):
                for x, tile in enumerate(row):
                    if tile in textures:
                        world_x = x * TILE_SIZE
                        world_y = y * TILE_SIZE
                        screen_x = world_x - self.camera.x
                        screen_y = world_y - self.camera.y
                        self.display.blit(textures[tile], (screen_x, screen_y))

            player_screen_x = width // 2 - 20
            player_screen_y = height // 2 - 20

            full_map_surface = pygame.Surface((self.MAP_WIDTH, self.MAP_HEIGHT))
            minimap_width, minimap_height = 76, 33
            minimap_surface = pygame.transform.scale(full_map_surface, (minimap_width, minimap_height))

            scale_x = minimap_width / self.MAP_WIDTH
            scale_y = minimap_height / self.MAP_HEIGHT

            player_minimap_x = int(self.x * scale_x)
            player_minimap_y = int(self.y * scale_y)
            pygame.draw.circle(minimap_surface, (255, 0, 0), (player_minimap_x, player_minimap_y), 2)

            self.player_rect = self.player_sprite.get_rect()
            self.display.blit(self.player_sprite, (player_screen_x+20, player_screen_y+20))
            self.player_rect.x = self.x# + 20
            self.player_rect.y = self.y# + 20

            Text(f"Health:{self.health}/100", (0, 0, 0), 5, 5, 20)
            Text(f"Stamina: {self.stamina}/160", (0, 0, 0), 5, 20, 20)
            Text(f'Level: {self.level} ({self.xp}/{self.xp_for_next_level} xp)', (0,0,0), 5, width-60)
            self.tick += 1
            self.secondTick += 1
            if self.tick > 5:
                self.tick = 0

            if self.secondTick > 160:
                self.secondTick = 0
            try:
                tile_x = self.x // TILE_SIZE
                tile_y = self.y // TILE_SIZE
                tile_number = map_data[tile_y][tile_x]
                if tile_number == 12:
                    self.ply_speed = 2
            except IndexError:
                pass


            for enemy_gen_pos in self.enimyGEN_pos:
                if self.secondTick == 39:
                    for x in range(self.wave_gens):
                        self.spawn_enemy_random()
                enemy_gen_minimap_x = int(enemy_gen_pos.x * scale_x)
                enemy_gen_minimap_y = int(enemy_gen_pos.y * scale_y)
                pygame.draw.circle(minimap_surface, (0, 255, 0), (enemy_gen_minimap_x, enemy_gen_minimap_y), 2)
                self.display.blit(self.wave_gen_img, (enemy_gen_pos.x - self.camera.x, enemy_gen_pos.y - self.camera.y))

            for enemy in self.enimies:
                screen_pos = (enemy.rect.x - self.camera.x, enemy.rect.y - self.camera.y)
                enemy.update(player_rect=self.player_rect)
                self.display.blit(enemy.image, screen_pos)

            self.display.blit(minimap_surface, (width - minimap_width - 10, 10))

            if isinstance(self.wave, int):
                Text(f"Wave {self.wave}", (0, 0, 0), self.wave_move, 60, 35)
                self.wave_move += self.wave_verlosity
                if self.wave_move >= width:
                    self.wave = 1.5
                if self.wave_move >= 80:
                    if self.wave_move <= 130:
                        if not self.wave_verlosity <= 1.5:
                            self.wave_verlosity -= 0.3
                    else:
                        self.wave_verlosity = 3
                else:
                    self.wave_verlosity = 3

            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.display.blit(self.pointer, (mouse_x-8, mouse_y-8))

            if mouse_y < 139:
                self.weapon_look = "back"
            if mouse_y > 179:
                self.weapon_look = "front"

            if mouse_x < 88:
                self.weapon_look = "left"
            if mouse_x > 247:
                self.weapon_look = "right"

            print(mouse_x)

            self.weapon_sprite = pygame.image.load(f"../assets/weapon/{self.weapon}/{self.weapon_look}.png").convert_alpha()
            self.display.blit(self.weapon_sprite, (width//2+16, height//2+5))

            self.update()


if __name__ == '__main__':
    main = Main_window()
    main.run()