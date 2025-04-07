from vars_and_stuff import *
from classes import *
import json





# load sprite assets
background = simplesprite('background.png', (width / 2, height / 2))
highlight = simplesprite('highlight.png', ((width / 2), height - 1000))
hotbarUI = simplesprite('carrothotbarUI.png', (width / 2, height - 30))
inventory = simplesprite('carrotinvUI.png', (width / 2, height / 2))

player = None

empty_crop_plot = pygame.image.load(get_asset_path("emptycropplot.png"))
carrot_seed_plot = pygame.image.load(get_asset_path("carrotseedplot.png"))
fully_grown_carrot = pygame.image.load(get_asset_path("fullygrowncarrot.png"))


carrotitem = simplesprite('justcarrot.png')
carrotseeds = simplesprite('carrotseedpack.png')
gardenhoe = simplesprite('gardenhoe.png')
gardenglove = simplesprite('gardenglove.png')
coin = simplesprite('coin.png')
itemdict = [
	{'item' : 'carrotseed', 'sprite' : carrotseeds},
	{'item' : 'carrot', 'sprite' : carrotitem},
	{'item' : 'hoe', 'sprite' : gardenhoe},
	{'item' : 'gardenglove', 'sprite' : gardenglove},
	{'item' : 'coin', 'sprite' : coin}
]


class Game:
	game_data = {}

	def _load(self):
		data_in = {}
		with open("saveddata.json", "r") as file:
			data_in = json.load(file)
		for key, value in data_in.items():
			self.game_data[key] = value

	def _save(self):
		# Save data only used at start/save times
		self.game_data['player_pos'] = player.rect.center

		with open("saveddata" + ".json", "w") as file:
			json.dump(self.game_data, file)

	def __init__(self, load = False):
		# initial setup
		pygame.display.set_caption("Carrot Game")

		self.game_data['mute'] = False
		self.game_data['carrotseed'] = 15
		self.game_data['carrots'] = 0
		self.game_data['hoe_durability'] = 6
		self.game_data['coinage'] = 0
		self.game_data['placing_crop'] = True
		self.game_data['move_ticker'] = 0
		self.game_data['dnum'] = 0
		self.game_data['grid_size'] = 50
		self.game_data['openinv'] = False

		self.rows, self.cols = width // self.game_data['grid_size'], width // self.game_data['grid_size']
		self.grid = [[0] * self.cols for _ in range(self.rows)]
		# Dictionary to store the state and planting time of each grid square
		self.game_data['grid_state'] = {str((row, col)): (0, 0) for row in range(self.rows) for col in range(self.cols)}

		self.Blanks = {}
		for x in range(0, 1):
			self.Blanks[x] = simplesprite('blank.png')
			self.Blanks[x].rect.center = ((width / 2)-172 + (68 * x), height - (hotbarUI.rect.height/2))

		# Only used at start/save time data
		self.game_data['player_pos'] = (width / 2, height / 2)


		# Load
		if load:
			self._load()


		global player
		player = simplesprite('bunny1.png', self.game_data['player_pos'])


		# ambiance
		mixer.music.set_volume(int(not self.game_data['mute']))

		# Start
		self._start()



	def _start(self):
		clock = pygame.time.Clock()

		while True:
			#variables that need to be in the loop
			keys = pygame.key.get_pressed()
			mousex, mousey = pygame.mouse.get_pos()
			mouse_rect = pygame.Rect(mousex, mousey, 1, 1)

			#prevents multiple key presses from one
			if self.game_data['move_ticker'] >= 1:
				self.game_data['move_ticker'] -= 1
			elif self.game_data['move_ticker'] != 0:
				self.game_data['move_ticker'] = 0


			#display background
			screen.blit(background.image, background.rect)
			#set where the sprites will be displayed

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
			wielded['sprite'].rect.center = (player.rect.x + 10, player.rect.y + 35)



			# creates the grid
			for row in range(self.rows):
				for col in range(self.cols):
					rect = pygame.Rect(col * self.game_data['grid_size'], row * self.game_data['grid_size'], self.game_data['grid_size'], self.game_data['grid_size'])

					# Display the appropriate crop grow stage based on the grid state
					state, planting_time = self.game_data['grid_state'][str((row, col))]
					if state == 1:
						screen.blit(empty_crop_plot, rect.topleft)
					elif state == 2:
						screen.blit(carrot_seed_plot, rect.topleft)
					elif state == 3:
						screen.blit(fully_grown_carrot, rect.topleft)

					# Check if the seed has been planted and update to fully grown after X seconds
					if state == 2 and time.time() - planting_time > grow_time:
						self.game_data['grid_state'][str((row, col))] = (3, planting_time)  # Mark as fully grown
			# event handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
					self._save()
					return

				#if event.type == pygame.VIDEORESIZE:
				#  width, height = event.w, event.h
				if event.type == pygame.MOUSEBUTTONDOWN:
					mousex, mousey = pygame.mouse.get_pos()
					for x in range(len(self.Blanks)):
						if self.Blanks[x].rect.colliderect(mouse_rect):
							self.game_data['dnum'] = x
							break

				if player.rect.colliderect(mouse_rect) and event.type == pygame.MOUSEBUTTONDOWN or keys[K_SPACE]:
					col, row = player.rect.center
					col //= self.game_data['grid_size']
					row //= self.game_data['grid_size']

					if self.game_data['placing_crop']:
						# Place empty crop plot if the square is empty
						if self.game_data['grid_state'][str((row, col))][0] == 0 and wielded['item'] == 'hoe' and self.game_data['hoe_durability'] > 0:
							self.game_data['grid_state'][str((row, col))] = (1, 0)  # Mark as empty crop plot
							self.game_data['hoe_durability'] -= 1
						elif self.game_data['grid_state'][str((row, col))][0] == 1 and wielded['item'] == 'carrotseed' and self.game_data['carrotseed'] > 0:
							self.game_data['grid_state'][str((row, col))] = (2, time.time())  # Change to seeded crop plot and start timer to grow carrot
							self.game_data['carrotseed'] -= 1
						elif self.game_data['grid_state'][str((row, col))][0] == 3 and wielded['item'] == 'gardenglove':
							self.game_data['grid_state'][str((row, col))] = (1, 0)
							self.game_data['carrots'] += 1
						#elif self.game_data['grid_state'][str((row, col))][0] == 2 and wielded == 'bonemeal': #and bonemeal.value > 0:
						#    bonemeal = True
					# Plant a new seed if the square has an empty crop plot
					else:
						if self.game_data['grid_state'][str((row, col))][0] == 1:
							self.game_data['grid_state'][str((row, col))] = (2, (time.time()))  # Marks the plot as planted in and starts the timer to grow carrot

			# displays everything that need to be on top
			screen.blit(player.image, player.rect)
			screen.blit(wielded['sprite'].image, wielded['sprite'].rect)

			# displaying everything else
			screen.blit(hotbarUI.image, hotbarUI.rect)

			for x in range(len(self.Blanks)):
				screen.blit(self.Blanks[x].image, self.Blanks[x].rect)

			screen.blit(highlight.image, highlight.rect)


			if keys[pygame.K_e] and self.game_data['move_ticker'] == 0:
				self.game_data['openinv'] = not self.game_data['openinv']
				self.game_data['move_ticker'] = key_cooldown

			if self.game_data['openinv']:
				screen.blit(inventory.image, inventory.rect)


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

			# Update display
			pygame.display.flip()





			# Post display operations

			#current buy and sell controls
			if self.game_data['move_ticker'] == 0:
				if keys[pygame.K_6]:
					self.game_data['coinage'] += self.game_data['carrots']*2
					self.game_data['carrots'] = 0
					self.game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_7] and self.game_data['coinage'] >= 10:
					self.game_data['coinage'] -= 10
					self.game_data['carrotseed'] += 10
					self.game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_8] and self.game_data['coinage'] >= 20 and self.game_data['carrotseed']*2 + self.game_data['carrots']*2 + self.game_data['coinage'] >= 30:
					self.game_data['hoe_durability'] += 6
					self.game_data['coinage'] -= 20
					self.game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_m]:
					mixer.music.set_volume(int(self.game_data['mute']))
					self.game_data['mute'] = not self.game_data['mute']
					self.game_data['move_ticker'] = key_cooldown

				
			# Move the player

			if keys[pygame.K_w]:
				player.rect.y -= playerspeed
			elif keys[pygame.K_s]:
				player.rect.y += playerspeed
			# Cap the player's position
			player.rect.y = max(0, min(player.rect.y, height - player.rect.height))

			if keys[pygame.K_a]:
				player.rect.x -= playerspeed
			elif keys[pygame.K_d]:
				player.rect.x += playerspeed
			# Cap the player's position
			player.rect.x = max(0, min(player.rect.x, width - player.rect.width))

			clock.tick(60)
