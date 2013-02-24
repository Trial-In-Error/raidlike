from actor import *

class enemy(actor):
	def __init__(self, display='x'):
		self.display=display
		self.displayPriority=1
	def act(self):
		pass
	def collide(self):
		return True