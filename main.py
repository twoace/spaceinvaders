import pygame
import random
from pygame import mixer

pygame.init()

# Initialize Screen
wn = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("spacebackground.jpg")

# Title and Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 500
playerX_change = 0

# Score & Level
score_value = 0
level_value = 1

score_font = pygame.font.Font("Starjedi.ttf", 32)
level_font = pygame.font.Font("Starjedi.ttf", 32)

score_textX = 10
score_textY = 10
level_textX = 400
level_textY = 10


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    wn.blit(score, (x, y))


def show_level(x, y):
    level = level_font.render("Level: " + str(level_value), True, (255, 255, 255))
    wn.blit(level, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 0


def createEnemies(num):
    for i in range(num):
        enemyImg.append(pygame.image.load("alien.png"))
        global added
        added = False
        while not added:
            x = random.randint(5, 730)
            isNear = False
            if len(enemyX) <= 0:
                enemyX.append(x)
                added = True
                break
            for number in enemyX:
                if x >= number - 35 and x <= number + 35:
                    isNear = True
                    break
            if not isNear:
                enemyX.append(x)
                added = True
        enemyY.append(50)
        enemyX_change.append(0.1)
        enemyY_change.append(65)
    global num_of_enemies
    num_of_enemies = len(enemyImg)


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletImg = pygame.transform.rotate(bulletImg, 90)
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 0.6
bullet_state = "ready"


# Player/Enemy/Bullet drawfunction
def player(x, y):
    wn.blit(playerImg, (x, y))


def enemy(x, y, i):
    wn.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    wn.blit(bulletImg, (x + 16, y + 10))


# Collision detection
def isCollision(aImg, aX, aY, bImg, bX, bY):
    if aImg.get_rect(x=aX, y=aY).colliderect(bImg.get_rect(x=bX, y=bY)):
        return True


# Initialise
createEnemies(6)

# Game Loop
running = True
while running:
    for event in pygame.event.get():

        # Quit event check
        if event.type == pygame.QUIT:
            running = False

        # Keybinding
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.1
            if event.key == pygame.K_d:
                playerX_change = 0.1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("fire.mp3")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # Draw background
    wn.fill((0, 0, 0))
    wn.blit(background, (0, 0))

    # Moving player and checking for boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 734:
        playerX = 734

    # Moving enemy and checking for boundaries
    if num_of_enemies <= 0:
        createEnemies(6)
        level_value += 1
        enemyX_change = [x+level_value/10 for x in enemyX_change]
    for i in range(num_of_enemies):
        # Draw enemy
        enemy(enemyX[i], enemyY[i], i)
        # Move enemy
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 734:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        if enemyY[i] >= 450:
            running = False
        if isCollision(bulletImg, bulletX, bulletY, enemyImg[i], enemyX[i], enemyY[i]):
            explosion_sound = mixer.Sound("explosion.mp3")
            explosion_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score_value += 1
            enemyImg.pop(i)
            enemyX.pop(i)
            enemyY.pop(i)
            enemyX_change.pop(i)
            enemyY_change.pop(i)
            num_of_enemies -= 1
            break
    # Moving bullet
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Draw Player
    player(playerX, playerY)

    # Draw Score & Level
    show_score(score_textX, score_textY)
    show_level(level_textX, level_textY)

    pygame.display.update()
