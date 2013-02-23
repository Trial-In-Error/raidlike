class grid():
	def __init__(self, player, levelWidth, levelHeight):
		self.levelHeight = levelHeight
		self.levelWidth = levelWidth
		self.grid = [[[]*levelWidth]*levelHeight for x in range(0,levelHeight)]
		self.set(1,1,player)
	def __iter__(self):
		xIterator = 1
		yIterator = 1
		#goes row by row, starting at bottom left as per get/set
		while(yIterator <= self.levelHeight):
			xIterator = 1
			while(xIterator <= self.levelWidth):
				try:
					result = self.get(xIterator, yIterator)
				except IndexError:
					raise StopIteration
				yield result
				xIterator += 1
			
			yIterator += 1
	def get(self, xpos, ypos):
		return self.grid[xpos-1][self.levelHeight-ypos]
	def set(self, xpos, ypos, value): #change to add
	#change to value, x, y
		self.grid[xpos-1][self.levelHeight-ypos] = value
	def load(self):
		pass