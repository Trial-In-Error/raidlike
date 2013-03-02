from levelManager import *
from player import *

currentLevel = levelManager("playerSaveState")
currentLevel.draw()
while(True):
    currentLevel.update()
    #currentLevel.draw()