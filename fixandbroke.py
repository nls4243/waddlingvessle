import pygame
from pygame import *
import time

# Initialize Pygame
pygame.init()

playerspeed = 5
score = 0
red = (255, 0, 0)

# Set up display
width, height = 1000, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Crop Simulation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
empty_crop_plot = pygame.image.load("emptycropplot.png")
carrot_seed_plot = pygame.image.load("carrotseedplot.png")
fully_grown_carrot = pygame.image.load("fullygrowncarrot.png")

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, l, h, png):
        super().__init__()
        self.image = pygame.Surface((l, h))
        self.image = pygame.image.load(png)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = True
        self.direction = 1

#sprites
sprite1 = Sprite(width / 2, height / 2, 50, 50, 'bunny1.png')
all_sprites = pygame.sprite.Group()
all_sprites.add(sprite1)
background = pygame.sprite.Sprite()
background.image = pygame.image.load('background2.png')
background.rect = background.image.get_rect()
background.rect.center = (0, 0)

def addscore():
    global score
    continu = True
    while continu:
        score += 10
        continu = False

#music
mixer.music.load('carrots.wav')
mixer.music.set_volume(0.5)


# Set up grid
grid_size = 50
rows, cols = width // grid_size, width // grid_size
grid = [[0] * cols for _ in range(rows)]

# Set up clock
clock = pygame.time.Clock()

# Define a dictionary to store the state and planting time of each grid square
grid_state = {(row, col): (0, 0) for row in range(rows) for col in range(cols)}

# Main game loop
running = True
placing_crop = True

while running:
    keys = pygame.key.get_pressed()
    screen.blit(background.image, background.rect)
    mixer.music.play(-1)

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * grid_size, row * grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Draw grid outline

            # Display the appropriate image based on the grid state
            state, planting_time = grid_state[(row, col)]
            if state == 1:
                screen.blit(empty_crop_plot, rect.topleft)
            elif state == 2:
                screen.blit(carrot_seed_plot, rect.topleft)
            elif state == 3:
                screen.blit(fully_grown_carrot, rect.topleft)
                addscore()
            # Check if the seed has been planted and update to fully grown state after 3 seconds
            if state == 2 and time.time() - planting_time > 3:
                grid_state[(row, col)] = (3, planting_time)  # Mark as fully grown


    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            col = x // grid_size
            row = y // grid_size

            if placing_crop:
                # Place empty crop plot if the square is empty
                if grid_state[(row, col)][0] == 0:
                    grid_state[(row, col)] = (1, 0)  # Mark as empty crop plot
                elif grid_state[(row, col)][0] == 1:
                    grid_state[(row, col)] = (2, time.time())  # Change to seeded variant
            else:
                # Plant a new seed if the square has an empty crop plot
                if grid_state[(row, col)][0] == 1:
                    grid_state[(row, col)] = (2, time.time())  # Mark as seed planted and store planting time

    all_sprites.draw(screen)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, red)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    if keys[pygame.K_w]:
        sprite1.rect.y -= playerspeed
    elif keys[pygame.K_s]:
        sprite1.rect.y += playerspeed
    elif keys[pygame.K_a]:
        sprite1.rect.x -= playerspeed
    elif keys[pygame.K_d]:
        sprite1.rect.x += playerspeed

    sprite1.rect.x = max(0, min(sprite1.rect.x, width - sprite1.rect.width))
    sprite1.rect.y = max(0, min(sprite1.rect.y, height - sprite1.rect.height))

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

