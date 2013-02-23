from grid import *
from timeLine import *

class levelManager():
	currentTimeLine = timeLine(16)
	viewDistance = 3;
	levelWidth = 5;
	levelHeight = 5;
	def __init__(self, player):
		self.currentTimeLine.add(player)
		self.currentGrid = grid(player, self.levelWidth, self.levelHeight)
	def load(self):
		pass
	def update(self):
		for actor in self.currentTimeLine:
			actor.act()	

	def draw(self):
		for element in self.currentGrid:
			try:
				element.draw()
			except TypeError:
				pass