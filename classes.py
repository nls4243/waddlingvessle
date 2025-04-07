from vars_and_stuff import *


# class for player sprite
class Sprite(pygame.sprite.Sprite):
	def __init__(self, x, y, l, h, png):
		super().__init__()
		self.image = pygame.Surface((l, h))
		self.image = pygame.image.load(png)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.alive = True
		self.direction = 1

# class for other sprites
class simplesprite(pygame.sprite.Sprite):
	def __init__(self, png):
		self.image = pygame.image.load(get_asset_path(png))
		self.rect = self.image.get_rect()
		self.rect.center = (1, 1)



class Inventory:
	value = []
	def _init__(self, element_count):
		for i in range(0, element_count-1):
			self.value.(i, {'count' : 0, 'item' : })