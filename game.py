from vars_and_stuff import *
from classes import *
import json





# load sprite assets
background = simplesprite('background.png')
carrotitem = simplesprite('justcarrot.png')
carrotseeds = simplesprite('carrotseedpack.png')
gardenhoe = simplesprite('gardenhoe.png')
gardenglove = simplesprite('gardenglove.png')
coin = simplesprite('coin.png')
highlight = simplesprite('highlight.png')
hotbarUI = simplesprite('carrothotbarUI.png')
#Up_Arrow = simplesprite('Up_arrow.png')
#Right_Arrow = simplesprite('Right_arrow.png')
#Down_Arrow = simplesprite('Down_arrow.png')
#Left_Arrow = simplesprite('Left_arrow.png')
inventory = simplesprite('carrotinvUI.png')

empty_crop_plot = pygame.image.load(get_asset_path("emptycropplot.png"))
carrot_seed_plot = pygame.image.load(get_asset_path("carrotseedplot.png"))
fully_grown_carrot = pygame.image.load(get_asset_path("fullygrowncarrot.png"))



class Game:
    game_data = {}

    def load(self):
        with open("saveddata.json", "r") as file:
            self.game_data = json.load(file)
    
    def save(self):
        with open("saveddata" + ".json", "w") as file:
            json.dump(self.game_data, file)

    def __init__(self):
        self.game_data['mute'] = False
        self.game_data['carrotseed'] = 15
        self.game_data['carrots'] = 0
        self.game_data['hoe_durability'] = 6
        self.game_data['coinage'] = 0
        self.game_data['placing_crop'] = True
        self.game_data['move_ticker'] = 0
        self.game_data['dnum'] = 0

        self.rows, self.cols = width // grid_size, width // grid_size
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        #dictionary to store the state and planting time of each grid square
        self.game_data['grid_state'] = {str((row, col)): (0, 0) for row in range(self.rows) for col in range(self.cols)}

        pygame.display.set_caption("Carrot Game")



    def start(self):
        # start volume
        mixer.music.set_volume(int(not self.game_data['mute']))

        openinv = True
        playerspeed = 3
        # Set up display
        screen = pygame.display.set_mode((window_width, window_height))

        mousex, mousey = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mousex, mousey,1,1)

    # Set up player sprite
        all_sprites = pygame.sprite.Group()
        sprite1 = Sprite(width / 2, height / 2, 50, 50, get_asset_path('bunny2.png'))

        background.rect.center = (width / 2, height / 2)

        """hotbarUI = pygame.transform.scale(hotbarUI, (448,120))"""
        hotbarUI.rect.center = ((width / 2), height - (hotbarUI.rect.height/2))           
        highlight.rect.center = ((width / 2), height - 1000)   

    #collision squares for hotbar
        Blanks = {}
        for x in range(0, 1):
            Blanks[x] = simplesprite('blank.png')
            Blanks[x].rect.center = ((width / 2)-172 + (68 * x), height - (hotbarUI.rect.height/2))

    #control arrows for mobile
        #Up_Arrow.rect.center = (width/2, height - (hotbarUI.rect.height/2)-140)
        #Down_Arrow.rect.center = (width/2, height - (hotbarUI.rect.height/2))
        #Left_Arrow.rect.center = ((width/2)-140, height - (hotbarUI.rect.height/2))
        #Right_Arrow.rect.center = ((width/2)+140, height - (hotbarUI.rect.height/2))
        all_sprites.add(sprite1)

        #hotbar assets
        inventory.rect.center = (width / 2, height / 2)

        # Set up clock
        clock = pygame.time.Clock()


    # Set up display
            #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
            #width, height = screen.get_size()

    #main while loop
        while True:
    #variables that need to be in the loop
            keys = pygame.key.get_pressed()
            mousex, mousey = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mousex, mousey, 1, 1)

            #prevents multiple key presses from one
            if self.game_data['move_ticker'] > 0:
                self.game_data['move_ticker'] -= 1
            if self.game_data['move_ticker'] < 0:
                self.game_data['move_ticker'] = 0


            #display background
            screen.blit(background.image, background.rect)
            #set where the sprites will be displayed
            carrotitem.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            carrotseeds.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            gardenhoe.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)
            gardenglove.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 45)
            coin.rect.center = (sprite1.rect.x + 10, sprite1.rect.y + 35)

            #hotbar and wieled
            if keys[pygame.K_1]:
                self.game_data['dnum'] = 0
            elif keys[pygame.K_2]:
                self.game_data['dnum'] = 1
            elif keys[pygame.K_3]:
                self.game_data['dnum'] = 2
            elif keys[pygame.K_4]:
                self.game_data['dnum'] = 3
            elif keys[pygame.K_5]:
                self.game_data['dnum'] = 4

            highlight.rect.center = (width / 2 - 86 + (34 * self.game_data['dnum']), height - (hotbarUI.rect.height/2))
            wielded = itemdict[self.game_data['dnum']]



            # creates the grid
            for row in range(self.rows):
                for col in range(self.cols):
                    rect = pygame.Rect(col * grid_size, row * grid_size, grid_size, grid_size)

                    # Display the appropriate crop grow stage based on the grid state
                    state, planting_time = self.game_data['grid_state'][str((row, col))]
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
                    if state == 2 and time.time() - planting_time > grow_time:
                        self.game_data['grid_state'][str((row, col))] = (3, planting_time)  # Mark as fully grown
    # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    self.save()
                    return

                #if event.type == pygame.VIDEORESIZE:
                    #  width, height = event.w, event.h
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = pygame.mouse.get_pos()
                    for x in range(len(Blanks)):
                        if Blanks[x].rect.colliderect(mouse_rect):
                            self.game_data['dnum'] = x
                            break

                if sprite1.rect.colliderect(mouse_rect) and event.type == pygame.MOUSEBUTTONDOWN or keys[K_SPACE]:
                    playerx = sprite1.rect.x + 32
                    playery = sprite1.rect.y + 32
                    col = playerx // grid_size
                    row = playery // grid_size
                
                    if self.game_data['placing_crop']:
                        # Place empty crop plot if the square is empty
                        if self.game_data['grid_state'][str((row, col))][0] == 0 or 4: #DO NOT REMOVE OR 4 STATEMNT CODE WILL STOP WORKING IDK WHY
                            if self.game_data['grid_state'][str((row, col))][0] == 0 and wielded == 'hoe' and self.game_data['hoe_durability'] > 0:
                                self.game_data['grid_state'][str((row, col))] = (1, 0)  # Mark as empty crop plot
                                self.game_data['hoe_durability'] -= 1
                            elif self.game_data['grid_state'][str((row, col))][0] == 1 and wielded == 'carrotseed' and self.game_data['carrotseed'] > 0:
                                self.game_data['grid_state'][str((row, col))] = (2, time.time())  # Change to seeded crop plot and start timer to grow carrot
                                self.game_data['carrotseed'] -= 1
                            elif self.game_data['grid_state'][str((row, col))][0] == 3 and wielded == 'gardenglove':
                                self.game_data['grid_state'][str((row, col))] = (1, 0)
                                self.game_data['carrots'] += 1
                            elif self.game_data['grid_state'][str((row, col))][0] == 2 and wielded == 'bonemeal': #and bonemeal.value > 0:
                                bonemeal = True
    # Plant a new seed if the square has an empty crop plot
                    else:
                        if self.game_data['grid_state'][str((row, col))][0] == 1:
                            self.game_data['grid_state'][str((row, col))] = (2, (time.time()))  # Marks the plot as planted in and starts the timer to grow carrot

    # displays everything that need to be on top
            all_sprites.draw(screen)
            if wielded == 'carrot':
                screen.blit(carrotitem.image, carrotitem.rect)
            if wielded == 'carrotseed':
                screen.blit(carrotseeds.image, carrotseeds.rect)
            if wielded == 'hoe':
                screen.blit(gardenhoe.image, gardenhoe.rect)
            if wielded == 'gardenglove':
                screen.blit(gardenglove.image, gardenglove.rect)
            if wielded == 'coin':
                screen.blit(coin.image, coin.rect)

    # displaying everything else
            screen.blit(hotbarUI.image, hotbarUI.rect)
            
            for x in range(len(Blanks)):
                screen.blit(Blanks[x].image, Blanks[x].rect)

            screen.blit(highlight.image, highlight.rect)

            if openinv == True:
                screen.blit(inventory.image, inventory.rect)
            
            if keys[pygame.K_e] and self.game_data['move_ticker'] == 0:
                if openinv == False:
                    openinv = True
                elif openinv == True:
                    openinv = False
                self.game_data['move_ticker'] = 20

    # display the number of items a player has
            color1 = BLACK
            color2 = BLACK
            color3 = BLACK
            color4 = BLACK
            if self.game_data['carrots'] >= 100:
                color1 = LBLUE
            if self.game_data['carrotseed'] >= 100:
                color2 = LBLUE
            if self.game_data['hoe_durability'] >= 100:
                color3 = LBLUE
            if self.game_data['coinage'] >= 100:
                color4 = LBLUE

            font = pygame.font.Font(None, 18)
            carrotseed_text = font.render(f"{self.game_data['carrotseed']}", True, color2)
            screen.blit(carrotseed_text, (width / 2 - 86 + (34 * 1) - 30, height - ((hotbarUI.rect.height/2) - 7)))
            carrots_text = font.render(f"{self.game_data['carrots']}", True, color1)
            screen.blit(carrots_text, (width / 2 - 86 + (34 * 2) - 25, height - ((hotbarUI.rect.height/2)-7 )))
            
            hoelife_text = font.render(f"{self.game_data['hoe_durability']}", True, color3)
            screen.blit(hoelife_text, (width / 2 - 86 + (34 * 3) - 25, height - ((hotbarUI.rect.height/2) - 7)))
            coin_text = font.render(f"{self.game_data['coinage']}", True, color4)            
            screen.blit(coin_text, (width / 2 - 86 + (34 * 5) - 25, height - ((hotbarUI.rect.height/2) - 7)))
            
            
    #esc for controls prompt
            controls_text = font.render("*CAUTION* Game Under Construction *CAUTION* ", True, YELLOW)
            screen.blit(controls_text, (10, 10))
            
    #update display
            pygame.display.flip()

    #current buy and sell controls
            if keys[pygame.K_6]:
                self.game_data['coinage'] += self.game_data['carrots']*2
                self.game_data['carrots'] = 0
            if keys[pygame.K_7] and self.game_data['coinage'] >= 10 and self.game_data['move_ticker'] == 0: #this will always do 2x idk why just leave it
                self.game_data['coinage'] -= 10
                self.game_data['carrotseed'] += 10
                self.game_data['move_ticker'] = 20
            if keys[pygame.K_8] and self.game_data['hoe_durability'] < 6 and self.game_data['move_ticker'] == 0 and self.game_data['carrots']*2 + self.game_data['coinage'] + self.game_data['carrotseed'] * 2 >= 30:
                self.game_data['hoe_durability'] = 6
                self.game_data['coinage'] -= 20
                self.game_data['move_ticker'] = 20

            if keys[pygame.K_m] and self.game_data['move_ticker'] == 0:
                mixer.music.set_volume(int(self.game_data['mute']))
                self.game_data['mute'] = not self.game_data['mute']
                self.game_data['move_ticker'] = 20


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
