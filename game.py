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
fully_grown_carrot = pygame.image.load(get_asset_path("fullygrowncarrot.png"))


gardenhoe = simplesprite('gardenhoe.png')
coin = simplesprite('coin.png')
noitem = simplesprite('blank.png')
soil = simplesprite('emptycropplot.png')

carrot_seed_plot = simplesprite('carrotseedplot.png')
fully_grown_carrot = simplesprite('fullygrowncarrot.png')
carrot = simplesprite('carrot.png')
carrotseeds = simplesprite('carrotseedpack.png')

radish = simplesprite('radish.png')
radish_seeds = simplesprite('radish_seeds.png')
radish_ungrown_plot = simplesprite('radish_ungrown_plot.png')
radish_grown_plot = simplesprite('radish_grown_plot.png')




items = {}



items = {
	'' : {
		'sprite' : noitem	# Must
	},

	'radish' : {
		'sprite' : radish,
		'countable' : 0,
		'value' : 3
	},
	'radish_seeds' : {
		'sprite' : radish_seeds,
		'countable' : 15,
		'use_on_soil' : ('radish_ungrown_plot', 3),
		'give_player' : True,
		'price' : (1, 2)
	},
	'radish_ungrown_plot' : {
		'sprite' : radish_ungrown_plot,
		'grows' : ('radish_grown_plot', 0)
	},
	'radish_grown_plot' : {
		'sprite' : radish_grown_plot,
		'fruit' : ('radish', ("soil", 0))
	},

	'carrot' : {
		'sprite' : carrot,
		'countable' : 0,
		'value' : 2
	},
	'carrotseed' : {
		'sprite' : carrotseeds,
		'countable' : 15,
		'use_on_soil' : ('carrot_seed_plot', 5),
		'give_player' : True,
		'price' : (1, 1)
	},
	'carrot_seed_plot' : {
		'sprite' : carrot_seed_plot,
		'grows' : ('fully_grown_carrot', 0)
	},
	'fully_grown_carrot' : {
		'sprite' : fully_grown_carrot,
		'fruit' : ('carrot', ("soil", 0))
	},

	'hoe' : {
		'sprite' : gardenhoe,
		'countable' : 6,
		'use_on_' : ('soil', 0),
		'give_player' : True,
		'price' : (2, 1)
	},
	'coin' : {
		'sprite' : coin,
		'countable' : 0
	},
	'soil' : {
		'sprite' : soil,
	}
}


market_items = {}
for item, idef in items.items():
	if 'value' in idef:
		market_items[item] = idef['value']

shop_items = {}
for item, idef in items.items():
	if 'price' in idef:
		shop_items[item] = idef['price']



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
		self.game_data['open_menu'] = None

		self.inventory = Inventory()
		for key, idef in items.items():
			if 'give_player' in idef:
				if 'countable' in idef:
					c = idef['countable']
					self.inventory.add_item(Itemstack({'item' : key, 'count' : c}))
				else:
					self.inventory.add_item(Itemstack({'item' : key, 'count' : 0}))
			

		self.game_data['inventory'] = self.inventory.get_metadata()


		self.rows, self.cols = width // self.game_data['grid_size'], width // self.game_data['grid_size']
		self.grid = [[0] * self.cols for _ in range(self.rows)]
		# Dictionary to store the state and planting time of each grid square
		self.game_data['grid_plots'] = {str((row, col)): ("", 0) for row in range(self.rows) for col in range(self.cols)}

		# Only used at start/save time data
		self.game_data['player_pos'] = (width / 2, height / 2)


		# Load
		if load:
			self._load()


		self.inventory = Inventory(self.game_data['inventory'])


		global player
		player = simplesprite('player.png', self.game_data['player_pos'])



		# ambiance
		mixer.music.set_volume(int(not self.game_data['mute']))


		self.clock = pygame.time.Clock()

		# Start
		pygame.mouse.set_visible(False)
		self._start()

		# Save
		self._save()
		pygame.mouse.set_visible(True)


	def _help(self):
		while True:
			events = pygame.event.get()
			keys = pygame.key.get_pressed()
			for event in events:
				if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
					self._save()
					return

			if not keys[pygame.K_h]:
				break

			screen.fill(YELLOW)

			#esc for controls prompt
			controls_text = font.render("*CAUTION* Game Under Construction *CAUTION* ", True, BLACK)
			screen.blit(controls_text, (10, 10))

			# Update display
			pygame.display.flip()

			self.clock.tick(60)
			


	def _start(self):
		moving_item = -1
		game_data = self.game_data
		while True:
			#variables that updated every frame
			events = pygame.event.get()
			keys = pygame.key.get_pressed()

			# Help HUD
			if keys[pygame.K_h]:
				self._help()
				continue

			mousex, mousey = pygame.mouse.get_pos()
			mouse_rect = pygame.Rect(mousex+3, mousey+3, 9, 9)

			# per loop vars
			pick_up_item = False

			#prevents multiple key presses from one
			if game_data['move_ticker'] >= 1:
				game_data['move_ticker'] -= 1
			elif game_data['move_ticker'] != 0:
				game_data['move_ticker'] = 0


			#display background
			screen.blit(background.image, background.rect)
			#set where the sprites will be displayed

			#hotbar and wieled
			if keys[pygame.K_1]:
				game_data['dnum'] = 0
			elif keys[pygame.K_2]:
				game_data['dnum'] = 1
			elif keys[pygame.K_3]:
				game_data['dnum'] = 2
			elif keys[pygame.K_4]:
				game_data['dnum'] = 3
			elif keys[pygame.K_5]:
				game_data['dnum'] = 4

			wielded = Empty()
			wielded.itemstack = self.inventory.value[game_data['dnum']]
			wielded.sprite = items[wielded.itemstack.value['item']]['sprite']
			wielded.sprite.rect.center = (player.rect.x + 10, player.rect.y + 35)



			# creates the grid
			for row in range(self.rows):
				for col in range(self.cols):
					rect = pygame.Rect(col * game_data['grid_size'], row * game_data['grid_size'], game_data['grid_size'], game_data['grid_size'])

					# Display the appropriate crop grow stage based on the grid state
					state, planting_time = game_data['grid_plots'][str((row, col))]
					if state != "":
						if 'grows' in items[state] and planting_time > 0 and time.time() >= planting_time:
							game_data['grid_plots'][str((row, col))] = items[state]['grows']

						screen.blit(items[state]['sprite'].image, rect.topleft)


			# displays everything that need to be on top
			screen.blit(player.image, player.rect)
			screen.blit(wielded.sprite.image, wielded.sprite.rect)

			# event handler
			SPACE_pressed = keys[K_SPACE] # Optimization
			for event in events:
				if event.type == pygame.QUIT:
					return

				#if event.type == pygame.VIDEORESIZE:
				#  width, height = event.w, event.h
				if event.type == pygame.MOUSEBUTTONDOWN:
					pick_up_item = True

				if (event.type == pygame.MOUSEBUTTONDOWN and player.rect.colliderect(mouse_rect)) or SPACE_pressed:
					col = player.rect.center[0] // game_data['grid_size']
					row = player.rect.center[1] // game_data['grid_size']

					# Place empty crop plot if the square is empty
					itemstack = wielded.itemstack
					itemdef = items[itemstack.get_item()]
					plot, _ = game_data['grid_plots'][str((row, col))]

					if 'use_on_' + plot in itemdef and itemstack.get_count() > 0:
						itemstack.add_count(-1)
						game_data['grid_plots'][str((row, col))] = (itemdef['use_on_' + plot][0], itemdef['use_on_' + plot][1] + time.time())
						continue

					elif plot != "" and 'fruit' in items[plot]:
						self.inventory.add_item(Itemstack(itemstack = {'item' : items[plot]['fruit'][0], 'count' : 1}))
						game_data['grid_plots'][str((row, col))] = items[plot]['fruit'][1]
						continue


			# Controls
			if game_data['move_ticker'] == 0:
				if keys[pygame.K_ESCAPE]:
					return

				elif keys[pygame.K_e]:
					if game_data['open_menu'] == 'inv':
						game_data['open_menu'] = None
					else:
						game_data['open_menu'] = 'inv'
					game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_6]:
					if game_data['open_menu'] == 'shop':
						game_data['open_menu'] = None
					else:
						game_data['open_menu'] = 'shop'
					game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_7]:
					if game_data['open_menu'] == 'market':
						game_data['open_menu'] = None
					else:
						game_data['open_menu'] = 'market'
					game_data['move_ticker'] = key_cooldown

				elif keys[pygame.K_m]:
					mixer.music.set_volume(int(game_data['mute']))
					game_data['mute'] = not game_data['mute']
					game_data['move_ticker'] = key_cooldown



			# HotBar

			screen.blit(hotbarUI.image, hotbarUI.rect)

			hotbar_x = width / 2 - 102
			hotbar_y = height - (hotbarUI.rect.height/2) - 15
			for i in range(5):
				item = self.inventory.value[i]
				item_def = items[item.value['item']]
				item_sprite = item_def['sprite']

				item_sprite.rect.x = hotbar_x + (i * 34)
				item_sprite.rect.y = hotbar_y
				screen.blit(item_sprite.image, item_sprite.rect)

				if pick_up_item and item_sprite.rect.colliderect(mouse_rect):
					game_data['dnum'] = i

				if 'countable' in item_def:
					carrots_text = font.render(f"{item.get_count()}", True, LBLUE)
					screen.blit(carrots_text, (hotbar_x + (i * 34), hotbar_y + 30))

			highlight.rect.center = (hotbar_x+16 + (34 * game_data['dnum']), hotbar_y + 15)
			screen.blit(highlight.image, highlight.rect)



			# Inv

			if game_data['open_menu'] == 'inv':
				screen.blit(inventory.image, inventory.rect)

				x = inventory.rect.x + 35
				y = inventory.rect.y + 30
				item_picked_up = False
				for i in range(len(self.inventory.value)):
					itemstack = self.inventory.value[i]
					item_def = items[itemstack.value['item']]
					item_sprite = item_def['sprite']

					item_sprite.rect.x = x + (i % 5 * 50)
					item_sprite.rect.y = y + (i // 5 * 50)

					# should be out of loop, this is inefficient
					if not item_picked_up and pick_up_item and item_sprite.rect.colliderect(mouse_rect):
						if moving_item == -1 and itemstack.get_item() != '':
							moving_item = i
						elif moving_item == i:
							moving_item = -1
						else:
							itemstack = self.inventory.get_item(i)
							self.inventory.set_item(i, self.inventory.get_item(moving_item))
							self.inventory.set_item(moving_item, itemstack)
							moving_item = -1

						item_picked_up = True

					# dont render extra stuff
					if moving_item == i:
						continue

					if itemstack.value['item'] != "":
						screen.blit(item_sprite.image, item_sprite.rect)

						if 'countable' in item_def:
							screen.blit(font.render(f"{itemstack.get_count()}", True, BLACK), (item_sprite.rect.x, item_sprite.rect.y + 30))

				if moving_item != -1:
					pointer = items[self.inventory.value[moving_item].value['item']]['sprite']
					px = pointer.rect.width
					py = pointer.rect.height
					screen.blit(pointer.image,  (min(inventory.rect.x + inventory.rect.width - px, max(mousex, inventory.rect.x + px)) - px // 2, min(inventory.rect.y + inventory.rect.height - py, max(mousey, inventory.rect.y + py)) - py // 2))

			elif game_data['open_menu'] == 'shop':
				screen.blit(inventory.image, inventory.rect)

				x = inventory.rect.x + 35
				y = inventory.rect.y + 30
				i = 0
				for item, price in shop_items.items():
					cost, value = price

					item_sprite = items[item]['sprite']

					item_sprite.rect.x = x + (i % 5 * 50)
					item_sprite.rect.y = y + (i // 5 * 50)
					screen.blit(item_sprite.image, item_sprite.rect)

					if pick_up_item and game_data['move_ticker'] == 0 and item_sprite.rect.colliderect(mouse_rect) and self.inventory.get_item_by_name('coin').get_count() >= cost:
						self.inventory.add_item(Itemstack({'item' : 'coin', 'count' : -cost}))
						self.inventory.add_item(Itemstack({'item' : item, 'count' : value}))


					screen.blit(font.render(f"{cost}", True, YELLOW), (item_sprite.rect.x - 5, item_sprite.rect.y - 5))
					screen.blit(font.render(f"{value}", True, BLACK), (item_sprite.rect.x - 5, item_sprite.rect.y + 30))

					i += 1

			elif game_data['open_menu'] == 'market':
				screen.blit(inventory.image, inventory.rect)

				x = inventory.rect.x + 35
				y = inventory.rect.y + 30
				i = 0
				for item, value in market_items.items():

					item_sprite = items[item]['sprite']

					item_sprite.rect.x = x + (i % 5 * 50)
					item_sprite.rect.y = y + (i // 5 * 50)
					screen.blit(item_sprite.image, item_sprite.rect)

					if pick_up_item and game_data['move_ticker'] == 0 and item_sprite.rect.colliderect(mouse_rect) and self.inventory.get_item_by_name(item).get_count() >= 1:
						self.inventory.add_item(Itemstack({'item' : 'coin', 'count' : value}))
						self.inventory.add_item(Itemstack({'item' : item, 'count' : -1}))


					screen.blit(font.render(f"{value}", True, BLUE), (item_sprite.rect.x - 5, item_sprite.rect.y + 30))

					i += 1


			if not game_data['open_menu'] == "inv":
				moving_item = -1
				

			
			
			pygame.draw.rect(screen, BROWN, mouse_rect)

			# Update display
			pygame.display.flip()


			# movement
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



			self.clock.tick(60)

			self.inventory.clean()
