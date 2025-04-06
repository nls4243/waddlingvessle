import pygame
from pygame import *
import time
import sys
import pickle

# Initialize Pygame
pygame.init()

# Create the starting window
window_width, window_height = (1280 ,720) #start_window.get_size()
start_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Main Window")#pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)

#variables
white = (255, 255, 255)
button_color = (50, 150, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LBLUE = (0, 255, 255)
running = True
open_game = False
in_pain = True
load_saved = False

#sprites
main_menu = pygame.sprite.Sprite()
main_menu.image = pygame.image.load('main_screen.png')
main_menu.rect = main_menu.image.get_rect()
main_menu.rect.center = (window_width / 2, window_height / 2)
new_button = pygame.sprite.Sprite()
new_button.image = pygame.image.load('newgame_button.png')
new_button.rect = new_button.image.get_rect()
new_button.rect.center = ((window_width / 2)+16, (window_height / 2)+70)
exit_button = pygame.sprite.Sprite()
exit_button.image = pygame.image.load('exit_button.png')
exit_button.rect = exit_button.image.get_rect()
exit_button.rect.center = ((window_width / 2)+16, (window_height / 2) + 200)
load_button = pygame.sprite.Sprite()
load_button.image = pygame.image.load('load_button.png')
load_button.rect = load_button.image.get_rect()
load_button.rect.center = ((window_width / 2)+16, (window_height / 2) - 52)
load_saved = False

#starting window loop
while running:

    mousex, mousey = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mousex, mousey, 1, 1)
    start_window.blit(main_menu.image, main_menu.rect)
    start_window.blit(new_button.image, new_button.rect)
    start_window.blit(load_button.image, load_button.rect)
    start_window.blit(exit_button.image, exit_button.rect)
    
    for event in pygame.event.get():
        #if event.type == pygame.VIDEORESIZE:
             #width, height = event.w, event.h
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
    pygame.display.set_caption("CARROT GAME")
    # Set up display
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Main Window") #pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
    width, height = (1280,720) #(1920,1080) screen.get_size()

#class for counting values 
    mousex, mousey = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mousex, mousey,1,1)       
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
            self.rect.center = (mousex + 15, mousey + 15)
                            
# Set up player sprite
    all_sprites = pygame.sprite.Group()
    sprite1 = Sprite(width / 2, height / 2, 50, 50, 'bunny2.png')  

# Load images
    empty_crop_plot = pygame.image.load("emptycropplot.png")
    carrot_seed_plot = pygame.image.load("carrotseedplot.png")
    fully_grown_carrot = pygame.image.load("fullygrowncarrot.png")
    background = simplesprite('background.png')
    background.rect.center = (width / 2, height / 2)
    carrotitem = simplesprite('justcarrot.png')
    carrotseeds = simplesprite('carrotseedpack.png')
    gardenhoe = simplesprite('gardenhoe.png')
    gardenglove = simplesprite('gardenglove.png')
    coin = simplesprite('coin.png')
    
    hotbarUI = simplesprite('carrothotbarUI.png')
    """hotbarUI = pygame.transform.scale(hotbarUI, (448,120))"""
    hotbarUI.rect.center = ((width / 2), height - (hotbarUI.rect.height/2))           
    highlight = simplesprite('highlight.png')
    highlight.rect.center = ((width / 2), height - 1000)   
    
#collision squares for hotbar
    Blank1 = simplesprite('blank.png')
    Blank1.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))
    Blank2 = simplesprite('blank.png')
    Blank2.rect.center = ((width / 2)-172+68, height - (hotbarUI.rect.height/2))
    Blank3 = simplesprite('blank.png')
    Blank3.rect.center = ((width / 2)-172+(68*2), height - (hotbarUI.rect.height/2))
    Blank4 = simplesprite('blank.png')
    Blank4.rect.center = ((width / 2)-172+(68*3), height - (hotbarUI.rect.height/2))
    Blank5 = simplesprite('blank.png')
    Blank5.rect.center = ((width / 2)-172+(68*4), height - (hotbarUI.rect.height/2))
    
#control arrows for mobile                
    Up_Arrow = simplesprite('Up_arrow.png')
    Up_Arrow.rect.center = (width/2, height - (hotbarUI.rect.height/2)-140)       
    Down_Arrow = simplesprite('Down_arrow.png')
    Down_Arrow.rect.center = (width/2, height - (hotbarUI.rect.height/2))      
    Left_Arrow = simplesprite('Left_arrow.png')
    Left_Arrow.rect.center = ((width/2)-140, height - (hotbarUI.rect.height/2))        
    Right_Arrow = simplesprite('Right_arrow.png')
    Right_Arrow.rect.center = ((width/2)+140, height - (hotbarUI.rect.height/2)) 
    all_sprites.add(sprite1)

#hotbar assets
    inventory = simplesprite('carrotinvUI.png')
    inventory.rect.center = (width / 2, height / 2)

    A8223 = True
    if A8223:
        BlankHB1 = simplesprite('blank.png')
        BlankHB1.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB2 = simplesprite('blank.png')
        BlankHB2.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB3 = simplesprite('blank.png')
        BlankHB3.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB4 = simplesprite('blank.png')
        BlankHB4.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB5 = simplesprite('blank.png')
        BlankHB5.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB6 = simplesprite('blank.png')
        BlankHB6.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB7 = simplesprite('blank.png')
        BlankHB7.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB8 = simplesprite('blank.png')
        BlankHB8.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB9 = simplesprite('blank.png')
        BlankHB9.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB10 = simplesprite('blank.png')
        BlankHB10.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB11 = simplesprite('blank.png')
        BlankHB11.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB12 = simplesprite('blank.png')
        BlankHB12.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB13 = simplesprite('blank.png')
        BlankHB13.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB14 = simplesprite('blank.png')
        BlankHB14.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB15 = simplesprite('blank.png')
        BlankHB15.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB16 = simplesprite('blank.png')
        BlankHB16.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB17 = simplesprite('blank.png')
        BlankHB17.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB18 = simplesprite('blank.png')
        BlankHB18.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB19 = simplesprite('blank.png')
        BlankHB19.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB20 = simplesprite('blank.png')
        BlankHB20.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB21 = simplesprite('blank.png')
        BlankHB21.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB22 = simplesprite('blank.png')
        BlankHB22.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB23 = simplesprite('blank.png')
        BlankHB23.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB24 = simplesprite('blank.png')
        BlankHB24.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

        BlankHB25 = simplesprite('blank.png')
        BlankHB25.rect.center = ((width / 2)-172, height - (hotbarUI.rect.height/2))

# Set up grid
    grid_size = 100
    rows, cols = width // grid_size, width // grid_size
    grid = [[0] * cols for _ in range(rows)]

#dictionary to store the state and planting time of each grid square
    grid_state = {(row, col): (0, 0) for row in range(rows) for col in range(cols)}
    grid_check = False

#User Data variables
    #player invetory variables
    itemdict = ['carrotseed', 'carrot', 'hoe', 'gardenglove', 'coin']
    carrotseed = Counter()
    carrots = Counter()
    hoe_durability = Counter()
    coinage = Counter()
    #other variables
    itemdictc = len(itemdict) - 1
    selected = None
    placing_crop = True
    running = True
    RUNNING = True
    openinv = True
    move_ticker = 0
    playerspeed = 3
    dnum = 0
    hoe_durability.value = 6
    carrotseed.addscore(15)

#ADD THESE TO SAVED DATA LATER
#growing variables
    is_bonemealed = False
    grow_time = 10

#END OF THINGS NEEDING TO BE ADDED TO THE SAVED DATA
# Set up clock
    clock = pygame.time.Clock()

#music
    volume = 1
    mixer.music.load('carrots.wav')
    mixer.music.play(-1)

#saving variables
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
            
#load saved variables
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

# Set up display
        #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
        #width, height = screen.get_size()

#main while loop
        while running:

#variables that need to be in the loop
            mixer.music.set_volume(volume)
            keys = pygame.key.get_pressed()
            mousex, mousey = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mousex, mousey, 1, 1)
            #prevents multiple key presses from one
            if move_ticker > 0:
                move_ticker -= 1
            if move_ticker < 0:
                move_ticker = 0
            #item the player is currently holding
            itemhave = itemdict[dnum]
#display background
            screen.blit(background.image, background.rect)
#set where the sprites will be displayed
            carrotitem.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            carrotseeds.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            gardenhoe.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            gardenglove.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 45)
            coin.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            
#hotbar keys
            if keys[pygame.K_1]:
                dnum = 0
            
            if keys[pygame.K_2]:
                dnum = 1
            
            if keys[pygame.K_3]:
                dnum = 2
            
            if keys[pygame.K_4]:
                dnum = 3
            
            if keys[pygame.K_5]:
                dnum = 4

#highlights selected hotbar slot
            if dnum == 0:
                highlight.rect.center = (width / 2 - 172, height - (hotbarUI.rect.height/2))
            if dnum == 1:
                highlight.rect.center = (width / 2 - 172 + 68, height - (hotbarUI.rect.height/2))
            if dnum == 2:
                highlight.rect.center = (width / 2 - 172 + 68*2, height - (hotbarUI.rect.height/2))
            if dnum == 3:
                highlight.rect.center = (width / 2 - 172 + 68*3, height - (hotbarUI.rect.height/2))
            if dnum == 4:
                highlight.rect.center = (width / 2 - 172 +68*4, height - (hotbarUI.rect.height/2))



# creates the grid
            for row in range(rows):
                for col in range(cols):
                    rect = pygame.Rect(col * grid_size, row * grid_size, grid_size, grid_size)

# Display the appropriate crop grow stage based on the grid state
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

 # Check if the seed has been planted and update to fully grown after X seconds
                    if state == 2 and not is_bonemealed and time.time() - planting_time > grow_time:
                        grid_state[(row, col)] = (3, planting_time)  # Mark as fully grown
                    elif state == 2 and is_bonemealed and time.time() - planting_time > (grow_time/2):
                        grid_state[(row, col)] = (3, planting_time)  # Mark as fully grown
# event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    running = False
                    save()
                    pygame.quit()
                    sys.exit()
                #if event.type == pygame.VIDEORESIZE:
                    #  width, height = event.w, event.h
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = pygame.mouse.get_pos()
                    if Blank1.rect.colliderect(mouse_rect):
                        dnum = 0
                        
                    elif Blank2.rect.colliderect(mouse_rect):
                        dnum = 1
                    
                    elif Blank3.rect.colliderect(mouse_rect):
                        dnum = 2
                    
                    elif Blank4.rect.colliderect(mouse_rect):
                        dnum = 3
                
                    elif Blank5.rect.colliderect(mouse_rect):
                        dnum = 4

                if sprite1.rect.colliderect(mouse_rect) and event.type == pygame.MOUSEBUTTONDOWN or keys[K_SPACE]:
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
                            elif grid_state[(row, col)][0] == 2 and itemhave == 'bonemeal': #and bonemeal.value > 0:
                                bonemeal = True
# Plant a new seed if the square has an empty crop plot                               
                    else:
                        if grid_state[(row, col)][0] == 1:
                            grid_state[(row, col)] = (2, (time.time()))  # Marks the plot as planted in and starts the timer to grow carrot

#displays everything that need to be on top
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
            """if itemhave == 'bonemeal':
                screen.blit(bonemeal.image, bonemeal.rect)"""
#displaying everything else   
            screen.blit(hotbarUI.image, hotbarUI.rect)
            screen.blit(Blank1.image, Blank1.rect)
            screen.blit(Blank2.image, Blank2.rect)
            screen.blit(Blank3.image, Blank3.rect)
            screen.blit(Blank4.image, Blank4.rect)
            screen.blit(Blank5.image, Blank5.rect)
            screen.blit(highlight.image, highlight.rect)

            if openinv == True:
                screen.blit(inventory.image, inventory.rect)
            
            if keys[pygame.K_e] and move_ticker == 0:
                if openinv == False:
                    openinv = True
                elif openinv == True:
                    openinv = False
                move_ticker = 20

# display the number of items a player has     
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

            font = pygame.font.Font(None, 45)
            carrotseed_text = font.render(f"{carrotseed.value}", True, color2)
            screen.blit(carrotseed_text, (width/2-172, height - (hotbarUI.rect.height / 2)))
            carrots_text = font.render(f"{carrots.value}", True, color1)
            screen.blit(carrots_text, (width/2-172+68, height - (hotbarUI.rect.height / 2)))
            
            hoelife_text = font.render(f"{hoe_durability.value}", True, color3)
            screen.blit(hoelife_text, (width/2-172+68*2, height - (hotbarUI.rect.height / 2)))
            coin_text = font.render(f"{coinage.value}", True, color4)            
            screen.blit(coin_text, (width/2-172+68*4, height - (hotbarUI.rect.height / 2)))
            
            
#esc for controls prompt            
            controls_text = font.render("*CAUTION* Game Under Construction *CAUTION* ", True, YELLOW)
            screen.blit(controls_text, (10, 10))
            
#update display
            pygame.display.flip()

#current buy and sell controls
            if keys[pygame.K_6]:
                coinage.addscore(carrots.value*2)
                carrots.value = 0
            if keys[pygame.K_7] and coinage.value >= 10 and move_ticker == 0: #this will always do 2x idk why just leave it
                coinage.addscore(-10)
                carrotseed.addscore(10)
                move_ticker = 20
            if keys[pygame.K_8] and hoe_durability.value < 6 and move_ticker == 0 and carrots.value*2 + coinage.value + carrotseed.value*2 >= 30:
                hoe_durability.value = 6
                coinage.addscore(-20)
                move_ticker = 20
            if keys[pygame.K_m] and move_ticker == 0:
                if volume > 0:
                    volume = 0

                elif volume == 0:
                    volume = 1
                   
                move_ticker = 20

            """if grid_check == True:
                print(grid_state)
                grid_check = False

            if keys[pygame.K_p]:
                grid_check = True"""

# Move the player 
                
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
