from levelManager import *
currentLevel = levelManager(0)
while(True):
	currentLevel.update()
	currentLevel.draw()