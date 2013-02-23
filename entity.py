class entity():
	def __init__(self, display='.'):
		self.display = display
	def draw(self): #generalize to return some stored char value
		return(self.display)
	def describe(self):
		pass
	def remove(self):
		pass
	def collide(self):
		pass