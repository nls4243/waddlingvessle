import pygame
from pygame import *
import time
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1000, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Crop Simulation")

# Load images
empty_crop_plot = pygame.image.load("emptycropplot.png")
carrot_seed_plot = pygame.image.load("carrotseedplot.png")
fully_grown_carrot = pygame.image.load("fullygrowncarrot.png")

#class for counting values
class Counter:
    def __init__(self):
        self.value = 0

    def addscore(self, amount):
        self.value += amount

#class for player sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, l, h, png):
        super().__init__()
        self.image = pygame.Surface((l, h))
        self.image = pygame.image.load(png)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = True
        self.direction = 1

#class for other sprites
class simplesprite(pygame.sprite.Sprite):
    def __init__(self, png):
        self.image = pygame.image.load(png)
        self.rect = self.image.get_rect()
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex + 15, mousey + 15)

#sprites
sprite1 = Sprite(width / 2, height / 2, 50, 50, 'bunny1.png')#player sprite
all_sprites = pygame.sprite.Group()
all_sprites.add(sprite1)

background = simplesprite('background2.png')
background.rect.center = (width / 2, height / 2)

carrotitem = simplesprite('justcarrot.png')

carrotseeds = simplesprite('carrotseedpack.png')

gardenhoe = simplesprite('gardenhoe.png')

gardenglove = simplesprite('gardenglove.png')

coin = simplesprite('coin.png')

hotbarUI = simplesprite('carrothotbarUI.png')
hotbarUI.rect.center = (width / 2, height - (hotbarUI.rect.height/2))

highlight = simplesprite('highlight.png')
highlight.rect.center = (width / 2 - 86, height - (hotbarUI.rect.height/2))

#note to self make a py group of simple sprites

# Set up grid
grid_size = 50
rows, cols = width // grid_size, width // grid_size
grid = [[0] * cols for _ in range(rows)]

# Set up clock
clock = pygame.time.Clock()

# Define a dictionary to store the state and planting time of each grid square
grid_state = {(row, col): (0, 0) for row in range(rows) for col in range(cols)}
#dictionary that keeps tracks of the items the player has
itemdict = ['carrotseed', 'carrot', 'hoe', 'gardenglove', 'coin']

#some variables and such
itemdictc = len(itemdict) - 1
carrotseed = Counter()
carrots = Counter()
hoe_durability = Counter()
coinage = Counter()
selected = None
placing_crop = True
running = True
RUNNING = True
move_ticker = 0
playerspeed = 3
dnum = 0
hoe_durability.value = 6
carrotseed.addscore(15)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 153)

#music
mixer.music.load('carrots.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

#while loop
while running:
    keys = pygame.key.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()

    #display background
    screen.blit(background.image, background.rect)

    #set where the sprites will be displayed
    carrotitem.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
    carrotseeds.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
    gardenhoe.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
    gardenglove.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
    coin.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)

    #prevents registering multiple key presses from one
    if move_ticker > 0:
        move_ticker -= 1

    #cycles through the keyboard
    if keys[pygame.K_TAB] and move_ticker == 0:
        move_ticker = 10
        dnum = (dnum + 1)
        highlight.rect.x += 34
        if dnum > itemdictc:
            highlight.rect.center = (width / 2 - 86, height - (hotbarUI.rect.height/2))
            dnum = 0

    #hotbar keys
    if keys[pygame.K_1]:
        dnum = 0
        highlight.rect.center = (width / 2 - 86, height - (hotbarUI.rect.height/2))
    if keys[pygame.K_2]:
        dnum = 1
        highlight.rect.center = (width / 2 - 86 + 34, height - (hotbarUI.rect.height/2))
    if keys[pygame.K_3]:
        dnum = 2
        highlight.rect.center = (width / 2 - 86 + 34*2, height - (hotbarUI.rect.height/2))
    if keys[pygame.K_4]:
        dnum = 3
        highlight.rect.center = (width / 2 - 86 + 34*3, height - (hotbarUI.rect.height/2))
    if keys[pygame.K_5]:
        dnum = 4
        highlight.rect.center = (width / 2 - 86 + 34*4, height - (hotbarUI.rect.height/2))

    #what item the player is currently holding
    itemhave = itemdict[dnum]

    # creates the grid
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * grid_size, row * grid_size, grid_size, grid_size)

            # Display the appropriate crop state based on the grid state
            state, planting_time = grid_state[(row, col)]
            if state == 1:
                screen.blit(empty_crop_plot, rect.topleft)
            elif state == 2:
                screen.blit(carrot_seed_plot, rect.topleft)
            elif state == 3:
                screen.blit(fully_grown_carrot, rect.topleft)
            #DO NOT REMOVE STATE 4 THIS WILL MAKE THE CODE STOP WORKING I DO NOT KNOW WHY
            elif state == 4:
                screen.blit(empty_crop_plot, rect.topleft)
            # Check if the seed has been planted and update to fully grown state after 3 seconds
            if state == 2 and time.time() - planting_time > 3:
                grid_state[(row, col)] = (3, planting_time)  # Mark as fully grown

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = x // grid_size
                row = y // grid_size

                playerx = sprite1.rect.x
                playery = sprite1.rect.y
                
                #Nathan this is your homework pls improve
                #if x < (playerx + 32) + 85 and x > (playerx - 32) - 85 and y < (playery + 32) + 88 and y > (playery - 32) - 100:

                if placing_crop:
                    # Place empty crop plot if the square is empty
                    if grid_state[(row, col)][0] == 0 or 4: #DO NOT REMOVE OR 4 STATEMNT CODE WILL STOP WORKING IDK WHY
                        if grid_state[(row, col)][0] == 0 and itemhave == 'hoe' and hoe_durability.value > 0:
                            grid_state[(row, col)] = (1, 0)  # Mark as empty crop plot
                            hoe_durability.addscore(-1)
                        elif grid_state[(row, col)][0] == 1 and itemhave == 'carrotseed' and carrotseed.value > 0:
                            grid_state[(row, col)] = (2, time.time())  # Change to seeded crop plot and start timer to grow carrot
                            carrotseed.addscore(-1)
                        elif grid_state[(row, col)][0] == 3 and itemhave == 'gardenglove':
                            grid_state[(row, col)] = (1, 0)
                            carrots.addscore(1)
                else:
                    # Plant a new seed if the square has an empty crop plot
                    if grid_state[(row, col)][0] == 1:
                        grid_state[(row, col)] = (2, time.time())  # Mark as seed planted and start timer to grow carrot

    #display hotbar
    screen.blit(hotbarUI.image, hotbarUI.rect)
    screen.blit(highlight.image, highlight.rect)

    # display the player and the item that is in his hand
    all_sprites.draw(screen)
    if itemhave == 'carrot':
        screen.blit(carrotitem.image, carrotitem.rect)
    if itemhave == 'carrotseed':
        screen.blit(carrotseeds.image, carrotseeds.rect)
    if itemhave == 'hoe':
        screen.blit(gardenhoe.image, gardenhoe.rect)
    if itemhave == 'gardenglove':
        screen.blit(gardenglove.image, gardenglove.rect)
    if itemhave == 'coin':
        screen.blit(coin.image, coin.rect)

    #score counters
    font = pygame.font.Font(None, 36)
    carrots_text = font.render(f"carrots: {carrots.value}", True, WHITE)
    screen.blit(carrots_text, (10, 10))

    font = pygame.font.Font(None, 36)
    carrotseed_text = font.render(f"carrot seeds: {carrotseed.value}", True, WHITE)
    screen.blit(carrotseed_text, (10, 30))

    font = pygame.font.Font(None, 36)
    hoelife_text = font.render(f"hoe durability: {hoe_durability.value}", True, WHITE)
    screen.blit(hoelife_text, (10, 50))

    font = pygame.font.Font(None, 36)
    coin_text = font.render(f"coins: {coinage.value}", True, WHITE)
    screen.blit(coin_text, (10, 70))

    font = pygame.font.Font(None, 36)
    controls_text = font.render("ESC for controls", True, WHITE)
    screen.blit(controls_text, (10, 90))

    #display controls is esc is pressed
    if keys[pygame.K_ESCAPE]:
        font = pygame.font.Font(None, 36)
        hoelife_text = font.render("press 7 to replenish seeds for 10 coins", True, RED)
        screen.blit(hoelife_text, (10, 150))

        font = pygame.font.Font(None, 36)
        sell_text = font.render("press 6 to sell carrots", True, RED)
        screen.blit(sell_text, (10, 130))

        font = pygame.font.Font(None, 36)
        sell_text = font.render("press 8 to repair hoe for 20 coins", True, RED)
        screen.blit(sell_text, (10, 170))

        font = pygame.font.Font(None, 36)
        sell_text = font.render("use 1-5 or TAB for item select", True, RED)
        screen.blit(sell_text, (10, 110))

        font = pygame.font.Font(None, 36)
        move_text = font.render("WASD to move", True, RED)
        screen.blit(move_text, (10, 190))

        font = pygame.font.Font(None, 36)
        hoe_text = font.render("""use hoe to place crop plot""", True, RED)
        screen.blit(hoe_text, (10, 210))

        font = pygame.font.Font(None, 36)
        seed_text = font.render("""use seeds to plant crops""", True, RED)
        screen.blit(seed_text, (10, 230))

        font = pygame.font.Font(None, 36)
        glove_text = font.render("""use glove to harvest crops""", True, RED)
        screen.blit(glove_text, (10, 250))

    #current buy and sell controls
    if keys[pygame.K_6]:
        coinage.addscore(carrots.value*2)
        carrots.value = 0
    if keys[pygame.K_8] and hoe_durability.value < 6 and move_ticker == 0 and carrots.value*2 + coinage.value + carrotseed.value*2 >= 30:
        hoe_durability.value = 6
        coinage.addscore(-20)
        move_ticker = 10
    if keys[pygame.K_7] and coinage.value >= 10 and move_ticker == 0: #this will always do 2x idk why just leave it
        coinage.addscore(-10)
        carrotseed.addscore(10)
        move_ticker = 10

    #update display
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
    # Cap the player's position
    sprite1.rect.x = max(0, min(sprite1.rect.x, width - sprite1.rect.width))
    sprite1.rect.y = max(0, min(sprite1.rect.y, height - sprite1.rect.height))

    # Cap the frame rate
    clock.tick(60)
# Quit Pygame
pygame.quit()
#reminder on how to check collision
#if sprite1.colliderect(carrotseeds.rect):
    #print('hit')
