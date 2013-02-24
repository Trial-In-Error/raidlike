from grid import *
from timeLine import *
from entity import *
from enemy import *

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
				self.currentGrid.set(x,y,entity(str(y)))
		self.currentTimeLine.add(player)
		self.currentPlayer = player
		#self.currentGrid.set(2, 2, player)
		player.currentGrid = self.currentGrid
		player.xpos=2
		player.ypos=2
		e1 = enemy()
		e1.xpos=3
		e1.ypos=3
		self.currentGrid.set(3,3,e1)
		for x in range(0,self.levelWidth+1):
			wall(x, 1, self.currentGrid)
			wall(x, self.levelHeight, self.currentGrid)
		for y in range(1, self.levelHeight):
			wall(1, y, self.currentGrid)
			wall(self.levelWidth, y, self.currentGrid)


	def load(self):
		pass
	def update(self):
		for actor in self.currentTimeLine:
			actor.act()	

	def draw(self):
		temp = []
		temp2 = ""
		for square in self.currentGrid:
			temp2 += sorted(square, reverse=True)[0].draw()
		for y in reversed(range(0, self.levelHeight)):
			print(temp2[y*self.levelWidth:(y+1)*self.levelWidth], end="\r\n")