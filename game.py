import pygame
import random
import math
import sys
import os

# Inicializar pygame
pygame.init()

# Establecer el tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Función para obtener la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar imagen de fondo
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

# Cargar icono de ventana
asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)

# Cargar sonido de fondo
asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)

# Cargar imagen del jugador
asset_playerimg = resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(asset_playerimg)

# Cargar imagen de bala
asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

# Cargar fuente para texto de game over
asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)

# Cargar fuente para texto de puntuación
asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

# Establecer título de ventana
pygame.display.set_caption("Amenaza Alienígena")

# Establecer ícono de ventana
pygame.display.set_icon(icon)

# Reproducir sonido de fondo en loop
pygame.mixer.music.play(-1)

# Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Posición inicial del jugador
playerX = 370
playerY = 470
playerx_change = 0

# Lista para almacenar posiciones de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

# Inicializar las variables para guardar las posiciones de los enemigos
for i in range(no_of_enemies):
    # Se carga la imagen del enemigo
    enemy = resource_path(f'assets/images/enemy{i % 2 + 1}.png')
    enemyimg.append(pygame.image.load(enemy))

    # Se asigna una posición aleatoria en X e Y para el enemigo
    enemyX.append(random.randint(0, screen_width - 64))
    enemyY.append(random.randint(0, 150))

    # Se establece la velocidad de movimiento del enemigo X e Y
    enemyX_change.append(5)
    enemyY_change.append(40)

# Inicializar las variables para guardar la posición de la bala
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Inicializar la puntuación en 0
score = 0

# Función para mostrar la puntuación en la pantalla
def show_score():
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

# Función para dibujar al jugador en la pantalla
def player(x, y):
    screen.blit(playerimg, (x, y))

# Función para dibujar al enemigo
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# Función para disparar la bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

# Función para comprobar si la bala colisionó con el enemigo
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Función para mostrar el texto de Game Over en pantalla
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (screen_width/2 - over_text.get_width()/2, screen_height/2 - over_text.get_height()/2))

    # Botón de nuevo juego
    new_game_text = font.render("New Game", True, (255, 255, 255))
    new_game_rect = new_game_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
    screen.blit(new_game_text, new_game_rect)

    return new_game_rect

# Función para reiniciar el juego
def reset_game():
    global score
    global playerX
    global playerx_change
    global enemyX
    global enemyY
    global bullet_state

    score = 0
    playerX = 370
    playerx_change = 0
    bullet_state = "ready"
    for i in range(no_of_enemies):
        enemyX[i] = random.randint(0, screen_width - 64)
        enemyY[i] = random.randint(0, 150)

# Bucle principal del juego
running = True
game_over = False
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            elif event.key == pygame.K_RIGHT:
                playerx_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Manejo del clic del mouse para un nuevo juego
            if game_over and new_game_rect.collidepoint(event.pos):
                reset_game()
                game_over = False

    # Mover al jugador
    playerX += playerx_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - 64:
        playerX = screen_width - 64

    # Mover a los enemigos y comprobar colisiones
    for i in range(no_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screen_width - 64:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Colisiones
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, screen_width - 64)
            enemyY[i] = random.randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

        # Game Over
        if enemyY[i] > 440:
            game_over = True
            break

    # Mover la bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Dibujar al jugador y mostrar la puntuación
    player(playerX, playerY)
    show_score()

    # Mostrar pantalla de Game Over si es necesario
    if game_over:
        new_game_rect = game_over_text()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()



