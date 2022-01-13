import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = (1365, 705)

HEALTH_FONT = pygame.font.SysFont('algerian', 45)
WIN_FONT = pygame.font.SysFont('algerian', 100)

BLUE = 0, 190, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
YELLOW = 255, 0, 255

BULLET_VELOCITY = 20
MAX_BULLETS = 3
VELOCITY = 10

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

FPS = 60
SHIP_WIDTH = 100
SHIP_HEIGHT = 100

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My 2 player Game ;)')

IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','img.png')), (800, 200))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

YELLOW_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)

RED_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

def win_display(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(IMAGE, (310, 0))
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, RED)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    pygame.draw.rect(WIN, BLACK, BORDER)
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))    
    pygame.display.update()

def ship_movements(red, yellow, key_pressed):
    # Yellow ship movements
    if key_pressed[pygame.K_a] and yellow.x > 0:    # Left move for yellow ship
        yellow.x -= VELOCITY
    if key_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x - BORDER.width:   # Right move for yellow ship
        yellow.x += VELOCITY
    if key_pressed[pygame.K_w] and yellow.y - 10> 0:    # Upward move for yellow ship
        yellow.y -= VELOCITY
    if key_pressed[pygame.K_s] and yellow.y + yellow.height + 20 < HEIGHT:   # Downward move for yellow ship
        yellow.y += VELOCITY

    # Red ship movements
    if key_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width + 10:    # Left move for red ship
        red.x -= VELOCITY
    if key_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH:   # Right move for red ship
        red.x += VELOCITY
    if key_pressed[pygame.K_UP] and red.y - 10 > 0:     # Upward move for red ship
        red.y -= VELOCITY
    if key_pressed[pygame.K_DOWN] and red.y + red.height + 20 < HEIGHT:     # Downward move for red ship
        red.y += VELOCITY

def bullet_movements(red, yellow, red_bullets, yellow_bullets):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_winner = WIN_FONT.render(text, 1, RED)
    WIN.blit(draw_winner, (WIDTH/2 - draw_winner.get_width(), HEIGHT/2 - draw_winner.get_height()))
    pygame.display.update()
    pygame.time.delay(500)

def main():
    yellow = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)
    red = pygame.Rect(1150, 300, SHIP_WIDTH, SHIP_HEIGHT)

    clock = pygame.time.Clock()

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    bullet_sound = pygame.mixer.Sound(os.path.join('Assets', 'fire2.wav'))
    collision_sound = pygame.mixer.Sound(os.path.join('Assets', 'collision2.wav'))

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2, 50, 30)
                    yellow_bullets.append(bullet)
                    bullet_sound.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height/2, 50, 30)
                    red_bullets.append(bullet)
                    bullet_sound.play()

            if event.type == RED_HIT:
                red_health -= 1
                collision_sound.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                collision_sound.play()
                
        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        ship_movements(red, yellow, key_pressed)
        bullet_movements(red, yellow, red_bullets, yellow_bullets)

        win_display(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

main()