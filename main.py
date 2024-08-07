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

# Dino settings
dino_width, dino_height = 50, 50
dino_x, dino_y = 50, HEIGHT - dino_height - 10
dino_vel = 10
jumping = False
jump_count = 10

# Obstacle settings
obs_width, obs_height = 50, 50
num_obstacles = 3
obstacles = []
for i in range(num_obstacles):
    obs_type = random.choice(['type1', 'type2'])
    x_pos = WIDTH + i * 300
    obstacles.append({'x': x_pos, 'y': HEIGHT - obs_height - 10, 'type': obs_type})

obs_vel = 15
obs_speed_increase = 1

# Background settings
bg_x1 = 0
bg_x2 = WIDTH
bg_speed = 5

# Score
score = 0
font = pygame.font.Font(None, 36)

def draw_dino(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, dino_width, dino_height))

def draw_obstacles(obs_list):
    for obs in obs_list:
        color = GRAY if obs['type'] == 'type1' else BLUE
        pygame.draw.rect(screen, color, (obs['x'], obs['y'], obs_width, obs_height))

def draw_background():
    global bg_x1, bg_x2
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (bg_x1, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, GREEN, (bg_x2, 0, WIDTH, HEIGHT))
    bg_x1 -= bg_speed
    bg_x2 -= bg_speed
    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= -WIDTH:
        bg_x2 = WIDTH

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def game_over():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    global dino_y, jumping, jump_count, obstacles, score, obs_vel, bg_x1, bg_x2
    run = True
    while run:
        clock.tick(FPS)
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
            obs['x'] -= obs_vel
            if obs['x'] < 0:
                obs['x'] = WIDTH
                obs['type'] = random.choice(['type1', 'type2'])
                score += 1
                if score % 5 == 0:
                    obs_vel += obs_speed_increase

        # Check for collision
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        for obs in obstacles:
            obs_rect = pygame.Rect(obs['x'], obs['y'], obs_width, obs_height)
            if dino_rect.colliderect(obs_rect):
                game_over()
                return

        draw_background()
        draw_dino(dino_x, dino_y)
        draw_obstacles(obstacles)
        draw_score(score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
