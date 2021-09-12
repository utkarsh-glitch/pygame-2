import pygame
import random
import math
from pygame import mixer

# initialize
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 540))
# background
background = pygame.image.load("bg.png")
# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# display title
pygame.display.set_caption("Space Petrol Delta")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# player
playerIMG = pygame.image.load("spaceship (1).png")
playerX = 370
playerY = 480
playerX_change = 0
# enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)
# Bullet
bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"
# font
score_value = 0
font = pygame.font.SysFont("freesansbold.ttr", 45)
textX = 10
textY = 10


# game over font
# game_font = pygame.font.SysFont("freesansbold.ttr", 64)
def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# def game_over_text():
#   over_text = game_font.render("GAME OVER", True, (255, 255, 255))
#  screen.blit(over_text, (200, 300))
def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # background color
    screen.fill((255, 255, 255))
    # background
    screen.blit(background, (0, 0))
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        # if  key strokes are pressed
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_LEFT:
                playerX_change = -0.5
            if events.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if events.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # bullet sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if events.type == pygame.KEYUP:
            if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                playerX_change = 0
    # boundaries for characters
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # enemy movement
    for i in range(num_of_enemies):
        ''' game over
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over_text()
                break'''
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_sound = mixer.Sound("explosion.wav")
            bullet_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
