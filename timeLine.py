class timeLine():
	currentLocation = 0
	line = []
	def __init__(self, size):
		self.size = size
		self.line = [[] for x in range(0, size)]
	def lengthen(self):
		self.size = self.size+1
		self.line.append([])
	def add(self, object, displacement = 0):
		self.line[self.currentLocation+displacement].append(object)
	def clear(self, displacement = 0):
		self.line[self.currentLocation+displacement] = []
	def progress(self, displacement = 0):
		while(self.currentLocation + displacement >= self.size):
			displacement = displacement - self.size
		self.currentLocation = self.currentLocation + displacement