import pygame
from pygame import *
import time
import random

# Initialize Pygame
pygame.init()
#other variables and such
playerspeed = 5
score = 0
itemdict = ['carrotseed', 'carrot', 'hoe', 'gardenglove', 'coin']
itemdictc = len(itemdict) - 1

selected = None
dnum = 0
# Set up display
width, height = 1000, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Crop Simulation")
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 153)

# Load images
empty_crop_plot = pygame.image.load("emptycropplot.png")
carrot_seed_plot = pygame.image.load("carrotseedplot.png")
fully_grown_carrot = pygame.image.load("fullygrowncarrot.png")

def addscore():
    global score
    while True:
        score += 1
        break

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

#music
mixer.music.load('carrots.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Set up grid
grid_size = 50
rows, cols = width // grid_size, width // grid_size
grid = [[0] * cols for _ in range(rows)]

# Set up clock
clock = pygame.time.Clock()

# Define a dictionary to store the state and planting time of each grid square
grid_state = {(row, col): (0, 0) for row in range(rows) for col in range(cols)}

#these are the images that get shown as items, different color circle for each item
items = [pygame.Surface((50,50),pygame.SRCALPHA) for x in range(4)]
pygame.draw.circle(items[0],(255,0,0),(25,25),25)
pygame.draw.circle(items[1],(0,255,0),(25,25),25)
pygame.draw.circle(items[2],(255,255,0),(25,25),25)
pygame.draw.circle(items[3],(0,0,255),(25,25),25)

#class for a item, just holds the surface and can resize it
class Item:
    def __init__(self,id):
        self.id = id
        self.surface = items[id]
    
    def resize(self,size):
        return pygame.transform.scale(self.surface,(size,size))

#the inventory system
class Inventory:
    def __init__(self):
        self.rows = 3
        self.col = 9
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 48
        self.x = 50
        self.y = 50
        self.border = 3
    
    #draw everything
    def draw(self):
        #draw background
        pygame.draw.rect(screen,(100,100,100),
                         (self.x,self.y,(self.box_size + self.border)*self.col + self.border,(self.box_size + self.border)*self.rows + self.border))
        for x in range(self.col):
            for y in range(self.rows):
                rect = (self.x + (self.box_size + self.border)*x + self.border,self.x + (self.box_size + self.border)*y + self.border,self.box_size,self.box_size )
                pygame.draw.rect(screen,(180,180,180),rect)
                if self.items[x][y]:
                    screen.blit(self.items[x][y][0].resize(self.box_size),rect)
                    obj = font.render(str(self.items[x][y][1]),True,(0,0,0))
                    screen.blit(obj,(rect[0] + self.box_size//2, rect[1] + self.box_size//2))
                    
    #get the square that the mouse is over
    def Get_pos(self):
        mouse = pygame.mouse.get_pos()
        
        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x//(self.box_size + self.border)
        y = y//(self.box_size + self.border)
        return (x,y)
    
    #add an item/s
    def Add(self,Item,xy):
        x, y = xy
        if self.items[x][y]:
            if self.items[x][y][0].id == Item[0].id:
                self.items[x][y][1] += Item[1]
            else:
                temp = self.items[x][y]
                self.items[x][y] = Item
                return temp
        else:
            self.items[x][y] = Item
    
    #check whether the mouse in in the grid
    def In_grid(self,x,y):
        if 0 > x > self.col-1:
            return False
        if 0 > y > self.rows-1:
            return False
        return True
player_inventory = Inventory()
running = True
placing_crop = True
44

#while loop
while running:
    keys = pygame.key.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()
    screen.blit(background.image, background.rect)
    carrotitem.rect.center = (mousex + 15, mousey + 15)
    carrotseeds.rect.center = (mousex + 15, mousey + 15)
    gardenhoe.rect.center = (mousex + 15, mousey + 15)
    gardenglove.rect.center = (mousex + 15, mousey + 15)
    coin.rect.center = (mousex + 15, mousey + 15)
    if keys[pygame.K_TAB]:
        time.sleep(0.15)
        dnum = (dnum + 1)
        highlight.rect.x += 34
        if dnum > itemdictc:
            highlight.rect.center = (width / 2 - 86, height - (hotbarUI.rect.height/2))
            dnum = 0
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


    itemhave = itemdict[dnum]

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * grid_size, row * grid_size, grid_size, grid_size)

            # Display the appropriate image based on the grid state
            state, planting_time = grid_state[(row, col)]
            if state == 1:
                screen.blit(empty_crop_plot, rect.topleft)
            elif state == 2:
                screen.blit(carrot_seed_plot, rect.topleft)
            elif state == 3:
                screen.blit(fully_grown_carrot, rect.topleft)
            #DO NOT REMOVE STATE 4 THIS WILL MAKE THE CODE STOP WORKING
            #NO I DO NOT KNOW WHY IT DOESN'T WORK
            elif state == 4:
                screen.blit(empty_crop_plot, rect.topleft)
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
                if grid_state[(row, col)][0] == 0 or 4: #DO NOT REMOVE OR STATEMNT WILL STOP WORKING IDK WHY
                    if grid_state[(row, col)][0] == 0 and itemhave == 'hoe':
                        grid_state[(row, col)] = (1, 0)  # Mark as empty crop plot
                    elif grid_state[(row, col)][0] == 1 and itemhave == 'carrotseed':
                        grid_state[(row, col)] = (2, time.time())  # Change to seeded variant
                    elif grid_state[(row, col)][0] == 3 and itemhave == 'gardenglove':
                        grid_state[(row, col)] = (1, 0)
                        addscore()
            else:
                # Plant a new seed if the square has an empty crop plot
                if grid_state[(row, col)][0] == 1:
                    grid_state[(row, col)] = (2, time.time())  # Mark as seed planted and store planting time

        elif keys[pygame.K_SPACE]:
            going = True
            while going:
                keys = pygame.key.get_pressed()
                pygame.display.update()
                screen.blit(background.image, background.rect)
                all_sprites.draw(screen)
                player_inventory.draw()
                mousex, mousey = pygame.mouse.get_pos()
                for row in range(rows):
                    for col in range(cols):
                        rect = pygame.Rect(col * grid_size, row * grid_size, grid_size, grid_size)
                        # Display the appropriate image based on the grid state
                        state, planting_time = grid_state[(row, col)]
                        if state == 1:
                            screen.blit(empty_crop_plot, rect.topleft)
                        elif state == 2:
                            screen.blit(carrot_seed_plot, rect.topleft)
                        elif state == 3:
                            screen.blit(fully_grown_carrot, rect.topleft)
                        #DO NOT REMOVE STATE 4 THIS WILL MAKE THE CODE STOP WORKING
                        #NO I DO NOT KNOW WHY IT DOESN'T WORK
                        elif state == 4:
                            screen.blit(empty_crop_plot, rect.topleft)
                        # Check if the seed has been planted and update to fully grown state after 3 seconds
                        if state == 2 and time.time() - planting_time > 3:
                            grid_state[(row, col)] = (3, planting_time)  # Mark as fully grown
                if selected:
                    screen.blit(selected[0].resize(30),(mousex,mousey))
                    obj = font.render(str(selected[1]),True,(0,0,0))
                    screen.blit(obj,(mousex + 15, mousey + 15))
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        #if right clicked, get a random item
                        if e.button == 3:
                            selected = [Item(random.randint(0,3)),1]
                        elif e.button == 1:
                            pos = player_inventory.Get_pos()
                            if player_inventory.In_grid(pos[0],pos[1]):
                                if selected:
                                    selected = player_inventory.Add(selected,pos)
                                elif player_inventory.items[pos[0]][pos[1]]:
                                    selected = player_inventory.items[pos[0]][pos[1]]
                                    player_inventory.items[pos[0]][pos[1]] = None
                if keys[pygame.K_ESCAPE]:
                    going = False
                player_inventory.draw()
    screen.blit(hotbarUI.image, hotbarUI.rect)
    screen.blit(highlight.image, highlight.rect)

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

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"carrots: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    if keys[pygame.K_w]:
        sprite1.rect.y -= playerspeed
    if keys[pygame.K_s]:
        sprite1.rect.y += playerspeed
    if keys[pygame.K_a]:
        sprite1.rect.x -= playerspeed
    if keys[pygame.K_d]:
        sprite1.rect.x += playerspeed

    sprite1.rect.x = max(0, min(sprite1.rect.x, width - sprite1.rect.width))
    sprite1.rect.y = max(0, min(sprite1.rect.y, height - sprite1.rect.height))

    # Cap the frame rate
    clock.tick(60)
# Quit Pygame
pygame.quit()
