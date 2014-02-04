from levelManager import levelManager
from entity import Player, Enemy, Zombie, Item
import sys
from unicurses import cbreak, clear, curs_set, endwin, initscr, keypad, refresh, noecho, start_color, stdscr
from worldManager import worldManager
import config
import os

"""
The main loop. The magic all happens here.
Each iteration of the while loop has currentLevel
progress() once through its timeline, updating all
actors in that quantum. The screen is drawn right
before the players' quanta.
"""

try:
    try:
        print(os.environ['TERM'])
    except KeyError:
        os.environ['TERM'] = foo
    os.environ['TERM'] = "xterm-256color"

    stdscr = initscr()
    start_color()
    noecho()
    cbreak()
    curs_set(0)
    keypad(stdscr, True)
    start_color()
    world = worldManager()
    config.world = world

    stdscr.refresh()
    while(True):
        world.update()

except:
    clear()
    refresh()
    endwin()
    raise