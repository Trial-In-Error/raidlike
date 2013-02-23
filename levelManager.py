from grid import *
from timeLine import *
from entity import *

class levelManager():
	currentTimeLine = timeLine(16)
	viewDistance = 3;
	levelWidth = 5;
	levelHeight = 5;
	def __init__(self, player):
		self.currentGrid = grid(player, self.levelWidth, self.levelHeight)
		for y in range(1, self.levelHeight+1):
			for x in range(1, self.levelWidth+1):
				#self.currentGrid.set(x,y,entity("("+str(y)+"."+str(x)+")"))
				self.currentGrid.set(x,y,entity())
		self.currentTimeLine.add(player)
		self.currentGrid.set(3, 3, player)
	def load(self):
		pass
	def update(self):
		for actor in self.currentTimeLine:
			actor.act()	

	def draw(self):
		temp = []
		temp2 = ""
		for element in self.currentGrid:
			temp2 += element.draw()
		for y in range(0, self.levelHeight):
			print(temp2[y*self.levelWidth:(y+1)*self.levelWidth], end="\r\n")