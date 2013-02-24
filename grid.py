class grid():
	def __init__(self, player, levelWidth, levelHeight):
		self.levelHeight = levelHeight
		self.levelWidth = levelWidth
		self.grid = [[[] for i in range(levelWidth)] for x in range(levelHeight)]
		self.set(2,2,player)
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
					print("INDEXXXXX at x= "+xIterator+" and y= "+xIterator)
					raise StopIteration
				yield result
				xIterator += 1
			yIterator += 1
	def get(self, xpos, ypos):
		#temp = []
		#for 
		return self.grid[xpos-1][self.levelHeight-ypos]
	def set(self, xpos, ypos, value): #change to add
	#change to value, x, y
		self.grid[xpos-1][self.levelHeight-ypos].append(value)
	def setNoConv(self, xpos, ypos, value):
		self.grid[xpos-1][self.levelHeight-ypos].append(value)
	def remove(self, value): #uses ^> coordinates
		self.grid[value.xpos-1][self.levelHeight-value.ypos].remove(value)
	def clear(self):
		for y in range(1, self.levelHeight):
			for x in range(1, self.levelWidth):
				self.grid[x-1][self.levelHeight-y] = []
	def load(self):
		pass