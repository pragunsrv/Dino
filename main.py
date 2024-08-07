import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dino settings
dino_width, dino_height = 50, 50
dino_x, dino_y = 50, HEIGHT - dino_height - 10
dino_vel = 10
jumping = False
jump_count = 10

# Obstacle settings
obs_width, obs_height = 50, 50
obs_x = WIDTH
obs_y = HEIGHT - obs_height - 10
obs_vel = 15

# Clock
clock = pygame.time.Clock()
FPS = 30

def draw_dino(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, dino_width, dino_height))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, obs_width, obs_height))

def main():
    global dino_y, jumping, jump_count, obs_x, obs_y
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

        obs_x -= obs_vel
        if obs_x < 0:
            obs_x = WIDTH
            obs_y = HEIGHT - obs_height - 10
        
        screen.fill(WHITE)
        draw_dino(dino_x, dino_y)
        draw_obstacle(obs_x, obs_y)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
