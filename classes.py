from vars_and_stuff import *



# class for other sprites
class simplesprite(pygame.sprite.Sprite):
	def __init__(self, png, pos = (0, 0)):
		self.image = pygame.image.load(get_asset_path(png))
		self.rect = self.image.get_rect()
		self.rect.center = pos




class Itemstack:
	def __init__(self, item, count):
		self.item = item
		self.count = count

	def same_as(self, itemstack):
		if self.item == itemstack.item:
			return True
		else:
			return False

	def combine(self, itemstack):
		self.count += itemstack.count
		return self

No_Item = Itemstack("", 0)


class Inventory:
	value = []
	def __init__(self):
		for i in range(0, 24):
			self.value.insert(i, Itemstack("", 0))

	def add_item(self, itemstack):
		for i in range(0, 24):
			if self.value[i].same_as(itemstack):
				self.value[i].combine(itemstack)
				return True

			elif self.value[i].same_as(No_Item):
				self.value[i] = itemstack
				return True

		return False

	def get_metadata(self):
		return self.value




class Hotbar:
	max = 4
	def __init__(self, selected):
		self.selected = selected

	def next(self):
		self.selected += 1

		if self.selected > self.max:
			self.selected = 0

	def get_metadata(self):
		return self.selected
