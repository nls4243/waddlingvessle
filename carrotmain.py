import pygame
import random

WIDTH, HEIGHT = 1000, 500
BG = (50, 50, 50)
carrot = 0
center_area_size = 50
playerspeed = 1
running = True
psprite = 'life1.png'

#level
lvl_map = ('background.png', (4000, 4000))#second half is map size

#settings
def exit_proc():
	pygame.quit()
	quit()

#main
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')

# Set up the sprite
sprite = pygame.sprite.Sprite()
sprite.image = pygame.image.load('bunny.png')
sprite.rect = sprite.image.get_rect()
sprite.rect.center = (WIDTH / 2, HEIGHT / 2)

#collisionblock
carrot = pygame.sprite.Sprite()
carrot.image = pygame.image.load('carrot.png')
carrot.rect = carrot.image.get_rect()
carrot.rect.center = (0, 0)

#background
background = pygame.sprite.Sprite()
background.image = pygame.image.load(lvl_map[0]).convert_alpha()
background.rect = background.image.get_rect()
background.rect.center = (WIDTH / 2, HEIGHT / 2)

win = pygame.sprite.Sprite()
win.image = pygame.image.load(lvl_map[0]).convert_alpha()
win.rect = win.image.get_rect()
win.rect.center = (0, 0)

while running:
	
	#update background
    screen.fill(BG)
    screen.blit(background.image, background.rect)
    screen.blit(carrot.image, carrot.rect)
    screen.blit(carrot.image, carrot.rect)
    
    if carrot.rect.colliderect(sprite.rect):
        carrot.rect.center = (0, 0)

	#show player image
    screen.blit(sprite.image, sprite.rect)

	#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
	
	# Update the display
    pygame.display.update()
   
    # Keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: # Left arrow key
        background.rect.x += playerspeed
        carrot.rect.x += playerspeed
    if keys[pygame.K_d]: # Right arrow key
        background.rect.x -= playerspeed
        carrot.rect.x -= playerspeed
    if keys[pygame.K_w]: # Up arrow key
        background.rect.y += playerspeed
        carrot.rect.y += playerspeed
    if keys[pygame.K_s]: # Down arrow key
        background.rect.y -= playerspeed
        carrot.rect.y -= playerspeed

pygame.quit()