from tarfile import EmptyHeaderError

import pygame, sys, random
from settings import width, height, fps
from map import map_data, TILE_SIZE
from src.angle_around_fixed_point import angle_to_cords
from src.map import weights
from text import Text
from Enimy import Enimy, Enemy_Spawners
from angle_around_fixed_point import get_angle
import math

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

        self.wenMIN = 2
        self.wenMAX = 4
        self.wave_gens = random.randint(self.wenMIN, self.wenMAX)

        self.camera = pygame.Vector2(0,0)

        self.wave_gen_img = pygame.image.load("../assets/player/EnemyONE_gen.png").convert_alpha()

        self.pointer  = pygame.image.load("../assets/pointer.png").convert_alpha()

        self.enimies = pygame.sprite.Group()
        self.enimie_spawners = pygame.sprite.Group()

        self.enimyGEN_pos = []
        for x in range(self.wave_gens):
            self.enimyGEN_pos.append(pygame.Vector2(random.randint(27, 2352*2), random.randint(27, 1003*2)))
            spawner = Enemy_Spawners(self.enimyGEN_pos[x][0], self.enimyGEN_pos[x][1])
            self.enimie_spawners.add(spawner)


        self.tick = 0
        self.secondTick = 0

        self.MAP_WIDTH = len(map_data[0]) * TILE_SIZE
        self.MAP_HEIGHT = len(map_data) * TILE_SIZE

        self.X_line = 0
        self.Y_line = 0

        self.hit_enemy = False
        self.hit_y = 0
        self.hit_x = 0

        self.hit_verlosity_x = -1
        self.hit_verlosity_y = -1

        self.magazeenSIZE = 6
        self.fullmagazeenSIZE = 6
        self.is_reloading = False
        self.reload_start_time = 0
        self.reload_duration = 1.8  # seconds
        self.magazeenSIZE = 0

        self.paused = False

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
        weapon = pygame.image.load("../assets/next weapon.png").convert_alpha()
        # Constants to tweak the animation behavior
        HIT_GRAVITY = 0.5
        HIT_DECAY_X = 0.04
        HIT_RESET_Y = 400  # threshold to reset animation
        HIT_INITIAL_VEL_X = -2  # Adjust for better arc
        HIT_INITIAL_VEL_Y = -8
        textures = {}
        for i in range(1,13):
            textures[i] = pygame.image.load(f"../assets/map_assets/{i}.png").convert_alpha()
            textures[i] = pygame.transform.scale(textures[i], (TILE_SIZE, TILE_SIZE))
        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.magazeenSIZE > 0:
                            if not self.is_reloading:
                                self.magazeenSIZE -= 1
                                dx = mouse_x - width//2
                                dy = mouse_y - height//2
                                length = math.hypot(dx, dy)

                                # Normalize and extend
                                if length != 0:
                                    direction = (dx / length, dy / length)
                                    extended_point = (
                                        mouse_x + direction[0] * 250,
                                        mouse_y + direction[1] * 250
                                    )
                                else:
                                    extended_point = mouse_x, mouse_y

                                shot_start = (width // 2, height // 2)
                                shot_end = extended_point
                                line = pygame.draw.line(self.display, (120, 120, 120), shot_start, shot_end, 2)

                                p1_world = (shot_start[0] + target_camera_x, shot_start[1] + target_camera_y)
                                p2_world = (shot_end[0] + target_camera_x, shot_end[1] + target_camera_y)

                                tolerance = 8  # Change this to adjust the ± range

                                for enemy in self.enimies:
                                    points = [
                                        enemy.rect.topleft,
                                        enemy.rect.topright,
                                        enemy.rect.bottomleft,
                                        enemy.rect.bottomright,
                                        enemy.rect.center,
                                        enemy.rect.midleft,
                                        enemy.rect.midright,
                                        enemy.rect.midtop,
                                        enemy.rect.midbottom,
                                    ]

                                    x1, y1 = p1_world
                                    x2, y2 = p2_world

                                    x_min = min(x1, x2) - tolerance
                                    x_max = max(x1, x2) + tolerance
                                    y_min = min(y1, y2) - tolerance
                                    y_max = max(y1, y2) + tolerance

                                    for px, py in points:
                                        if x_min <= px <= x_max and y_min <= py <= y_max:
                                            enemy.damage_enemy(6)
                                            self.hit_enemy = True
                                            self.hit_x = enemy.rect.topleft[0]
                                            self.hit_y = enemy.rect.topleft[1]
                                            self.hit_verlosity_x = -2
                                            self.hit_verlosity_y = -8
                                            break
                                    else:
                                        continue  # only runs if no break occurred
                                    break
                                for enemy in self.enimie_spawners:
                                    points = [
                                        enemy.rect.topleft,
                                        enemy.rect.topright,
                                        enemy.rect.bottomleft,
                                        enemy.rect.bottomright,
                                        enemy.rect.center,
                                        enemy.rect.midleft,
                                        enemy.rect.midright,
                                        enemy.rect.midtop,
                                        enemy.rect.midbottom,
                                    ]

                                    x1, y1 = p1_world
                                    x2, y2 = p2_world

                                    x_min = min(x1, x2) - tolerance
                                    x_max = max(x1, x2) + tolerance
                                    y_min = min(y1, y2) - tolerance
                                    y_max = max(y1, y2) + tolerance

                                    for px, py in points:
                                        if x_min <= px <= x_max and y_min <= py <= y_max:
                                            enemy.damage_enemy(6)
                                            self.hit_enemy = True
                                            self.hit_x = enemy.rect.topleft[0]
                                            self.hit_y = enemy.rect.topleft[1]
                                            self.hit_verlosity_x = -2
                                            self.hit_verlosity_y = -8
                                            break
                                    else:
                                        continue  # only runs if no break occurred
                                    break
                        else:
                            self.is_reloading = True
                            self.reload_start_time = pygame.time.get_ticks()
                            self.reload = True
            if self.paused:
                from Upgrades import get_three_random_upgrades
                self.display.fill((37, 37, 37))  # Optional: clear screen
                self.display.blit(weapon, (width // 2-50, height // 2))
                Text("Upgrade!", (255, 255, 255), width // 2 - 50, height // 2 - 40, 40)
                self.display.blit(self.pointer, (mouse_x, mouse_y))
                Weapon, Armor, Health = get_three_random_upgrades()
                #Weapon_sprite = pygame.image.load(f"../assets/weapon/{Weapon}/cover.png").convert_alpha()
                #self.display.blit(Weapon_sprite, (width // 2 - 16, height // 2-8))
                self.update()
                continue

            self.update()
            if not self.paused:
                keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.y -= self.ply_speed
            if keys[pygame.K_s]:
                self.y += self.ply_speed
            if keys[pygame.K_a]:
                self.x -= self.ply_speed
            if keys[pygame.K_d]:
                self.x += self.ply_speed
            if keys[pygame.K_r] and not self.is_reloading:
                self.is_reloading = True
                self.reload_start_time = pygame.time.get_ticks()
                self.reload = True
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

            if self.xp >= self.xp_for_next_level:
                self.paused = True
                self.level += 1
                self.xp_for_next_level = (self.level ** 3) + 40
                self.xp = 0

            if self.is_reloading:
                now = pygame.time.get_ticks()
                elapsed_time = (now - self.reload_start_time) / 1000  # convert to seconds
                progress = elapsed_time / self.reload_duration

                # Compute how many bullets should be added
                bullets_to_reload = int(progress * self.fullmagazeenSIZE)

                # Ensure we don't overfill
                bullets_to_add = min(bullets_to_reload, self.fullmagazeenSIZE - self.magazeenSIZE)
                self.magazeenSIZE += bullets_to_add

                # Restart time if bullets were added to avoid double-adding
                if bullets_to_add > 0:
                    self.reload_start_time = now

                print(f"Reloading: {self.magazeenSIZE}/{self.fullmagazeenSIZE}")

                # Stop reloading when full
                if self.magazeenSIZE >= self.fullmagazeenSIZE:
                    self.magazeenSIZE = self.fullmagazeenSIZE
                    self.is_reloading = False


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
            if self.tick > 20:
                self.tick = 0

            if self.secondTick > 190*2:
                self.secondTick = 0
            try:
                tile_x = self.x // TILE_SIZE
                tile_y = self.y // TILE_SIZE
                tile_number = map_data[tile_y][tile_x]
                if tile_number == 12:
                    self.ply_speed = 2
            except IndexError:
                pass


            if not self.paused:
                for enemy_gen_pos in self.enimyGEN_pos:
                    if self.secondTick == 39:
                        for x in range(len(self.enimie_spawners)):
                            self.spawn_enemy_random()
                    enemy_gen_minimap_x = int(enemy_gen_pos.x * scale_x)
                    enemy_gen_minimap_y = int(enemy_gen_pos.y * scale_y)
                    pygame.draw.circle(minimap_surface, (0, 255, 0), (enemy_gen_minimap_x, enemy_gen_minimap_y), 2)

                for enemy_gen_pos in self.enimie_spawners:
                    output = enemy_gen_pos.update()
                    screen_pos = (enemy_gen_pos.rect.x - self.camera.x, enemy_gen_pos.rect.y - self.camera.y)
                    self.display.blit(enemy_gen_pos.image, screen_pos)
                    try:
                        if output[:2] == "xp":
                            self.xp += int(output[2:])
                    except TypeError:
                        pass

                for enemy in self.enimies:
                    screen_pos = (enemy.rect.x - self.camera.x, enemy.rect.y - self.camera.y)
                    damaged = enemy.update(self.player_rect, self.enimies)
                    if damaged == "damage":
                        if self.tick == 3:
                            self.health -= 3
                    try:
                        if damaged[:2] == "xp":
                            self.xp += int(damaged[2:])
                    except TypeError:
                        pass
                    self.display.blit(enemy.image, screen_pos)

            self.display.blit(minimap_surface, (width - minimap_width - 10, 10))

            if len(self.enimie_spawners) == 0:
                self.wave += 1
                self.wave = int(self.wave)
                print(self.wave)
                self.wave_move = -100

                self.enimies = pygame.sprite.Group()
                self.enimie_spawners = pygame.sprite.Group()

                self.wenMIN *= 1.5
                self.wenMAX *= 1.5
                self.wave_gens = random.randint(int(self.wenMIN), int(self.wenMAX))

                self.enimyGEN_pos = []
                for x in range(self.wave_gens):
                    self.enimyGEN_pos.append(pygame.Vector2(random.randint(27, 2352 * 2), random.randint(27, 1003 * 2)))
                    spawner = Enemy_Spawners(self.enimyGEN_pos[x][0], self.enimyGEN_pos[x][1])
                    self.enimie_spawners.add(spawner)

            if isinstance(self.wave, int):
                Text(f"Wave {self.wave}", (0, 0, 0), self.wave_move, 60, 35)
                self.wave_move += self.wave_verlosity
                if self.wave_move >= width:
                    self.wave = self.wave + 0.5
                if self.wave_move >= 80:
                    if self.wave_move <= 130:
                        if not self.wave_verlosity <= 1.5:
                            self.wave_verlosity -= 0.3
                    else:
                        self.wave_verlosity = 3
                else:
                    self.wave_verlosity = 3

            self.display.blit(self.pointer, (mouse_x-8, mouse_y-8))

            if mouse_y < 139:
                self.weapon_look = "back"
            if mouse_y > 179:
                self.weapon_look = "front"

            if mouse_x < 88:
                self.weapon_look = "left"
            if mouse_x > 247:
                self.weapon_look = "right"

            if self.magazeenSIZE == 0:
                if self.secondTick >= 40:
                    Text("Press R to reload!", (255, 0, 0), 110, 50)


            self.weapon_sprite = pygame.image.load(f"../assets/weapon/{self.weapon}/{self.weapon_look}.png").convert_alpha()
            self.display.blit(self.weapon_sprite, (width//2+16, height//2+5))

            Text(f"Bullets:{self.magazeenSIZE}/{self.fullmagazeenSIZE}", (0,0,0), 5, width-80)

            # Animation update
            if self.hit_enemy:
                Text("6", (0, 0, 0), self.hit_x - self.camera.x, self.hit_y - self.camera.y, 25)

                self.hit_x += self.hit_verlosity_x+random.uniform(0.24, 0.67)-0.45
                self.hit_y += self.hit_verlosity_y+random.uniform(0.24, 0.67)-0.45

                self.hit_verlosity_x += HIT_DECAY_X  # slows horizontal movement
                self.hit_verlosity_y += HIT_GRAVITY  # gravity effect

                if self.hit_y >= HIT_RESET_Y:
                    if self.secondTick == 120:
                        self.hit_enemy = False

            self.update()


if __name__ == '__main__':
    main = Main_window()
    main.run()