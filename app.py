import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game Enhanced")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game variables
clock = pygame.time.Clock()
player_car = pygame.Rect(175, 500, 50, 80)
enemy_cars = []
power_ups = []
obstacles = []
score = 0
lives = 3
game_over = False
paused = False
shield_active = False
speed_boost_active = False
shield_timer = 0
speed_boost_timer = 0
player_speed = 5

# Load assets
player_car_img = pygame.image.load("player_car.png")
enemy_car_img = pygame.image.load("enemy_car.png")
background_img = pygame.image.load("background.png")
crash_sound = pygame.mixer.Sound("crash.mp3")
score_sound = pygame.mixer.Sound("score.mp3")
power_up_sound = pygame.mixer.Sound("power_up.mp3")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

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
    if shield_active:
        pygame.draw.ellipse(screen, BLUE, player_car.inflate(20, 20), 5)
    screen.blit(player_car_img, (player_car.x, player_car.y))

def draw_enemies():
    for car in enemy_cars:
        screen.blit(enemy_car_img, (car.x, car.y))

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, YELLOW, obstacle)

def draw_power_ups():
    for power_up in power_ups:
        pygame.draw.circle(screen, GREEN if power_up.type == 'shield' else BLUE, (power_up.x + 25, power_up.y + 25), 25)

def draw_health_bar():
    bar_width = 150
    bar_height = 20
    filled_width = int(bar_width * (lives / 3))
    pygame.draw.rect(screen, RED, (10, 40, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (10, 40, filled_width, bar_height))

def generate_enemy():
    if random.random() < 0.02:
        x = random.choice([50, 150, 250, 350]) - 25
        enemy_cars.append(pygame.Rect(x, -80, 50, 80))

def generate_obstacle():
    if random.random() < 0.01:
        x = random.choice([50, 150, 250, 350]) - 25
        obstacles.append(pygame.Rect(x, -60, 50, 80))

def generate_power_up():
    if random.random() < 0.005:
        x = random.choice([50, 150, 250, 350]) - 25
        power_up_type = 'shield' if random.random() < 0.5 else 'speed'
        power_ups.append(pygame.Rect(x, -50, 50, 50, type=power_up_type))

def move_enemies():
    global score, lives, shield_active, shield_timer
    for car in enemy_cars[:]:
        car.y += 5 + score // 10
        if car.y > SCREEN_HEIGHT:
            enemy_cars.remove(car)
            score += 1
            score_sound.play()

        if player_car.colliderect(car):
            if shield_active:
                enemy_cars.remove(car)
            else:
                crash_sound.play()
                lives -= 1
                enemy_cars.remove(car)
                if lives <= 0:
                    end_game()

def move_obstacles():
    for obstacle in obstacles[:]:
        obstacle.y += 2
        if obstacle.y > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
        if player_car.colliderect(obstacle):
            crash_sound.play()
            lives -= 1
            obstacles.remove(obstacle)
            if lives <= 0:
                end_game()

def move_power_ups():
    global shield_active, shield_timer, speed_boost_active, speed_boost_timer, player_speed
    for power_up in power_ups[:]:
        power_up.y += 3
        if power_up.y > SCREEN_HEIGHT:
            power_ups.remove(power_up)
        if player_car.colliderect(power_up):
            power_up_sound.play()
            if power_up.type == 'shield':
                shield_active = True
                shield_timer = pygame.time.get_ticks()
            elif power_up.type == 'speed':
                speed_boost_active = True
                speed_boost_timer = pygame.time.get_ticks()
                player_speed = 8
            power_ups.remove(power_up)

def check_timers():
    global shield_active, speed_boost_active, player_speed
    if shield_active and pygame.time.get_ticks() - shield_timer > 5000:
        shield_active = False
    if speed_boost_active and pygame.time.get_ticks() - speed_boost_timer > 3000:
        speed_boost_active = False
        player_speed = 5

def end_game():
    global game_over
    game_over = True

def restart_game():
    global score, lives, enemy_cars, power_ups, obstacles, game_over, paused, shield_active, speed_boost_active, player_speed
    score = 0
    lives = 3
    enemy_cars = []
    power_ups = []
    obstacles = []
    game_over = False
    paused = False
    shield_active = False
    speed_boost_active = False
    player_speed = 5

def toggle_pause():
    global paused
    paused = not paused

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_car.x > 0:
        player_car.x -= player_speed
    if keys[pygame.K_RIGHT] and player_car.x < SCREEN_WIDTH - player_car.width:
        player_car.x += player_speed
    if keys[pygame.K_p]:
        toggle_pause()
    if keys[pygame.K_m]:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1)
    if keys[pygame.K_r] and game_over:
        restart_game()

    if game_over:
        draw_text(f"Game Over! Score: {score}", 55, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30)
        draw_text("Press R to Restart", 30, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20)
    elif not paused:
        draw_background()
        draw_player()
        draw_enemies()
        draw_obstacles()
        draw_power_ups()
        generate_enemy()
        generate_obstacle()
        generate_power_up()
        move_enemies()
        move_obstacles()
        move_power_ups()
        check_timers()

        # Display score, lives, and health bar
        draw_text(f"Score: {score}", 25, BLACK, 10, 10)
        draw_health_bar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
