import pygame
from pygame import *
import time
import sys
import pickle
import math


# Initialize Pygame
pygame.init()

#variables and stuff
window_width, window_height = 1000, 500
white = (255, 255, 255)
button_color = (50, 150, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 153)
BLUE = (0, 0, 255)
LBLUE = (0, 255, 255)
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
        blank = simplesprite('blank.png')
        hotbarUI = simplesprite('CarrotHotBar2.png')
        hotbarUI.rect.center = (width / 2, height - (hotbarUI.rect.height/2))
        inventory = simplesprite('carrotinvUI.png')
        inventory.rect.center = (width / 2, height / 2)
        highlight = simplesprite('highlight.png')
        highlight.rect.center = (width / 2 - 86, height - (hotbarUI.rect.height/2))

        #note to self make a py group of simple sprites

        # Set up grid
        grid_size = 50
        rows, cols = width // grid_size, width // grid_size
        grid = [[0] * cols for _ in range(rows)]

        # Define a dictionary to store the state and planting time of each grid square
        grid_state = {(row, col): (0, 0) for row in range(rows) for col in range(cols)}


        hotbardict = {
        "item1":carrotseeds.image,
        "item2":carrotitem.image,
        "item3":gardenhoe.image,
        "item4":gardenglove.image,
        "item5":coin.image
        }

        
        invodict = {
        "invslot1":blank.image,
        "invslot2":blank.image,
        "invslot3":blank.image,
        "invslot4":blank.image,
        "invslot5":blank.image,
        "invslot6":blank.image,
        "invslot7":blank.image,
        "invslot8":blank.image,
        "invslot9":blank.image,
        "invslot10":blank.image,
        "invslot11":blank.image,
        "invslot12":blank.image,
        "invslot13":blank.image,
        "invslot14":blank.image,
        "invslot15":blank.image,
        "invslot16":blank.image,
        "invslot17":blank.image,
        "invslot18":blank.image,
        "invslot19":blank.image,
        "invslot20":blank.image,
        "invslot21":blank.image,
        "invslot22":blank.image,
        "invslot23":blank.image,
        "invslot24":blank.image,
        "invslot25":blank.image
        }
        
        itemselected = hotbardict["item1"]
        itemselectedinv = invodict["invslot1"]
        openinv = False
        invonum = 0
        itemnum = 0


        def swap():
            global invonum, itemnum, itemselected, itemselectedinv
            if itemselected == hotbardict["item1"]:
                itemselectedinv = hotbardict["item1"]
                itemnum = 1
            elif itemselected == hotbardict["item2"]:
                itemselectedinv = hotbardict["item2"]
                itemnum = 2
            elif itemselected == hotbardict["item3"]:
                itemselectedinv = hotbardict["item3"]
                itemnum = 3
            elif itemselected == hotbardict["item4"]:
                itemselectedinv = hotbardict["item4"]
                itemnum = 4
            elif itemselected == hotbardict["item5"]:
                itemselectedinv = hotbardict["item5"]
                itemnum = 5
            else:
                print("Invalid")
            itemselected = invodict["invslot"+ str(invonum)]
            invodict["invslot"+ str(invonum)], hotbardict["item"+ str(itemnum)] = itemselectedinv, itemselected


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
                    print(mousex, mousey)
                    if mousex > 400 and mousey > 454 and mousex < 430 and mousey < 485 and openinv == False:               
                        dnum = 0
                    elif mousex > 433 and mousey > 454 and mousex < 465 and mousey < 485 and openinv == False:
                        dnum = 1
                    elif mousex > 468 and mousey > 454 and mousex < 500 and mousey < 485 and openinv == False:
                        dnum = 2
                    elif mousex > 501 and mousey > 454 and mousex < 532 and mousey < 485 and openinv == False:
                        dnum = 3
                    elif mousex > 535 and mousey > 454 and mousex < 566 and mousey < 485 and openinv == False:
                        dnum = 4
            if openinv == True and move_ticker == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousex, mousey = pygame.mouse.get_pos()
                    if mousex > 376 and mousex < 423 and mousey > 127 and mousey < 172:
                        invonum = 1
                        swap()
                        move_ticker = 20

                    elif mousex > 427 and mousex < 472 and mousey > 127 and mousey < 172:
                        invonum = 2
                        swap()
                        move_ticker = 20

                    elif mousex > 478 and mousex < 525 and mousey > 127 and mousey < 172:
                        invonum = 3
                        swap()
                        move_ticker = 20

                    elif mousex > 529 and mousex < 576 and mousey > 127 and mousey < 172:
                        invonum = 4
                        swap()
                        move_ticker = 20

                    elif mousex > 580 and mousex < 624 and mousey > 127 and mousey < 172:
                        invonum = 5
                        swap()
                        move_ticker = 20

                    elif mousex > 376 and mousex < 423 and mousey > 176 and mousey < 221:
                        invonum = 6
                        swap()
                        move_ticker = 20

                    elif mousex > 427 and mousex < 472 and mousey > 176 and mousey < 221:
                        invonum = 7
                        swap()
                        move_ticker = 20

                    elif mousex > 478 and mousex < 525 and mousey > 176 and mousey < 221:
                        invonum = 8
                        swap()
                        move_ticker = 20

                    elif mousex > 529 and mousex < 576 and mousey > 176 and mousey < 221:
                        invonum = 9
                        swap()
                        move_ticker = 20

                    elif mousex > 580 and mousex < 624 and mousey > 176 and mousey < 221:
                        invonum = 10
                        swap()
                        move_ticker = 20

                    elif mousex > 376 and mousex < 423 and mousey > 226 and mousey < 272:
                        invonum = 11
                        swap()
                        move_ticker = 20

                    elif mousex > 427 and mousex < 472 and mousey > 226 and mousey < 272:
                        invonum = 12
                        swap()
                        move_ticker = 20

                    elif mousex > 478 and mousex < 525 and mousey > 226 and mousey < 272:
                        invonum = 13
                        swap()
                        move_ticker = 20

                    elif mousex > 529 and mousex < 576 and mousey > 226 and mousey < 272:
                        invonum = 14
                        swap()
                        move_ticker = 20

                    elif mousex > 580 and mousex < 624 and mousey > 226 and mousey < 272:
                        invonum = 15
                        swap()
                        move_ticker = 20

                    elif mousex > 376 and mousex < 423 and mousey > 280 and mousey < 322:
                        invonum = 16
                        swap()
                        move_ticker = 20

                    elif mousex > 427 and mousex < 472 and mousey > 280 and mousey < 322:
                        invonum = 17
                        swap()
                        move_ticker = 20

                    elif mousex > 478 and mousex < 525 and mousey > 280 and mousey < 322:
                        invonum = 18
                        swap()
                        move_ticker = 20

                    elif mousex > 529 and mousex < 576 and mousey > 280 and mousey < 322:
                        invonum = 19
                        swap()
                        move_ticker = 20

                    elif mousex > 580 and mousex < 624 and mousey > 280 and mousey < 322:
                        invonum = 20
                        swap()
                        move_ticker = 20

                    elif mousex > 376 and mousex < 423 and mousey > 330 and mousey < 374:
                        invonum = 21
                        swap()
                        move_ticker = 20


                    elif mousex > 427 and mousex < 472 and mousey > 330 and mousey < 374:
                        invonum = 22
                        swap()
                        move_ticker = 20

                    elif mousex > 478 and mousex < 525 and mousey > 330 and mousey < 374:
                        invonum = 23
                        swap()
                        move_ticker = 20

                    elif mousex > 529 and mousex < 576 and mousey > 330 and mousey < 374:
                        invonum = 24
                        swap()
                        move_ticker = 20

                    elif mousex > 580 and mousex < 624 and mousey > 330 and mousey < 374:
                        invonum = 25
                        swap()
                        move_ticker = 20

                    if mousex > 400 and mousey > 454 and mousex < 430 and mousey < 485:
                        itemselected = hotbardict["item1"]
                        move_ticker = 20
                    elif mousex > 433 and mousey > 454 and mousex < 465 and mousey < 485:
                        itemselected = hotbardict["item2"]
                        move_ticker = 20
                    elif mousex > 468 and mousey > 454 and mousex < 500 and mousey < 485:
                        itemselected = hotbardict["item3"]
                        move_ticker = 20
                    elif mousex > 501 and mousey > 454 and mousex < 532 and mousey < 485:
                        itemselected = hotbardict["item4"]
                        move_ticker = 20
                    elif mousex > 535 and mousey > 454 and mousex < 566 and mousey < 485:
                        itemselected = hotbardict["item5"]
                        print(str(itemselected))
                        move_ticker = 20
                    else:
                        print("idk anymore")

            itemdict[0] = hotbardict["item1"]
            itemdict[1] = hotbardict["item2"]
            itemdict[2] = hotbardict["item3"]
            itemdict[3] = hotbardict["item4"]
            itemdict[4] = hotbardict["item5"]
            itemhave = itemdict[dnum]

            if keys[K_SPACE]:
                    playerx = sprite1.rect.x + 32
                    playery = sprite1.rect.y + 32
                    col = playerx // grid_size
                    row = playery // grid_size
                    if grid_state[(row, col)][0] == 0 or 4: #DO NOT REMOVE OR 4 STATEMNT CODE WILL STOP WORKING IDK WHY
                        if grid_state[(row, col)][0] == 0 and itemhave == gardenhoe.image and hoe_durability.value > 0:
                            grid_state[(row, col)] = (1, 0)  # Mark as empty crop plot
                            hoe_durability.addscore(-1)
                        elif grid_state[(row, col)][0] == 1 and itemhave == carrotseeds.image and carrotseed.value > 0:
                            grid_state[(row, col)] = (2, time.time())  # Change to seeded crop plot and start timer to grow carrot
                            carrotseed.addscore(-1)
                        elif grid_state[(row, col)][0] == 3 and itemhave == gardenglove.image:
                            grid_state[(row, col)] = (1, 0)
                            carrots.addscore(1)
                    else:
                        # Plant a new seed if the square has an empty crop plot
                        if grid_state[(row, col)][0] == 1:
                            grid_state[(row, col)] = (2, time.time())  # Mark as seed planted and start timer to grow carrot

            #display hotbar
            screen.blit(hotbarUI.image, hotbarUI.rect)
            screen.blit(hotbardict["item1"], (400, 454))
            screen.blit(hotbardict["item2"], (433, 454))
            screen.blit(hotbardict["item3"], (468, 454))
            screen.blit(hotbardict["item4"], (500, 454))
            screen.blit(hotbardict["item5"], (534, 454))
            screen.blit(highlight.image, highlight.rect)

            # display the player and the item that is in his hand
            all_sprites.draw(screen)
            if itemhave == carrotitem.image:
                screen.blit(carrotitem.image, carrotitem.rect)
            if itemhave == carrotseeds.image:
                screen.blit(carrotseeds.image, carrotseeds.rect)
            if itemhave == gardenhoe.image:
                screen.blit(gardenhoe.image, gardenhoe.rect)
            if itemhave == gardenglove.image:
                screen.blit(gardenglove.image, gardenglove.rect)
            if itemhave == coin.image:
                screen.blit(coin.image, coin.rect)
            color1 = BLACK
            color2 = BLACK
            color3 = BLACK
            color4 = BLACK
            if carrots.value >= 100:
                color1 = LBLUE
            if carrotseed.value >= 100:
                color2 = LBLUE
            if hoe_durability.value >= 100:
                color3 = LBLUE
            if coinage.value >= 100:
                color4 = LBLUE

            # display the number of items a player has
            font = pygame.font.Font(None, 15)
            carrots_text = font.render(f"{carrots.value}", True, color1)
            screen.blit(carrots_text, (455, 455))

            font = pygame.font.Font(None, 15)
            carrotseed_text = font.render(f"{carrotseed.value}", True, color2)
            screen.blit(carrotseed_text, (415, 455))

            font = pygame.font.Font(None, 15)
            hoelife_text = font.render(f"{hoe_durability.value}", True, color3)
            screen.blit(hoelife_text, (490, 455))

            font = pygame.font.Font(None, 15)
            coin_text = font.render(f"{coinage.value}", True, color4)
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
                interact_text = font.render("""press SPACE to interact""", True, RED)
                screen.blit(interact_text, (10, 235))

                font = pygame.font.Font(None, 36)
                interact_text = font.render("""press M to mute/unmute""", True, RED)
                screen.blit(interact_text, (10, 260))


            #current buy and sell controls
            if keys[pygame.K_6]:
                coinage.addscore(carrots.value*2)
                carrots.value = 0
            if keys[pygame.K_8] and hoe_durability.value < 6 and move_ticker == 0 and carrots.value*2 + coinage.value + carrotseed.value*2 >= 30:
                if coinage.value >= 20:
                    hoe_durability.value = 6
                    coinage.addscore(-20)
                    move_ticker = 20
            if keys[pygame.K_7] and coinage.value >= 10 and move_ticker == 0:
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

            if keys[pygame.K_q] and move_ticker == 0:
                if openinv == False:
                    openinv = True
                elif openinv == True:
                    openinv = False
                move_ticker = 20
            if openinv == True:
                screen.blit(inventory.image, inventory.rect)
                screen.blit(invodict["invslot1"], (384, 140))
                screen.blit(invodict["invslot2"], (434, 140))
                screen.blit(invodict["invslot3"], (486, 140))
                screen.blit(invodict["invslot4"], (536, 140))
                screen.blit(invodict["invslot5"], (588, 140))
                screen.blit(invodict["invslot6"], (384, 187))
                screen.blit(invodict["invslot7"], (434, 187))
                screen.blit(invodict["invslot8"], (486, 187))
                screen.blit(invodict["invslot9"], (536, 187))
                screen.blit(invodict["invslot10"], (588, 187))
                screen.blit(invodict["invslot11"], (384, 240))
                screen.blit(invodict["invslot12"], (434, 240))
                screen.blit(invodict["invslot13"], (486, 240))
                screen.blit(invodict["invslot14"], (536, 240))
                screen.blit(invodict["invslot15"], (588, 240))
                screen.blit(invodict["invslot16"], (384, 287))
                screen.blit(invodict["invslot17"], (434, 287))
                screen.blit(invodict["invslot18"], (486, 287))
                screen.blit(invodict["invslot19"], (536, 287))
                screen.blit(invodict["invslot20"], (588, 287))
                screen.blit(invodict["invslot21"], (384, 338))
                screen.blit(invodict["invslot22"], (434, 338))
                screen.blit(invodict["invslot23"], (486, 338))
                screen.blit(invodict["invslot24"], (536, 338))
                screen.blit(invodict["invslot25"], (588, 338))

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
