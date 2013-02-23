from levelManager import *
from player import *

currentPlayer = player()
currentLevel = levelManager(currentPlayer)
while(True):
	currentLevel.update()
	currentLevel.draw()