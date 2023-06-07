import pygame
from pygame.locals import *
from pygame import mixer
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT 

pygame.init()

FPS = pygame.time.Clock()

# Get the client's screen resolution
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Calculate the percentage values
HEIGHT = int(screen_height * 1.00)  # % of the screen height
WIDTH = int(screen_width * 1.00)  # % of the screen width

# HEIGHT = 950
# WIDTH = 1800

scale_x = 200
scale_y = 200

scale_bomb_x = 250
scale_bomb_y = 90

FONT = pygame.font.SysFont('Verdana', 40)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_BLUE =(0,0,255)
COLOR_GREEN =(0,255,0)
COLOR_RED =(136, 8, 8)

main_display = pygame.display.set_mode((WIDTH,HEIGHT))

bg = pygame.transform.scale(pygame.image.load('resources/background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 2

IMAGE_PATH = "resources/Fokker"
IMAGE_PATH1 = "resources/Fokker_death"
IMAGE_PATH2 = "resources/Coin"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
PLAYER_IMAGES1 = os.listdir(IMAGE_PATH1)
PLAYER_IMAGES2 = os.listdir(IMAGE_PATH2)

# print(PLAYER_IMAGES)

mixer.init()
mixer.music.load('resources/music.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.6)



# player_size = (20,20)
player = pygame.transform.scale(pygame.image.load('resources/Fokker_default.png').convert_alpha(),(scale_x,scale_y)) #pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player_rect = player.get_rect(centery=HEIGHT/2, centerx= WIDTH/7)
# player_rect = player.get_rect()
# player_rect.center = main_display.get_rect().center
# player_speed = [1,1]
player_move_down = [0,16]
player_move_up = [0,-16]
player_move_left = [-16,0]
player_move_right = [16,0]


def create_enemy():
    # enemy_size = (30,30)
    enemy = pygame.transform.scale(pygame.image.load('resources/enemy.png').convert_alpha(),(scale_bomb_x,scale_bomb_y))  #pygame.Surface(enemy_size)
    # enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height(),HEIGHT-enemy.get_height()),*enemy.get_size())
    # print(enemy_rect)
    enemy_move = [random.randint(-8,-4),0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    # bonus_size = (30,30)
    bonus = pygame.image.load('resources/bonus.png').convert_alpha() #pygame.Surface(bonus_size)
    # bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(bonus.get_width(),WIDTH-bonus.get_width()), -100,*bonus.get_size())
    bonus_move = [0,random.randint(4,8)]
    return [bonus, bonus_rect, bonus_move]


CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE,170)
CHANGE_BONUS = pygame.USEREVENT + 4
pygame.time.set_timer(CHANGE_BONUS,80)


bonus_size_q = (0,0)
zvezda = pygame.Surface(bonus_size_q)
pered = (0, 0,0,0)

enemies = []
bonuses = []
pered2 = []

score = 0
score1 = 0

image_index = 0
image_index1 = 0
image_index2 = 0

enem = 0
bon = 0

playing = True

while playing:
    FPS.tick(50)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())  
        if event.type == CHANGE_BONUS:          
            if bon == 1:
                zvezda = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH2, PLAYER_IMAGES2[image_index2])),(80,80))
                image_index2 += 1
                if image_index2 >= len(PLAYER_IMAGES2):
                    image_index2 = 0     
                    bon = 0  
                    zvezda = pygame.Surface(bonus_size_q)      
        if event.type == CHANGE_IMAGE:
            if enem == 0 :
                player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])),(scale_x,scale_y)) 
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0           
            else:
                player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH1, PLAYER_IMAGES1[image_index1])),(scale_x,scale_y)) 
                image_index1 += 1
                if image_index1 >= len(PLAYER_IMAGES1):
                    enem = 0
                    image_index1 = 0
                    player = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])),(scale_x,scale_y))   
                    image_index += 1
                    if image_index >= len(PLAYER_IMAGES):
                        image_index = 0 
                                     
    # main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move
    
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
  
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
            
    main_display.blit(bg, (bg_X1,0))
    main_display.blit(bg, (bg_X2,0))
        
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    
    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)    
    
    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)    
    
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)  

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])
        
        if player_rect.colliderect(enemy[1]):
            score1 += 1
            enemies.pop(enemies.index(enemy))
            enem = 1
            explosion_sound = mixer.Sound('resources/explosion.wav')
            explosion_sound.play()
            explosion_sound.set_volume(0.3)         
  
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0],bonus[1])  
        
        if player_rect.colliderect(bonus[1]):
            score += 1
            bon = 1
            pered = bonus[1]         
            bonuses.pop(bonuses.index(bonus))
            bonus_sound = mixer.Sound('resources/bonus.wav')
            bonus_sound.play()
            bonus_sound.set_volume(0.4)
 
    main_display.blit(FONT.render(str(score),True, COLOR_BLACK),(WIDTH-75, 60))       
    main_display.blit(FONT.render(str(score1),True, COLOR_RED),(WIDTH-170, 60))        
    main_display.blit(player, player_rect)
    # main_display.blit(zvezda, pered)
    main_display.blit(zvezda, pygame.Rect(pered[0],pered[1]+150 ,pered[2],pered[3]))
    main_display.blit(pygame.transform.scale(pygame.image.load('resources/Coin.png'),(40,40)),(WIDTH-80, 20))
    main_display.blit(pygame.transform.scale(pygame.image.load('resources/enemy.png'),(100,40)),(WIDTH-200, 20)) 
    pygame.display.flip()
    
    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))            