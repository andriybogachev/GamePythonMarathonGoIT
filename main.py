import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0, 0, 255)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

# player_size = (20, 20)
# player = pygame.Surface(player_size)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

player_rect.bottom = HEIGHT/2
player_rect.right = WIDTH/5

def  create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT-100), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_benefit():
    benefit_size = (50, 50)
    benefit = pygame.image.load('bonus.png').convert_alpha()
    benefit_rect = pygame.Rect(random.randint(100, WIDTH-100), 0, *benefit_size)
    benefit_move = [0, random.randint(4, 8)]
    return [benefit, benefit_rect, benefit_move]


# Events
CREATE_ENEMY = pygame.USEREVENT +1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BENEFIT = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BENEFIT, 1500)

CHANGE_IMAGE = pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMAGE, 200)


enemies = []
benefits = []

score = 0

image_index = 0

playing = True
while playing:
    FPS.tick(240)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BENEFIT:
            benefits.append(create_benefit())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 <- bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 <- bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    # Керування квадратом
    if keys[K_DOWN]:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP]:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT]:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT]:
        player_rect = player_rect.move(player_move_left)

    # Поведінка при виході за межу екрану
    if player_rect.bottom >= HEIGHT:
        player_rect.bottom = 80

    if player_rect.top <= 0:
        player_rect.top = HEIGHT-80

    if player_rect.right >= WIDTH:
        player_rect.right = 200

    if player_rect.left <= 0:
        player_rect.left = WIDTH-200


    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            exit()

    for benefit in benefits:
        benefit[1] = benefit[1].move(benefit[2])
        main_display.blit(benefit[0], benefit[1])

        if player_rect.colliderect(benefit[1]):
            score += 1
            benefits.pop(benefits.index(benefit))

    
    main_display.blit(FONT.render(str("Score:"), True, COLOR_BLACK), (WIDTH-125, 20))
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    
    # print(len(enemies))
    # print(len(benefits))

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for benefit in benefits:
        if benefit[1].bottom > HEIGHT:
            benefits.pop(benefits.index(benefit))