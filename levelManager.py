from grid import *
class levelManager():
	timeLine = []
	levelWidth = 5;
	levelHeight = 5;
	def __init__(self, player):
		#self.timeLine[0] = player
		self.currentGrid = grid(player, self.levelWidth, self.levelHeight)
	def load(self):
		pass
	def update(self):
		for actor in self.timeLine:
			actor.act()
	def draw(self):
		#for element in grid[][]
		#	element.draw() 
		pass