import pygame
import random
import os

pygame.init()

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
FPS = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

mainDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

backGround = pygame.transform.scale(pygame.image.load('img/background.png'), (WIDTH,HEIGHT))
bgX1 = 0
bgX2 = backGround.get_width()
backGroundMove = 3

imgPath = 'img/Goose'
PLAYER_IMAGES = os.listdir(imgPath) 

playerSize = (20, 20)
playerMoveDown = [0, 4]
playerMoveUp = [0, -4]
playerMoveRight = [4, 0]
playerMoveLeft = [-4, 0]

player = pygame.image.load('img/player.png').convert_alpha() 
playerRect = player.get_rect()
isPlaying = True

playerRect.centerx = WIDTH/2
playerRect.centery = HEIGHT/2



def SpawnEnemy():
    enemySize = (30, 30)
    enemy = pygame.image.load('img/enemy.png').convert_alpha()
    enemyRect = pygame.Rect(WIDTH, random.randint(100, HEIGHT-100), *enemySize)
    enemyMove = [random.randint(-8, -4), 0]
    return [enemy, enemyRect, enemyMove]

def SpawnBonus():
    bonusSize = (50,50)
    bonus = pygame.image.load('img/bonus.png').convert_alpha()
    bonusRect = pygame.Rect(random.randint(100, WIDTH-100),0 , *bonusSize)
    bonusMove = [0, random.randint(4,8)]
    return [bonus, bonusRect, bonusMove]


ENEMY_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SPAWN, 1500)

BONUS_SPAWN = pygame.USEREVENT +2
pygame.time.set_timer(BONUS_SPAWN, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0 

imgIndex = 0 

while isPlaying:
    FPS.tick(700)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == ENEMY_SPAWN:
            enemies.append(SpawnEnemy())
        if event.type == BONUS_SPAWN:
            bonuses.append(SpawnBonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(imgPath, PLAYER_IMAGES[imgIndex]))
            imgIndex += 1
            if imgIndex >= len(PLAYER_IMAGES):
                imgIndex = 0


    bgX1 -= backGroundMove
    bgX2 -= backGroundMove 
    
    if  bgX1 < -backGround.get_width():
        bgX1 = backGround.get_width()
        
    if  bgX2 < -backGround.get_width():
        bgX2 = backGround.get_width()

    mainDisplay.blit(backGround, (bgX1, 0))
    mainDisplay.blit(backGround, (bgX2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and playerRect.bottom < HEIGHT:
        playerRect = playerRect.move(playerMoveDown)

    if keys[K_UP] and playerRect.top > 0:
        playerRect = playerRect.move(playerMoveUp)

    if keys[K_RIGHT] and playerRect.right < WIDTH:
        playerRect = playerRect.move(playerMoveRight)

    if keys[K_LEFT] and playerRect.left > 0:
        playerRect = playerRect.move(playerMoveLeft)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        mainDisplay.blit(enemy[0], enemy[1])
        
        if playerRect.colliderect(enemy[1]):
            isPlaying = False
        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        mainDisplay.blit(bonus[0], bonus[1])
        
        if playerRect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    mainDisplay.blit(FONT.render(str(score),True,COLOR_BLACK), (WIDTH - 50, 20))

    mainDisplay.blit(player,playerRect)

    pygame.display. flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
