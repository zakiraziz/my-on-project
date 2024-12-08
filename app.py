import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Load assets
player_car = pygame.image.load("player_car.png")
player_car = pygame.transform.scale(player_car, (50, 100))

enemy_car = pygame.image.load("enemy_car.png")
enemy_car = pygame.transform.scale(enemy_car, (50, 100))

road_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
road_image.fill(GRAY)

# Font for score and lives
font = pygame.font.Font(None, 36)

# Game variables
player_x = SCREEN_WIDTH // 2 - 25
player_y = SCREEN_HEIGHT - 120
player_speed = 6

enemy_cars = [{"x": random.randint(50, SCREEN_WIDTH - 100), "y": random.randint(-300, -100), "speed": random.randint(3, 6)} for _ in range(3)]
score = 0
lives = 3

road_y = 0

# Functions
def draw_text(text, x, y, color=WHITE):
    """Render and display text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def move_road():
    """Animate the scrolling road."""
    global road_y
    road_y += 4
    if road_y >= SCREEN_HEIGHT:
        road_y = 0
    screen.blit(road_image, (0, road_y - SCREEN_HEIGHT))
    screen.blit(road_image, (0, road_y))

def game_over():
    """Display a game-over screen."""
    screen.fill(BLACK)
    draw_text("GAME OVER!", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 40, RED)
    draw_text(f"Score: {score}", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, WHITE)
    draw_text("Press R to Restart", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, YELLOW)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
                return

def restart_game():
    """Restart the game."""
    global player_x, player_y, enemy_cars, score, lives
    player_x = SCREEN_WIDTH // 2 - 25
    player_y = SCREEN_HEIGHT - 120
    enemy_cars[:] = [{"x": random.randint(50, SCREEN_WIDTH - 100), "y": random.randint(-300, -100), "speed": random.randint(3, 6)} for _ in range(3)]
    score = 0
    lives = 3

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 100:
        player_x += player_speed

    # Move road
    move_road()

    # Move enemy cars
    for enemy in enemy_cars:
        enemy["y"] += enemy["speed"]
        if enemy["y"] > SCREEN_HEIGHT:
            enemy["y"] = random.randint(-300, -100)
            enemy["x"] = random.randint(50, SCREEN_WIDTH - 100)
            enemy["speed"] = random.randint(3, 6)
            score += 1

    # Check for collisions
    player_rect = pygame.Rect(player_x, player_y, 50, 100)
    for enemy in enemy_cars:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 100)
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            enemy["y"] = random.randint(-300, -100)
            enemy["x"] = random.randint(50, SCREEN_WIDTH - 100)
            if lives == 0:
                game_over()

    # Draw player car
    screen.blit(player_car, (player_x, player_y))

    # Draw enemy cars
    for enemy in enemy_cars:
        screen.blit(enemy_car, (enemy["x"], enemy["y"]))

    # Display score and lives
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", SCREEN_WIDTH - 100, 10, GREEN)

    # Update display and control FPS
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
