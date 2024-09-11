import pygame
import random
import math

# Inicializa pygame
pygame.init()

# Crea la ventana (Ancho, Alto)
screen = pygame.display.set_mode((800, 600))

# Fondo
background = pygame.image.load('images/background.jpg')

# Title and Icon
pygame.display.set_caption("Cazadores")
icon = pygame.image.load('images/hunter.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/player.png')
playerX = 0
playerY = 260
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(650, 700))
    enemyY.append(random.randint(50, 480))
    enemyX_change.append(60)
    enemyY_change.append(0.2)

# Bala
# Ready - No se ve la bala en la pantalla
# Fire - La bala se esta moviendo

bulletImg = pygame.image.load('images/bullet.png')
bulletX = 100
bulletY = 0
bulletX_change = 0.5
bulletY_change = 0
bullet_state = "ready"

# Puntuación
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Texto de inicio del juego
menu_font = pygame.font.Font('freesansbold.ttf', 64)
button_font = pygame.font.Font('freesansbold.ttf', 32)

# Texto de fin del juego
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y+15))

def isColission(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 30

def draw_button(x, y, w, h, text):
    pygame.draw.rect(screen, (54, 158, 75), (x, y, w, h))
    text_surface = button_font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surface, text_rect)

def show_menu():
    screen.blit(background, (0,0))
    menu_text = menu_font.render("CAZADORES", True, (255, 255, 255))
    screen.blit(menu_text, (200, 200))
    draw_button(260, 300, 300, 50, "Iniciar")
    draw_button(260, 400, 300, 50, "Salir")
    screen.blit(menu_text, (200, 200))
    pygame.display.update()

def start_button():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 260 <= mouse_pos[0] <= 560 and 300 <= mouse_pos[1] <= 350:
                    waiting = False
                if 260 <= mouse_pos[0] <= 560 and 400 <= mouse_pos[1] <= 450:
                    pygame.quit()
                    quit()

# Mostrar el menú antes de empezar el juego
show_menu()
start_button()

# Game loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0,0,0))
    # Fondo
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movimiento del jugador en Y
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -0.23
            if event.key == pygame.K_DOWN:
                playerY_change = 0.23
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    
    # Barrera para el jugador en Y
    playerY += playerY_change

    if playerY <= 0:
        playerY = 0
    elif playerY >= 480:
        playerY = 480

    # Barrera y movimiento para el enemigo
    for i in range(num_of_enemies):

        #Game over
        if enemyX[i] < 120:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyY[i] += enemyY_change[i]

        if enemyY[i] <= 0:
            enemyY_change[i] = 0.2
            enemyX[i] -= enemyX_change[i]
        elif enemyY[i] >= 536:
            enemyY_change[i] = -0.2
            enemyX[i] -= enemyX_change[i]

        # Colisión
        collision = isColission(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletX = 80
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(600, 750)
            enemyY[i] = random.randint(0, 536)

        enemy(enemyX[i], enemyY[i], i)

    # Moviemiento de la bala
    if bulletX >= 800:
        bulletX = 120
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletX += bulletX_change

    player(playerX, playerY)
    show_score(textX, textY)    
    pygame.display.update()