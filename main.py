import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Dino settings
dino_width, dino_height = 50, 50
dino_x, dino_y = 50, HEIGHT - dino_height - 10
dino_vel = 10
jumping = False
jump_count = 10

# Dino Animation
dino_images = [pygame.Surface((dino_width, dino_height)) for _ in range(2)]
dino_images[0].fill(BLACK)  # Dino color
dino_images[1].fill(GRAY)   # Dino color when walking
dino_frame = 0
dino_animation_speed = 10

# Obstacle settings
obs_width, obs_height = 50, 50
num_obstacles = 3
obstacles = []
for i in range(num_obstacles):
    obs_type = random.choice(['type1', 'type2'])
    x_pos = WIDTH + i * 300
    obstacles.append({'x': x_pos, 'y': HEIGHT - obs_height - 10, 'type': obs_type, 'behavior': random.choice(['normal', 'fast'])})

obs_vel = 15
obs_speed_increase = 2
level_up_score = 10

# Power-up settings
power_up_width, power_up_height = 30, 30
power_ups = []
power_up_interval = 5000  # Power-up spawn interval in milliseconds
power_up_timer = pygame.time.get_ticks()
power_up_active = False
power_up_duration = 5000  # Power-up duration in milliseconds
power_up_start_time = 0

# Background settings
bg1_x, bg2_x = 0, WIDTH
bg_speed = 5

# Score and Level
score = 0
level = 1
font = pygame.font.Font(None, 36)

def draw_dino(x, y, frame):
    screen.blit(dino_images[frame], (x, y))

def draw_obstacles(obs_list):
    for obs in obs_list:
        color = GRAY if obs['type'] == 'type1' else BLUE
        pygame.draw.rect(screen, color, (obs['x'], obs['y'], obs_width, obs_height))

def draw_power_ups(power_up_list):
    for (x, y) in power_up_list:
        pygame.draw.rect(screen, YELLOW, (x, y, power_up_width, power_up_height))

def draw_background():
    global bg1_x, bg2_x
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (bg1_x, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, GREEN, (bg2_x, 0, WIDTH, HEIGHT))
    bg1_x -= bg_speed
    bg2_x -= bg_speed
    if bg1_x <= -WIDTH:
        bg1_x = WIDTH
    if bg2_x <= -WIDTH:
        bg2_x = WIDTH

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_level(level):
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(level_text, (WIDTH - 100, 10))

def game_over():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    level_text = font.render(f"Final Level: {level}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(level_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    global dino_y, jumping, jump_count, obstacles, score, obs_vel, power_ups, power_up_timer, power_up_active, power_up_start_time, bg1_x, bg2_x, level, dino_frame
    run = True
    while run:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        # Dino animation
        dino_frame = (dino_frame + 1) % 2
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not jumping:
            jumping = True
        
        if jumping:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                dino_y -= (jump_count ** 2) * 0.4 * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = 10

        for obs in obstacles:
            if obs['behavior'] == 'fast':
                obs['x'] -= obs_vel * 1.5
            else:
                obs['x'] -= obs_vel
            if obs['x'] < 0:
                obs['x'] = WIDTH
                obs['type'] = random.choice(['type1', 'type2'])
                obs['behavior'] = random.choice(['normal', 'fast'])
                score += 1
                if score % level_up_score == 0:
                    level += 1
                    obs_vel += obs_speed_increase

        # Check for collision with obstacles
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        for obs in obstacles:
            obs_rect = pygame.Rect(obs['x'], obs['y'], obs_width, obs_height)
            if dino_rect.colliderect(obs_rect):
                game_over()
                return

        # Handle power-ups
        if not power_up_active and current_time - power_up_timer > power_up_interval:
            power_up_x = WIDTH
            power_up_y = HEIGHT - power_up_height - 10
            power_ups.append((power_up_x, power_up_y))
            power_up_timer = current_time

        if power_up_active and current_time - power_up_start_time > power_up_duration:
            power_up_active = False
            obs_vel = 15
            power_ups = []

        new_power_ups = []
        for (x, y) in power_ups:
            x -= obs_vel
            if x < 0:
                continue
            dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
            power_up_rect = pygame.Rect(x, y, power_up_width, power_up_height)
            if dino_rect.colliderect(power_up_rect):
                power_up_active = True
                power_up_start_time = current_time
                obs_vel = 5
                power_ups = []
            else:
                new_power_ups.append((x, y))
        power_ups = new_power_ups

        draw_background()
        draw_dino(dino_x, dino_y, dino_frame)
        draw_obstacles(obstacles)
        draw_power_ups(power_ups)
        draw_score(score)
        draw_level(level)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
