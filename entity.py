class entity():
	def __init__(self, grid, xloc, yloc):
		grid.set(xloc, yloc, self)
	def draw(self):
		pass
	def describe(self):
		pass
	def remove(self):
		pass
	def collide(self):
		pass