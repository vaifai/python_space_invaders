import pygame
import random
import math
# inintialize pygame library
pygame.init()
# creating screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')
running = True

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('gaming.png')
playerX, playerY, playerX_change = 370, 480, 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(20)


# bullet
# Ready->ready to be fired
# fire->bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY, bulletX_change, bulletY_change = 0, 480, 0, 10
bullet_state = "ready"
score = 0

font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    ss = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(ss, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+17))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX-bulletX)**2 + (enemyY-bulletY)**2)
    if(distance < 27):
        return True
    else:
        return False


# GameLoop
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT):
                playerX_change -= 3
                #print('Left key pressed')
            elif(event.key == pygame.K_RIGHT):
                playerX_change += 3
                #print('Right key pressed')

            elif(event.key == pygame.K_SPACE):
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        elif(event.type == pygame.KEYUP):
            if(event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                playerX_change = 0

    # boundary Checking
    playerX += playerX_change
    #enemyX += enemyX_change
    playerX = max(playerX, 0)
    playerX = min(playerX, 736)

    for i in range(num_of_enemies):
        # Game OVer
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if(enemyX[i] <= 0):
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif(enemyX[i] >= 736):
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 100)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if(bulletY <= 0):
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # to make sure display is always updating
