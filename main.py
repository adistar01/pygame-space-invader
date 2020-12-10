import pygame
import random
import math
from pygame import mixer

# Initializing pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

background=pygame.image.load("2819.jpg")

#Background sound
mixer.music.load('media.io_b16b2c3fd7b649ac831d74e1936217ef.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('001-spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0.0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('001-space-invaders.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

#Bullet
#Ready - You can't see the bullet on the screen
#Fire - The bullet is currently working
bulletImg = pygame.image.load('001-bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change=1.0
bullet_state='ready'

def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow((enemyX-bulletX),2))+(math.pow((enemyY-bulletY),2)))
    if distance<27:
        return True
    else:
        return False
#Score
score=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

# Game Over Text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score_val=font.render("Score : "+str(score),True,(255,255,255))
    screen.blit(score_val,(x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER !",True,(245,189,230))
    screen.blit(over_text,(200,250))

# Game Screen Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check if its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3

            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0

    # RGB value fill screen
    screen.fill((15, 235, 70))

    #Background Image
    screen.blit(background,(0,0))

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    if playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over
        if (enemyY[i] > 440):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]=-0.3
            enemyY[i]+=enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score = score + 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i],i)

    #Bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state=="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
