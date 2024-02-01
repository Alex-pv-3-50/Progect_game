import math
import pygame
import os


flag_end_game = False

center_x, center_y = 600, 400
running = True

rectlowx1 = center_x * 0.9
rectlowx2 = center_x * 0.9 + center_x * 0.28
rectlowy1 = center_y * 0.93
rectlowy2 = center_y * 0.93 + center_y * 0.1

rectmiddlex1 = center_x * 0.9
rectmiddlex2 = center_x * 0.9 + center_x * 0.28
rectmiddley1 = center_y * 0.6
rectmiddley2 = center_y * 0.6 + center_y * 0.1

recthighx1 = center_x * 0.9
recthighx2 = center_x * 0.9 + center_x * 0.28
recthighy1 = center_y * 0.77
recthighy2 = center_y * 0.77 + center_y * 0.1

rectbackx1 = center_x * 0.89
rectbackx2 = center_x * 0.89 + center_x * 0.25
rectbacky1 = center_y * 1.37
rectbacky2 = center_y * 1.37 + center_y * 0.09

flag_btn = True
flag_dsrp = False
flag_story = False
flag_start_game = False


flag1 = False
flag2 = False
flag_gutend = False
flag_pult = False
flag_dos = False
case_far = False
false_case1 = ""
count = -1
list_of_pics = [pygame.image.load('pic1.png'), pygame.image.load('pic2.png'), pygame.image.load('pic3.png'),
                pygame.image.load('pic4.png'),pygame.image.load('pic5.png'),pygame.image.load('pic6.png')]


pult = list_of_pics[4]
pult = pygame.transform.scale(pult, (200, 300)) 


# game settings
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PENTA_HEIGHT = 5 * HEIGHT
DOUBLE_HEIGHT = 2 * HEIGHT
FPS = 60
TILE = 100
FPS_POS = (WIDTH - 65, 5)

# minimap settings
MINIMAP_SCALE = 5
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_SCALE = 3 * MINIMAP_SCALE # 1 -> 12 x 8, 2 -> 24 x 16, 3 -> 36 x 24
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MINIMAP_SCALE)

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# sprite settings
DOUBLE_PI = math.pi * 2
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 100
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS

# texture settings (1200 x 1200)
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# player settings
player_pos = (HALF_WIDTH // 4, HALF_HEIGHT - 50)
player_angle = 0
player_speed = 5

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)
DARKBROWN = (97, 61, 25)
DARKORANGE = (255, 140, 0)



sc = pygame.display.set_mode((WIDTH, HEIGHT))







_ = False
matrix_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 5, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, 4, _, _, 4, _, 5, _, _, _, _, _, 5, 5, _, _, _, 5, 2, _, 1],
    [1, _, _, 4, 5, _, _, 1, 2, 3, 3, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, _, _, _, _, 5, 5, _, _, _, _, _, _, _, _, _, _, _, _, 2, 1],
    [1, _, _, 6, 4, _, _, _, _, _, _, 1, _, _, _, _, _, 5, 5, 3, _, _, _, 4, 2, _, _, _, _, _, _, _, 5, _, _, _, _, _, 4, 1, _, _, _, _, _, 3, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, 10, 2, 2, _, _, _, 5, 4, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, 4, 4, 4, _, _, _, _, _, 1],
    [1, _, _, 4, 7, _, _, _, _, _, 5, 3, _, _, _, _, _, 1, 2, 4, _, _, _, _, 1, _, _, _, _, _, _, _, 3, 4, 4, 1, 2, 2, _, _, _, _, 1, _, _, _, _, 1],
    [1, _, _, 2, 5, 1, 4, _, _, _, 4, 4, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, 3, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 3, 4, _, _, _, _, _, 2, _, _, _, _, _, _, _, 2, _, _, _, 2, _, _, _, _, _, _, 1, _, _, _, _, 2, _, _, _, _, 3, 1, _, _, _, 1],
    [1, _, _, _, _, _, 2, 5, _, _, _, _, _, 3, _, _, _, _, _, _, _, 1, _, _, 4, 4, 4, _, 1, 2, _, _, 4, _, _, _, _, _, _, _, _, _, 3, 1, _, _, _, 1],
    [1, _, _, 4, 2, _, _, _, _, _, 2, 4, _, _, 4, 3, _, 4, 4, _, 3, 3, _, _, _, 1, _, _, 3, 4, _, 1, _, _, _, _, _, _, 4, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 4, _, _, _, _, _, 4, 2, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 3, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, 1, _, _, 1, 3, _, _, _, _, _, 1, _, _, 1, 1, _, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, _, _, _, 3, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, 7, _, _, 3, 3, _, _, 2, _, _, 2, _, _, 10, 3, _, _, _, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 2, 3, _, _, _, _, _, _, _, _, 3, _, 3, 5, _, 9, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, 4, _, _, _, _, 1],
    [1, _, _, 1, 3, _, 4, 5, _, _, _, _, _, _, _, 5, _, _, 2, _, _, _, 1, 3, _, _, _, _, _, _, _, _, _, _, 3, 4, 10, 8, _, _, _, 1, 3, _, _, _, _, 1],
    [1, _, _, 3, 4, _, _, _, 8, _, _, _, _, _, _, 3, _, 4, 4, _, _, _, _, 3, _, _, _, _, 1, 1, _, _, _, _, 2, 6, 9, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 6, 1, _, _, 6, 5, _, _, _, _, _, 5, _, _, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, 6, _, _, _, 4, 2, _, _, 9, 8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, 4, _, _, _, _, _, _, _, _, _, _, _, _, 5, 4, _, _, 1],
    [1, _, 8, 4, 6, 4, _, _, _, _, _, 2, _, _, _, _, _, 1, 6, _, _, _, 2, _, _, _, _, 5, 5, _, _, 4, 5, _, _, _, _, _, _, _, _, _, _, 6, 3, _, _, 1],
    [1, _, _, _, _, 4, 2, _, _, _, 4, 1, _, _, _, _, _, 7, 8, _, _, 4, _, _, _, _, _, 1, 5, _, _, 4, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 5, 3, _, _, _, 2, 1, _, _, _, _, _, _, 1, _, _, 3, 3, _, _, _, _, _, _, _, _, _, _, _, _, 3, 4, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 1, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, _, _, _, 2, 3, _, 2, _, _, _, _, 4, 3, _, _, _, _, _, _, 4, _, _, 1, 5, _, _, _, _, _, 1],
    [1, _, 5, 2, 3, 2, 1, _, _, _, _, _, _, _, 1, 4, _, 2, _, _, 2, _, _, _, _, 4, _, _, _, _, 4, 10, _, _, _, _, 1, _, _, _, 5, 4, _, _, _, _, _, 1],
    [1, _, _, _, _, 4, 3, _, _, _, 3, 4, _, _, 2, 5, _, _, _, _, _, _, _, _, _, 5, 4, _, _, _, 4, _, _, _, _, 3, 2, 5, _, _, _, 3, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 2, 3, _, _, _, _, _, 5, 6, _, _, _, _, _, _, _, _, _, _, 3, _, _, 7, 8, _, 3, _, _, _, _, _, _, 2, 2, _, _, _, 1],
    [1, _, 3, 4, _, _, 5, 2, 1, 2, 2, _, _, _, _, _, _, 1, 2, _, _, _, _, 4, 6, _, _, _, 2, _, _, _, _, _, 9, _, _, _, _, _, 2, 4, _, 2, 2, _, _, 1],
    [1, _, 2, 10, 9, _, 6, 3, _, _, 3, 4, _, _, _, _, _, _, _, _, 3, 2, _, 3, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3, 3, _, 3, 10, 9, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 2, 4, _, _, _, _, _, _, _, _, 1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = {}
mini_map = set()
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4
            elif char == 5:
                world_map[(i * TILE, j * TILE)] = 5
            elif char == 6:
                world_map[(i * TILE, j * TILE)] = 6
            elif char == 7:
                world_map[(i * TILE, j * TILE)] = 7
            elif char == 8:
                world_map[(i * TILE, j * TILE)] = 8
            elif char == 9:
                world_map[(i * TILE, j * TILE)] = 9
            elif char == 10:
                world_map[(i * TILE, j * TILE)] = 10

def write_discr():
    f1 = pygame.font.Font(None, int(sc.get_size()[0]/53.33))
    back_menu = f1.render('Вернуться в меню', True,
                  (0, 25, 185))


    sc.blit(fill1, fill_rect)
    discr_pict = load_image("discr.JPG")
    discr_pict = pygame.transform.scale(discr_pict, (450, 450))
    pictx, picty = discr_pict.get_size()

    sc.blit(discr_pict, (center_x * 0.636363, center_y * 0.1666))

    pygame.draw.rect(sc, (0, 185, 25), 
                 (center_x * 0.89, center_y * 1.37, center_x * 0.25, center_y * 0.09))
    sc.blit(back_menu, (center_x * 0.9, center_y * 1.4))

def write_story():
    f1 = pygame.font.Font(None, int(sc.get_size()[0]/53.33))
    back_menu = f1.render('Вернуться в меню', True,
                  (0, 25, 185))
    center_x, center_y = sc.get_rect().center
    sc.blit(fill1, fill_rect)
    story_pict = load_image("story.JPG")
    story_pict = pygame.transform.scale(story_pict, (450, 450))
    pictx, picty = story_pict.get_size()
    sc.blit(story_pict, (center_x * 0.636363, center_y * 0.1666))

    pygame.draw.rect(sc, (0, 185, 25), 
                 (center_x * 0.89, center_y * 1.37, center_x * 0.25, center_y * 0.09))
    sc.blit(back_menu, (center_x * 0.9, center_y * 1.4))


def check_btn():
    global flag_btn
    global flag_dsrp
    global flag_story
    global flag_start_game
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if flag_btn:
        if rectlowx1 <= mouse_x <= rectlowx2 and rectlowy1 <= mouse_y <= rectlowy2:
            flag_start_game = True 
            pygame.mouse.set_visible(False)
            flag_btn = False
            
        elif rectmiddlex1 <= mouse_x <= rectmiddlex2 and rectmiddley1 <= mouse_y <= rectmiddley2:
            flag_story = True
            flag_btn = False

        elif recthighx1 <= mouse_x <= recthighx2 and recthighy1 <= mouse_y <= recthighy2:
            flag_btn = False
            flag_dsrp = True

    elif flag_dsrp or flag_story:
        if rectbackx1 <= mouse_x <= rectbackx2 and rectbacky1 <= mouse_y <= rectbacky2:
            flag_btn = True
            flag_dsrp = False
            flag_story = False


def draw_buttons():


    sc.blit(fill1, fill_rect)
    f1 = pygame.font.Font(None, int(sc.get_size()[0]/53.33))
    text1 = f1.render('Начать игру', True,
                  (0, 25, 185))
    text2 = f1.render('Открыть историю', True,
                  (0, 15, 185))
    text3 = f1.render('Открыть описание', True,
                  (0, 15, 185))

    pygame.draw.rect(sc, (0, 185, 25), 
                 (center_x * 0.9, center_y * 0.93, center_x * 0.28, center_y * 0.1))
    sc.blit(text1, (center_x * 0.966666, center_y * 0.95))
    

    pygame.draw.rect(sc, (0, 185, 25), 
                 (center_x * 0.9, center_y * 0.6, center_x * 0.28, center_y * 0.1))
    sc.blit(text2, (center_x * 0.9285, center_y * 0.6296))


    pygame.draw.rect(sc, (0, 185, 25), 
                 (center_x * 0.9, center_y * 0.77, center_x * 0.28, center_y * 0.1))
    sc.blit(text3, (center_x * 0.923, center_y * 0.8))
 
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image



def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(player, textures):
    walls = []
    ox, oy = player.pos
    texture_v, texture_h = 1, 1
    xm, ym = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player.angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min(int(PROJ_COEFF / depth), PENTA_HEIGHT)

        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
        wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))
        cur_angle += DELTA_ANGLE
    return walls









class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.sensitivity = 0.004
        # collision parameters
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)



    @property
    def pos(self):
        return (self.x, self.y)

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(collision_walls)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = collision_walls[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity


class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load('11z.png').convert(),
                         2: pygame.image.load('2z.png').convert(),
                         3: pygame.image.load('3z.png').convert(),
                         4: pygame.image.load('4z.png').convert(),
                         5: pygame.image.load('5z.png').convert(),
                         6: pygame.image.load('6z.png').convert(),
                         7: pygame.image.load('7z.png').convert(),
                         8: pygame.image.load('8z.png').convert(),
                         9: pygame.image.load('9z.png').convert(),
                         10: pygame.image.load('10z.png').convert(),
                         'S': pygame.image.load('ggr2.png').convert()
                         }


    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, DARKORANGE)
        self.sc.blit(render, FPS_POS)

    def mini_map(self, player):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                 map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, DARKBROWN, (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)



class Sprites:
    def __init__(self):
        self.sprite_types = {'devil': pygame.image.load('devil.png').convert_alpha()}
        self.list_of_objects = [SpriteObject(self.sprite_types['devil'], True, (16, 6), 0, 1.2)]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale


    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        distance_to_sprite = self.distance_to_sprite

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)



def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            return False
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                self.npc_move(obj)
                if self.npc_move(obj):
                    return True
                


    def npc_move(self, obj):
        dx = obj.x
        dy = obj.y
        if abs(obj.distance_to_sprite) > TILE:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 0.5 if dx < 0 else obj.x - 0.5
            obj.y = obj.y + 0.5 if dy < 0 else obj.y - 0.5

        if abs(obj.x - dx) <= 3 and abs(obj.y - dy) <= 3:
            return True




def play_music():
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('AlienShooter.mp3')
        pygame.mixer.music.play(100)


list_case_pos = [(1676, 548), (352, 2923), (2075, 1450), ( 4450, 2924), (3153, 2524), (3651, 1575)]
false_case = []

def check_pos():
    global case_far
    global false_case1
    case_far = False
    for el in list_case_pos:
        if abs(player.x - el[0]) <= 50 and abs(player.y - el[1]) <= 50:
            case_far = True
            false_case1 = el
            
            break
            
flag_pic = False

pygame.init()
if __name__ == '__main__':
    fill2 = load_image("dead_pic.png")
    fill2 = pygame.transform.scale(fill2, sc.get_size())
    fill_rect = fill2.get_rect()
    fill1 = load_image("заброшка.JPG")
    fill1 = pygame.transform.scale(fill1, sc.get_size())
    fill_rect = fill1.get_rect()

    fill3 = load_image("win_pic.png")
    fill3 = pygame.transform.scale(fill3, sc.get_size())

    pygame.init()
   
    
    sc_map = pygame.Surface(MINIMAP_RES)

    sprites = Sprites()
    clock = pygame.time.Clock()
    player = Player()
    drawing = Drawing(sc, sc_map)
    
    
    interaction = Interaction(player, sprites, drawing)

    sc.fill((0,0,0))
    play_music()
    pygame.display.flip()

    while running:
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if flag_start_game:
               
                if case_far and keys[pygame.K_e] and false_case1 not in false_case:

                    flag_pic = True
                    count += 1 
                    picture = list_of_pics[count]
                    picture_rect = picture.get_rect()
                    picture = pygame.transform.scale(picture, (400, 600))

                 
                    false_case.append(false_case1)
                    false_case1 = ""


                check_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                player.movement()
                sc.fill(BLACK)

                check_pos()

                drawing.background(player.angle)
                walls = ray_casting(player, drawing.textures)
                drawing.world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects])
               # drawing.fps(clock)
               # drawing.mini_map(player)
                if not flag_btn:
                    interaction.npc_action()

                if interaction.npc_action():
                    flag_start_game = False
                    flag_end_game = True
                    

                if flag_pic:
                    sc.blit(picture, picture_rect)

                if keys[pygame.K_SPACE]:
                    flag_pic = False


                if keys[pygame.K_k] and count >= 4 and not flag_dos:
                    flag_pult = True
                    flag_dos = True

                elif keys[pygame.K_k] and count >= 4 and flag_dos:
                    flag_dos = False
                    flag_pult = False

                if flag_pult:
                    sc.blit(pult, (400, 400))

                if keys[pygame.K_1] and flag_pult:
                    flag1 = True

                if keys[pygame.K_3] and flag1 and flag_pult:
                    flag2 = True

                if keys[pygame.K_4] and flag2 and flag_pult:
                    flag_gutend = True
                    flag_start_game = False

                if keys[pygame.K_n]:
                    flag_btn = True
                    flag_start_game = False
                    pygame.mouse.set_visible(True)
                    
            if (keys[pygame.K_ESCAPE] and flag_end_game) or (keys[pygame.K_ESCAPE] and flag_gutend):
                    running = False
            if flag_end_game:
                sc.blit(fill2, fill_rect)
                
            if flag_gutend:
                sc.blit(fill3, fill_rect)

            if flag_btn:
                draw_buttons()
            elif flag_dsrp:
                write_discr()
            elif flag_story:
                write_story()
            elif flag_start_game and count == 1:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_btn()
            

            pygame.display.flip()
            clock.tick()