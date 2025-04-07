from vars_and_stuff import *
from classes import *
import json





# load sprite assets
background = simplesprite('background.png', (width / 2, height / 2))
highlight = simplesprite('highlight.png', ((width / 2), height - 1000))
hotbarUI = simplesprite('CarrotHotBar2.png', (width / 2, height - 30))
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
noitem = simplesprite('blank.png')

itemdict = {
	'carrotseed' : {'item' : 'carrotseed', 'sprite' : carrotseeds},
	'carrot' : {'item' : 'carrot', 'sprite' : carrotitem},
	'hoe' : {'item' : 'hoe', 'sprite' : gardenhoe},
	'gardenglove' : {'item' : 'gardenglove', 'sprite' : gardenglove},
	'coin' : {'item' : 'coin', 'sprite' : coin},
	'' : {'item' : '', 'sprite' : noitem}
}


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
		self.game_data['inventory'] = self.inventory.get_metadata()

		with open("saveddata" + ".json", "w") as file:
			json.dump(self.game_data, file)

	def __init__(self, load = False):
		# initial setup
		pygame.display.set_caption("Carrot Game")

		self.game_data['mute'] = False
		self.game_data['placing_crop'] = True
		self.game_data['move_ticker'] = 0
		self.game_data['dnum'] = 0
		self.game_data['grid_size'] = 50
		self.game_data['openinv'] = False

		self.inventory = Inventory()
		self.inventory.set_item(0, Itemstack({'item' : "carrotseed", 'count' : 15}))
		self.inventory.set_item(1, Itemstack({'item' : "carrot", 'count' : 0}))
		self.inventory.set_item(2, Itemstack({'item' : "hoe", 'count' : 6}))
		self.inventory.set_item(3, Itemstack({'item' : "gardenglove", 'count' : 0}))
		self.inventory.set_item(4, Itemstack({'item' : "coin", 'count' : 0}))
		self.game_data['inventory'] = self.inventory.get_metadata()


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


		self.inventory = Inventory(self.game_data['inventory'])


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
			wielded = Empty()
			wielded.item = self.inventory.value[self.game_data['dnum']]
			wielded.sprite = itemdict[wielded.item.value['item']]['sprite']
			wielded.sprite.rect.center = (player.rect.x + 10, player.rect.y + 35)



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
						match self.game_data['grid_state'][str((row, col))][0]:
							case 0:
								if  wielded.item.value['item'] == 'hoe' and wielded.item.get_count() > 0:
									self.game_data['grid_state'][str((row, col))] = (1, 0)  # Mark as empty crop plot
									self.inventory.add_item(Itemstack({'item' : 'hoe', 'count' : -1}))
							case 1:
								if wielded.item.value['item'] == 'carrotseed' and wielded.item.get_count() > 0:
									self.game_data['grid_state'][str((row, col))] = (2, time.time())  # Change to seeded crop plot and start timer to grow carrot
									self.inventory.add_item(Itemstack({'item' : 'carrotseed', 'count' : -1}))
							case 3:
								if wielded.item.value['item'] == 'gardenglove':
									self.game_data['grid_state'][str((row, col))] = (1, 0)
									self.inventory.add_item(Itemstack({'item' : 'carrot', 'count' : 1}))

					# Plant a new seed if the square has an empty crop plot
					else:
						match self.game_data['grid_state'][str((row, col))][0]:
							case 1:
								self.game_data['grid_state'][str((row, col))] = (2, (time.time()))  # Marks the plot as planted in and starts the timer to grow carrot

			# displays everything that need to be on top
			screen.blit(player.image, player.rect)
			screen.blit(wielded.sprite.image, wielded.sprite.rect)


			# displaying everything else

			for x in range(len(self.Blanks)):
				screen.blit(self.Blanks[x].image, self.Blanks[x].rect)


			# HotBar

			screen.blit(hotbarUI.image, hotbarUI.rect)

			x = width / 2 - 102
			y = height - (hotbarUI.rect.height/2) - 15
			for i in range(0, 5):
				if self.inventory.value[i].value['item'] != "":
					screen.blit(itemdict[self.inventory.value[i].value['item']]['sprite'].image, (x + (i * 34), y))

					carrots_text = font.render(f"{self.inventory.value[i].value['count']}", True, LBLUE)
					screen.blit(carrots_text, (x + (i * 34), y + 30))

			screen.blit(highlight.image, highlight.rect)



			# Inv

			if keys[pygame.K_e] and self.game_data['move_ticker'] == 0:
				self.game_data['openinv'] = not self.game_data['openinv']
				self.game_data['move_ticker'] = key_cooldown

			if self.game_data['openinv']:
				screen.blit(inventory.image, inventory.rect)

				x = inventory.rect.x + 35
				y = inventory.rect.y + 30
				for i in range(0, 24):
					if self.inventory.value[i].value['item'] != "":
						screen.blit(itemdict[self.inventory.value[i].value['item']]['sprite'].image, (x + (i % 5 * 50), y + (i // 5 * 50)))

						carrots_text = font.render(f"{self.inventory.value[i].value['count']}", True, BLACK)
						screen.blit(carrots_text, (x + (i % 5 * 50), y + (i // 5 * 50) + 30))

				pointer = carrotitem
				px = pointer.rect.width
				py = pointer.rect.height
				screen.blit(pointer.image,  (min(inventory.rect.x + inventory.rect.width - px, max(mousex, inventory.rect.x + px)) - px // 2, min(inventory.rect.y + inventory.rect.height - py, max(mousey, inventory.rect.y + py)) - py // 2))
				

			
			
			#esc for controls prompt
			controls_text = font.render("*CAUTION* Game Under Construction *CAUTION* ", True, YELLOW)
			screen.blit(controls_text, (10, 10))

			# Update display
			pygame.display.flip()





			# Post display operations

			#current buy and sell controls
			if self.game_data['move_ticker'] == 0:
				if keys[pygame.K_6]:
					self.inventory.add_item(Itemstack({'item' : 'coin', 'count' : self.inventory.get_item('carrot').get_count() * 2}))
					self.inventory.get_item('carrot').set_count(0)
					self.game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_7] and self.inventory.get_item('coin').get_count() >= 10:
					self.inventory.add_item(Itemstack({'item' : 'coin', 'count' : -10}))
					self.inventory.add_item(Itemstack({'item' : 'carrotseed', 'count' : 10}))
					self.game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_8] and self.inventory.get_item('coin').get_count() >= 20 and self.inventory.get_item('carrotseed').get_count()*2 + self.inventory.get_item('carrot').get_count()*2 + self.inventory.get_item('coin').get_count() >= 30:
					self.inventory.add_item(Itemstack({'item' : 'hoe', 'count' : 6}))
					self.inventory.add_item(Itemstack({'item' : 'coin', 'count' : -20}))
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
