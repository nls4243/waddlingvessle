import pygame
import sys
import math

playerspeed = 5

pygame.init()
# Set up display
width, height = 1500, 960
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("carrots")
score = 0
red = (255, 0, 0)
class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, l, h, png):
        super().__init__()
        self.image = pygame.Surface((l, h))
        self.image = pygame.image.load(png) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = True
        self.direction = 1  # Initial direction (1 for right, -1 for left)

    def move_invasion_pattern(self, speed, screen_width):
        if self.alive:
            self.rect.x += speed * self.direction

            # Check if the sprite has hit the edge of the screen
            if self.rect.right > screen_width or self.rect.left < 0:
                self.rect.y += 60  # Move down by 30 pixels
                self.direction *= -1  # Change direction

            self.rect.x += speed * self.direction

    def move_towards(self, speed):
        angle = math.atan2(-90, 0)
        self.rect.x += speed * math.cos(angle)
        self.rect.y += speed * math.sin(angle)

sprite1 = Sprite(width / 2, height / 2, 100, 100, 'bunny1.png')
all_sprites = pygame.sprite.Group()
all_sprites.add(sprite1)
background = pygame.sprite.Sprite()
background.image = pygame.image.load('background2.png')
background.rect = background.image.get_rect()
background.rect.center = (0, 0)

# Grid setup
grid_color = (0, 0, 0)
grid_spacing = 50  # Adjust this value to change the spacing of the grid lines

# Modified grid to include timer and color state for each square
grid = [[{'rect': None, 'timer': 0, 'color': (139, 69, 19)} for _ in range((width*2) // grid_spacing)] for _ in range((height*2) // grid_spacing)]

# Variable to keep track of the elapsed time
start_time = pygame.time.get_ticks()

clock = pygame.time.Clock()
running = True

while running:
    keys = pygame.key.get_pressed()
    screen.blit(background.image, background.rect)
    
    for row in grid:
        for square in row:
            if square['rect'] is not None:
                # Check the image in the square
                if  square.has_key('image):
                    screen.blit(square['image'], square['rect'].topleft)

    

    # Draw a grid over the background
    for x in range(0, width, grid_spacing):
        pygame.draw.line(screen, grid_color, (x, 0), (x, height))
    
    for y in range(0, height, grid_spacing):
        pygame.draw.line(screen, grid_color, (0, y), (width, y))

    # old code
    """for row in grid:
        for square in row:
            if square['rect'] is not None:
                pygame.draw.rect(screen, square['color'], square['rect'])

                # Update timer and change color to green after 5 seconds
                square['timer'] += 1
                if square['timer'] >= 300:  # 60 frames per second * 5 seconds
                    square['color'] = (0, 255, 0)  # Change color to green
                    square['timer'] = 0  # Reset timer"""
     # Draw filled grid squares
    for row in grid:
        for square in row:
            if square['rect'] is not None:
                # Check the image in the square
                if square['image'] == None:
                    square['image'] = pygame.image.load('carrotseedplot.png')
                    square['timer'] += 1
                    if square['timer'] >= 300:  # 60 frames per second * 5 seconds
                        square['image'] = pygame.image.load('fullygrowncarrot.png') # Change image to carrot seed plot
                        square['timer'] = 0  # Reset timer
                        score += 10

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the grid position based on mouse click
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX = mouseX // grid_spacing
            gridY = mouseY // grid_spacing

            # Fill the grid square with brown color
            grid[gridY][gridX]['rect'] = pygame.Rect(gridX * grid_spacing, gridY * grid_spacing, grid_spacing, grid_spacing)
            grid[gridY][gridX]['timer'] = 0  # Reset timer when the square is filled

    # Draws sprites to the screen
    all_sprites.draw(screen)

     # Displays score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, red)
    screen.blit(score_text, (10, 10))

    # Updates the display
    pygame.display.flip()

    # Move the player
    if keys[pygame.K_w]:
        sprite1.rect.y -= playerspeed
    if keys[pygame.K_s]:
        sprite1.rect.y += playerspeed
    if keys[pygame.K_a]:
        sprite1.rect.x -= playerspeed
    if keys[pygame.K_d]:
        sprite1.rect.x += playerspeed

    sprite1.rect.x = max(sprite1.rect.x, 0)
    sprite1.rect.x = min(sprite1.rect.x, width - sprite1.rect.width)
    sprite1.rect.y = max(sprite1.rect.y, 0)
    sprite1.rect.y = min(sprite1.rect.y, height - sprite1.rect.height)
        
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
