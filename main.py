from levelManager import *
from player import *

"""
The main loop. The magic all happens here.
Each iteration of the while loop has currentLevel
progress() once through its timeline, updating all
actors in that quantum. The screen is drawn right
before the players' quanta.
"""

currentLevel = levelManager("playerSaveState")
while(True):
    currentLevel.update()