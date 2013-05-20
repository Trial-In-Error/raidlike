from levelManager import levelManager
from entity import Player, Enemy, Zombie, Item
import sys
from unicurses import cbreak, clear, curs_set, endwin, initscr, keypad, refresh, noecho, start_color, stdscr

"""
The main loop. The magic all happens here.
Each iteration of the while loop has currentLevel
progress() once through its timeline, updating all
actors in that quantum. The screen is drawn right
before the players' quanta.
"""

try:
    stdscr = initscr()
    start_color()
    noecho()
    cbreak()
    curs_set(0)
    keypad(stdscr, True)
    start_color()

    if len(sys.argv) > 1:
        level = levelManager.load(sys.argv[1])
    else:
        # Set up default level
        level = levelManager("playerSaveState", 21 , 21)
        level.setPlayer(Player(4, 4, level))
        level.populateWalls()
        level.populateFloor()
        e1 = Enemy(5,5,level)
        e2 = Zombie(5,2,level)

    stdscr.refresh()
    while(True):
        level.update()

except:
    clear()
    refresh()
    endwin()
    raise
