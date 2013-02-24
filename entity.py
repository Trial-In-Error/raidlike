class entity():
	xpos = 'null'
	ypos = 'null'
	def __init__(self, display='.'):
		self.display = display
		self.displayPriority = 0
	def __lt__(self, other):
		if(self.displayPriority < other.displayPriority):
			return True
		elif(self.displayPriority < other.displayPriority):
			return False
		#else:
			#raise CustomException
	def draw(self):
		return(self.display)
	def describe(self):
		pass
	def remove(self):
		pass
	def collide(self):
		return False