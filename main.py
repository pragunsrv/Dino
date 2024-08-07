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

# Dino settings
dino_width, dino_height = 50, 50
dino_x, dino_y = 50, HEIGHT - dino_height - 10
dino_vel = 10
jumping = False
jump_count = 10

# Obstacle settings
obs_width, obs_height = 50, 50
num_obstacles = 3
obstacles = [(WIDTH + i * 300, HEIGHT - obs_height - 10) for i in range(num_obstacles)]
obs_vel = 15

# Score
score = 0
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()
FPS = 30

def draw_dino(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, dino_width, dino_height))

def draw_obstacles(obs_list):
    for (x, y) in obs_list:
        pygame.draw.rect(screen, GRAY, (x, y, obs_width, obs_height))

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
    global dino_y, jumping, jump_count, obstacles, score
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

        for i in range(num_obstacles):
            obstacles[i] = (obstacles[i][0] - obs_vel, obstacles[i][1])
            if obstacles[i][0] < 0:
                obstacles[i] = (WIDTH, HEIGHT - obs_height - 10)
                score += 1
        
        # Check for collision
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        for (obs_x, obs_y) in obstacles:
            obs_rect = pygame.Rect(obs_x, obs_y, obs_width, obs_height)
            if dino_rect.colliderect(obs_rect):
                game_over()
                return

        screen.fill(WHITE)
        draw_dino(dino_x, dino_y)
        draw_obstacles(obstacles)
        draw_score(score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
