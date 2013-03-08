from levelManager import *
from player import *
from unicurses import *
stdscr = initscr()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)

"""
The main loop. The magic all happens here.
Each iteration of the while loop has currentLevel
progress() once through its timeline, updating all
actors in that quantum. The screen is drawn right
before the players' quanta.
"""

currentLevel = levelManager("playerSaveState", stdscr)
#currentLevel.draw()
stdscr.refresh()
while(True):
    currentLevel.update()