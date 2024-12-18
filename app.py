import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variables
clock = pygame.time.Clock()
player_car = pygame.Rect(175, 500, 50, 80)
enemy_cars = []
score = 0
lives = 3
game_over = False
paused = False

# Load assets
player_car_img = pygame.image.load("player_car.png")
enemy_car_img = pygame.image.load("enemy_car.png")
background_img = pygame.image.load("background.png")
crash_sound = pygame.mixer.Sound("crash.mp3")
score_sound = pygame.mixer.Sound("score.mp3")

# Background scrolling
background_y = 0

def draw_background():
    global background_y
    screen.blit(background_img, (0, background_y))
    screen.blit(background_img, (0, background_y - SCREEN_HEIGHT))
    background_y += 2
    if background_y >= SCREEN_HEIGHT:
        background_y = 0

def draw_player():
    screen.blit(player_car_img, (player_car.x, player_car.y))

def draw_enemies():
    for car in enemy_cars:
        screen.blit(enemy_car_img, (car.x, car.y))

def generate_enemy():
    if random.random() < 0.02:
        x = random.randint(0, SCREEN_WIDTH - 50)
        enemy_cars.append(pygame.Rect(x, -80, 50, 80))

def move_enemies():
    global score, lives
    for car in enemy_cars[:]:
        car.y += 5 + score // 10
        if car.y > SCREEN_HEIGHT:
            enemy_cars.remove(car)
            score += 1
            score_sound.play()

        if player_car.colliderect(car):
            crash_sound.play()
            lives -= 1
            enemy_cars.remove(car)
            if lives <= 0:
                end_game()

def end_game():
    global game_over
    game_over = True

def restart_game():
    global score, lives, enemy_cars, game_over, paused
    score = 0
    lives = 3
    enemy_cars = []
    game_over = False
    paused = False

def toggle_pause():
    global paused
    paused = not paused

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_car.x > 0:
        player_car.x -= 5
    if keys[pygame.K_RIGHT] and player_car.x < SCREEN_WIDTH - player_car.width:
        player_car.x += 5

    if game_over:
        font = pygame.font.SysFont(None, 55)
        text = font.render(f"Game Over! Score: {score}", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    elif not paused:
        draw_background()
        draw_player()
        draw_enemies()
        generate_enemy()
        move_enemies()

        # Display score and lives
        font = pygame.font.SysFont(None, 25)
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

