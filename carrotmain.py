import pygame
from pygame import *
import time
import random
import math
import sys
import pickle

# Initialize Pygame
pygame.init()

#variables and stuff
window_width, window_height = 1000, 500
white = (255, 255, 255)
button_color = (50, 150, 255)
BLUE = (0, 0, 255)
running = True
open_game = False
in_pain = True

# Create the starting window
start_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Main Window")

#sprites
main_menu = pygame.sprite.Sprite()
main_menu.image = pygame.image.load('main_screen.png')
main_menu.rect = main_menu.image.get_rect()
main_menu.rect.center = (window_width / 2, window_height / 2)

new_button = pygame.sprite.Sprite()
new_button.image = pygame.image.load('newgame_button.png')
new_button.rect = new_button.image.get_rect()
new_button.rect.center = ((window_width / 2)+8, (window_height / 2)+35)

exit_button = pygame.sprite.Sprite()
exit_button.image = pygame.image.load('exit_button.png')
exit_button.rect = exit_button.image.get_rect()
exit_button.rect.center = ((window_width / 2)+8, (window_height / 2) + 100)

load_button = pygame.sprite.Sprite()
load_button.image = pygame.image.load('load_button.png')
load_button.rect = load_button.image.get_rect()
load_button.rect.center = ((window_width / 2)+8, (window_height / 2) - 30)

load_saved = False

#starting window loop
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
    start_window.blit(main_menu.image, main_menu.rect)
    start_window.blit(new_button.image, new_button.rect)
    start_window.blit(load_button.image, load_button.rect)
    start_window.blit(exit_button.image, exit_button.rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_button.rect.colliderect(mouse_rect):
                open_game = True
                running = False
            elif load_button.rect.colliderect(mouse_rect):
                load_saved = True
                open_game = True
                running = False
            elif exit_button.rect.colliderect(mouse_rect):
                pygame.quit()

    pygame.display.flip()

#start main game
if open_game:

    # Set up display
    width, height = 1000, 500
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CARROT GAME")

    new_window_running = True
    while new_window_running:

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

        # Set up player sprite
        sprite1 = Sprite(width / 2, height / 2, 50, 50, 'bunny1.png')#player sprite
        all_sprites = pygame.sprite.Group()
        all_sprites.add(sprite1)

        background = simplesprite('background.png')
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

        # Define a dictionary to store the state and planting time of each grid square
        grid_state = {(row, col): (0, 0) for row in range(rows) for col in range(cols)}


    #User Data for file pickeling
        #stuff for player invo
        itemdict = ['carrotseed', 'carrot', 'hoe', 'gardenglove', 'coin']
        carrotseed = Counter()
        carrots = Counter()
        hoe_durability = Counter()
        coinage = Counter()
        #some variables and such
        itemdictc = len(itemdict) - 1
        selected = None
        placing_crop = True
        running = True
        RUNNING = True
        move_ticker = 0
        playerspeed = 3
        dnum = 0
        hoe_durability.value = 6
        carrotseed.addscore(15)
        # Set up clock
        clock = pygame.time.Clock()
    #end of block

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        YELLOW = (255, 255, 153)
        BLUE = (0, 0, 255)

        #music
        volume = 1
        mixer.music.load('carrots.wav')
        mixer.music.play(-1)

        def save():
            userdat = [
                itemdict,
                carrotseed,
                carrots,
                hoe_durability,
                coinage,
                itemdictc,
                selected,
                placing_crop,
                True,
                RUNNING,
                move_ticker,
                playerspeed,
                dnum,
                hoe_durability,
                grid_state
            ]

            pickle.dump(userdat, open("saveddata" + ".crtusrdat", "wb"))
            

        if load_saved == True:
            userdat = pickle.load(open("saveddata" + ".crtusrdat", "rb"))
            itemdict = userdat[0]
            carrotseed = userdat[1]
            carrots = userdat[2]
            hoe_durability = userdat[3]
            coinage = userdat[4]
            itemdictc = userdat[5]
            selected = userdat[6]
            placing_crop = userdat[7]
            running  = userdat[8]
            RUNNING = userdat[9]
            move_ticker = userdat[10]
            playerspeed = userdat[11]
            dnum = userdat[12]
            hoe_durability = userdat[13]
            grid_state = userdat[14]





        #while loop
        while running:
            mixer.music.set_volume(volume)
            keys = pygame.key.get_pressed()
            mousex, mousey = pygame.mouse.get_pos()

            #display background
            screen.blit(background.image, background.rect)

            #set where the sprites will be displayed
            carrotitem.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            carrotseeds.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            gardenhoe.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            gardenglove.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 45)
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
            if dnum == 0:
                highlight.rect.center = (width / 2 - 86, height - (hotbarUI.rect.height/2))
            if keys[pygame.K_2]:
                dnum = 1
            if dnum == 1:
                highlight.rect.center = (width / 2 - 86 + 34, height - (hotbarUI.rect.height/2))
            if keys[pygame.K_3]:
                dnum = 2
            if dnum == 2:
                highlight.rect.center = (width / 2 - 86 + 34*2, height - (hotbarUI.rect.height/2))
            if keys[pygame.K_4]:
                dnum = 3
            if dnum == 3:
                highlight.rect.center = (width / 2 - 86 + 34*3, height - (hotbarUI.rect.height/2))
            if keys[pygame.K_5]:
                dnum = 4
            if dnum == 4:
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
                    save()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousex, mousey = pygame.mouse.get_pos()
                    if mousex < 425 and mousey < 470 and mousex > 395 and mousey > 440:               
                        dnum = 0
                    elif mousex < 460 and mousey < 470 and mousex > 425 and mousey > 440:
                        dnum = 1
                    elif mousex < 495 and mousey < 470 and mousex > 460 and mousey > 440:
                        dnum = 2
                    elif mousex < 530 and mousey < 470 and mousex > 495 and mousey > 440:
                        dnum = 3
                    elif mousex < 565 and mousey < 470 and mousex > 530 and mousey > 440:
                        dnum = 4

                elif keys[K_SPACE] and move_ticker == 0:
                        playerx = sprite1.rect.x + 32
                        playery = sprite1.rect.y + 32
                        col = playerx // grid_size
                        row = playery // grid_size

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

            # display the number of items a player has
            font = pygame.font.Font(None, 15)
            carrots_text = font.render(f"{carrots.value}", True, BLACK)
            screen.blit(carrots_text, (455, 455))

            font = pygame.font.Font(None, 15)
            carrotseed_text = font.render(f"{carrotseed.value}", True, BLACK)
            screen.blit(carrotseed_text, (415, 455))

            font = pygame.font.Font(None, 15)
            hoelife_text = font.render(f"{hoe_durability.value}", True, BLACK)
            screen.blit(hoelife_text, (490, 455))

            font = pygame.font.Font(None, 15)
            coin_text = font.render(f"{coinage.value}", True, BLACK)
            screen.blit(coin_text, (560, 455))

            #esc for controls prompt
            font = pygame.font.Font(None, 36)
            controls_text = font.render("ESC for controls", True, WHITE)
            screen.blit(controls_text, (10, 10))

            #display controls is esc is being pressed
            if keys[pygame.K_ESCAPE]:
                font = pygame.font.Font(None, 36)
                hoelife_text = font.render("press 7 to replenish seeds for 10 coins", True, RED)
                screen.blit(hoelife_text, (10, 85))

                font = pygame.font.Font(None, 36)
                sell_text = font.render("press 6 to sell carrots", True, RED)
                screen.blit(sell_text, (10, 60))

                font = pygame.font.Font(None, 36)
                sell_text = font.render("press 8 to repair hoe for 20 coins", True, RED)
                screen.blit(sell_text, (10, 110))

                font = pygame.font.Font(None, 36)
                sell_text = font.render("use 1-5 or TAB for item select", True, RED)
                screen.blit(sell_text, (10, 35))

                font = pygame.font.Font(None, 36)
                move_text = font.render("WASD to move", True, RED)
                screen.blit(move_text, (10, 135))

                font = pygame.font.Font(None, 36)
                hoe_text = font.render("""use hoe to place crop plot""", True, RED)
                screen.blit(hoe_text, (10, 160))

                font = pygame.font.Font(None, 36)
                seed_text = font.render("""use seeds to plant crops""", True, RED)
                screen.blit(seed_text, (10, 185))

                font = pygame.font.Font(None, 36)
                glove_text = font.render("""use glove to harvest crops""", True, RED)
                screen.blit(glove_text, (10, 210))

                font = pygame.font.Font(None, 36)
                interact_text = font.render("""press E to interact""", True, RED)
                screen.blit(interact_text, (10, 235))

                font = pygame.font.Font(None, 36)
                interact_text = font.render("""press M to mute/unmute""", True, RED)
                screen.blit(interact_text, (10, 260))


            #current buy and sell controls
            if keys[pygame.K_6]:
                coinage.addscore(carrots.value*2)
                carrots.value = 0
            if keys[pygame.K_8] and hoe_durability.value < 6 and move_ticker == 0 and carrots.value*2 + coinage.value + carrotseed.value*2 >= 30:
                hoe_durability.value = 6
                coinage.addscore(-20)
                move_ticker = 20
            if keys[pygame.K_7] and coinage.value >= 10 and move_ticker == 0: #this will always do 2x idk why just leave it
                coinage.addscore(-10)
                carrotseed.addscore(10)
                move_ticker = 20
            if keys[pygame.K_m]:
                if volume > 0 and move_ticker == 0:
                    volume = 0
                    move_ticker = 20
                elif volume == 0 and move_ticker == 0:
                    volume = 1
                    move_ticker = 20

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
