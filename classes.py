from vars_and_stuff import *



# class for other sprites
class simplesprite(pygame.sprite.Sprite):
	def __init__(self, png, pos = (0, 0)):
		self.image = pygame.image.load(get_asset_path(png))
		self.rect = self.image.get_rect()
		self.rect.center = pos


class Empty:
	def __init__(self):
		return


class Itemstack:
	def __init__(self, itemstack = {'item' : "", 'count' : 0}):
		item, count = itemstack

		self.value = itemstack

	def same_as(self, itemstack):
		if self.value['item'] == itemstack.value['item']:
			return True
		else:
			return False

	def combine(self, itemstack):
		self.value['count'] += itemstack.value['count']
		return self

	def get_count(self):
		return self.value['count']

	def set_count(self, n):
		self.value['count'] = n

	def add_count(self, n):
		self.value['count'] += n

	def get_item(self):
		return self.value['item']

	def get_metadata(self):
		return self.value

No_Item = Itemstack()


class Inventory:
	def __init__(self, value = None):
		self.value = []

		if value != None:
			for i in range(25):
				self.value.insert(i, Itemstack(value[i]))
		else:
			for i in range(25):
				self.value.insert(i, No_Item)


	# Broken
	def add_item(self, itemstack):
		free = -1
		for i in range(len(self.value)):
			if self.value[i].same_as(itemstack):
				self.value[i].combine(itemstack)
				return True

			elif self.value[i].same_as(No_Item) and free == -1:
				free = i

		if free != -1:
			self.value[i] = itemstack
			return True

		return False

	def set_item(self, i, itemstack):
		self.value[i] = itemstack

	def get_item(self, i):
		return self.value[i]

	def get_item_by_name(self, item):
		for i in range(len(self.value)):
			if self.value[i].value['item'] == item:
				return self.value[i]

	def get_metadata(self):
		meta = []
		for i in range(len(self.value)):
			meta.insert(i, self.value[i].get_metadata())

		return meta




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
