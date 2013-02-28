from levelManager import *
from player import *

currentLevel = levelManager("playerSaveState")
while(True):
    currentLevel.update()
    currentLevel.draw()