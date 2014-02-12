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

    # Turn on terminal 256-color mode
    try:
        bool(os.environ['TERM']) #?
    except KeyError:
        os.environ['TERM'] = foo
    os.environ['TERM'] = "xterm-256color"

    # Curses set-up
    stdscr = initscr()
    start_color()
    noecho()
    cbreak()
    curs_set(0)
    keypad(stdscr, True)
    start_color()

    # Game world set-up
    world = worldManager()
    config.world = world
    stdscr.refresh()

    # Main loop
    while(True):
        world.update()

except:
    #os.environ['TERM'] = "xterm"
    clear()
    refresh()
    endwin()
    raise