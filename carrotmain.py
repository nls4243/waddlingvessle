#wr = 43 seconds
#num2 = 59 seconds
import pygame
from pygame import mixer
import sys
import math

mixer.init()

playerspeed = 5

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, l, h, png):
        super().__init__()
        self.image = pygame.Surface((l, h))
        self.image = pygame.image.load(png)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = True
        self.direction = 1

    def move_invasion_pattern(self, speed, screen_width):
        if self.alive:
            self.rect.x += speed * self.direction
            if self.rect.right > screen_width or self.rect.left < 0:
                self.rect.y += 60
                self.direction *= -1
            self.rect.x += speed * self.direction

    def move_towards(self, speed):
        angle = math.atan2(-90, 0)
        self.rect.x += speed * math.cos(angle)
        self.rect.y += speed * math.sin(angle)

class Sprite2(pygame.sprite.Sprite):
    def __init__(self, x, y, l, h, png):
        super().__init__()
        self.image = pygame.Surface((l, h))
        self.image = pygame.image.load(png)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = True
        self.direction = 1

pygame.init()
width, height = 1000, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("carrots")
score = 0
red = (255, 0, 0)

#sprites
sprite1 = Sprite(width / 2, height / 2, 50, 50, 'bunny1.png')
all_sprites = pygame.sprite.Group()
all_sprites.add(sprite1)
background = pygame.sprite.Sprite()
background.image = pygame.image.load('background2.png')
background.rect = background.image.get_rect()
background.rect.center = (0, 0)

#music
mixer.music.load('carrots.wav')
mixer.music.set_volume(0.5)

grid_color = (0, 0, 0)
grid_spacing = 50
grid = [[{'rect': None, 'timer': 0, 'image': None} for _ in range((width * 2) // grid_spacing)] for _ in range((height * 2) // grid_spacing)]

start_time = pygame.time.get_ticks()

carrot_seed_plot = pygame.image.load('carrotseedplot.png')
fully_grown_carrot = pygame.image.load('fullygrowncarrot.png')

clock = pygame.time.Clock()
running = True

def draw_grid():
    for x in range(0, width, grid_spacing):
        pygame.draw.line(screen, grid_color, (x, 0), (x, height))

    for y in range(0, height, grid_spacing):
        pygame.draw.line(screen, grid_color, (0, y), (width, y))

def fill_grid_square(gridX, gridY):
    grid[gridY][gridX]['rect'] = pygame.Rect(gridX * grid_spacing, gridY * grid_spacing, grid_spacing, grid_spacing)
    grid[gridY][gridX]['timer'] = 0

mixer.music.play()
while running:
    keys = pygame.key.get_pressed()
    screen.blit(background.image, background.rect)

    draw_grid()

    for row in grid:
        for square in row:
            if square['rect'] is not None:
                if square['image'] is None:
                    square['image'] = 'carrotseedplot.png'
                    square['timer'] += 1
                    if square['timer'] >= 300:
                        square['image'] = 'fullygrowncarrot.png'
                        square['timer'] = 0
                        score += 10
                else:
                    square['timer'] += 1
                    if square['timer'] >= 300:
                        square['image'] = 'fullygrowncarrot.png'
                        square['timer'] = 0
                        score += 10

                # Load image once and blit it onto the screen
                if square['image'] == 'carrotseedplot.png':
                    screen.blit(carrot_seed_plot, square['rect'].topleft)
                elif square['image'] == 'fullygrowncarrot.png':
                    screen.blit(fully_grown_carrot, square['rect'].topleft)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX = mouseX // grid_spacing
            gridY = mouseY // grid_spacing
            fill_grid_square(gridX, gridY)

    clock.tick(60)

pygame.quit()
sys.exit()
