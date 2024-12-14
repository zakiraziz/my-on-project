import pygame
import random
import sys
import os

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
BLUE = (0, 0, 255)

# Function to load images with error handling
def load_image(name, scale=None):
    try:
        image = pygame.image.load(name)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error:
        print(f"Error: Unable to load image {name}")
        sys.exit()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Load assets
player_car = load_image("player_car.png", (50, 100))
enemy_car = load_image("enemy_car.png", (50, 100))
power_up_image = load_image("power_up.png", (30, 30))

road_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
road_image.fill(GRAY)

# Sound effects
def load_sound(name):
    try:
        return pygame.mixer.Sound(name)
    except pygame.error:
        print(f"Error: Unable to load sound {name}")
        sys.exit()

crash_sound = load_sound("crash.wav")
power_up_sound = load_sound("power_up.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Font for score and lives
font = pygame.font.Font(None, 36)

# Game variables
player_x = SCREEN_WIDTH // 2 - 25
player_y = SCREEN_HEIGHT - 120
player_speed = 6
player_shield = False

enemy_cars = [{"x": random.randint(50, SCREEN_WIDTH - 100), "y": random.randint(-300, -100), "speed": random.randint(3, 6)} for _ in range(3)]
power_ups = [{"x": random.randint(50, SCREEN_WIDTH - 100), "y": random.randint(-600, -100), "speed": 4}]
score = 0
lives = 3
road_y = 0
paused = False

# Functions
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def move_road():
    global road_y
    road_y += 4
    if road_y >= SCREEN_HEIGHT:
        road_y = 0
    screen.blit(road_image, (0, road_y - SCREEN_HEIGHT))
    screen.blit(road_image, (0, road_y))

def game_over():
    pygame.mixer.music.stop()
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
    global player_x, player_y, enemy_cars, power_ups, score, lives, player_shield
    player_x = SCREEN_WIDTH // 2 - 25
    player_y = SCREEN_HEIGHT - 120
    enemy_cars[:] = [{"x": random.randint(50, SCREEN_WIDTH - 100), "y": random.randint(-300, -100), "speed": random.randint(3, 6)} for _ in range(3)]
    power_ups[:] = [{"x": random.randint(50, SCREEN_WIDTH - 100), "y": random.randint(-600, -100), "speed": 4}]
    score = 0
    lives = 3
    player_shield = False
    pygame.mixer.music.play(-1)

def toggle_pause():
    global paused
    paused = not paused

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                toggle_pause()

    if paused:
        draw_text("PAUSED", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, YELLOW)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 100:
        player_x += player_speed

    move_road()

    for enemy in enemy_cars:
        enemy["y"] += enemy["speed"]
        if enemy["y"] > SCREEN_HEIGHT:
            enemy["y"] = random.randint(-300, -100)
            enemy["x"] = random.randint(50, SCREEN_WIDTH - 100)
            enemy["speed"] = random.randint(3, 6)
            score += 1

    for power_up in power_ups:
        power_up["y"] += power_up["speed"]
        if power_up["y"] > SCREEN_HEIGHT:
            power_up["y"] = random.randint(-600, -100)
            power_up["x"] = random.randint(50, SCREEN_WIDTH - 100)

    player_rect = pygame.Rect(player_x, player_y, 50, 100)
    for enemy in enemy_cars:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 100)
        if player_rect.colliderect(enemy_rect):
            if player_shield:
                player_shield = False
            else:
                lives -= 1
                crash_sound.play()
            enemy["y"] = random.randint(-300, -100)
            if lives == 0:
                game_over()

    for power_up in power_ups:
        power_up_rect = pygame.Rect(power_up["x"], power_up["y"], 30, 30)
        if player_rect.colliderect(power_up_rect):
            player_shield = True
            power_up_sound.play()
            power_up["y"] = random.randint(-600, -100)

    screen.blit(player_car, (player_x, player_y))

    for enemy in enemy_cars:
        screen.blit(enemy_car, (enemy["x"], enemy["y"]))

    for power_up in power_ups:
        screen.blit(power_up_image, (power_up["x"], power_up["y"]))

    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", SCREEN_WIDTH - 100, 10, GREEN)
    draw_text(f"Shield: {'Active' if player_shield else 'Inactive'}", 10, 50, BLUE)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-game')
def start_game():
    subprocess.Popen(["python", "pygame_game.py"])
    return "Game started! Check your desktop."

if __name__ == "__main__":
    app.run(debug=True)


def save_score(player_name, score):
    with open("scores.txt", "a") as file:
        file.write(f"{player_name},{score}\n")
@app.route('/leaderboard')
def leaderboard():
    with open("scores.txt", "r") as file:
        scores = [line.strip().split(",") for line in file.readlines()]
    return {"scores": scores}
