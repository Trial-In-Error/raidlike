from levelManager import levelManager
from entity import Player, Enemy, Zombie, Item
import sys
from unicurses import cbreak, clear, curs_set, endwin, initscr, keypad, refresh, noecho, start_color, stdscr, getch, erase, mvaddch
import unicurses
from worldManager import worldManager
import config
import os
from camera import Camera
from religion import Pantheon

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
    for entry in config.colorDict:
           unicurses.init_pair(config.colorDict[entry][0], config.colorDict[entry][1], config.colorDict[entry][2])

    # Main menu
    erase()
    selected = 0
    temp_camera = Camera(51, 19, None)
    temp_camera.drawHUDBoundaries()
    while(True):
        if(selected == 0):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"][0]))
            unicurses.mvaddstr(1, 1, "New game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"][0]))
        else:
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["g12"][0]))
            unicurses.mvaddstr(1, 1, "New game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["g12"][0]))
        if(selected == 1):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"][0]))
            unicurses.mvaddstr(2, 1, "Load game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"][0]))
        else:
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["g12"][0]))
            unicurses.mvaddstr(2, 1, "Load game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["g12"][0]))
        if(selected == 2):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"][0]))
            unicurses.mvaddstr(3, 1, "Credits")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"][0]))
        else:
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["g12"][0]))
            unicurses.mvaddstr(3, 1, "Credits")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["g12"][0]))
        lineIn = getch()
        if(lineIn == unicurses.KEY_DOWN or lineIn == 'j'):
            selected = (selected + 1) % 3
        elif(lineIn == unicurses.KEY_UP or lineIn == 'k'):
            selected = (selected - 1) % 3
        elif(lineIn == unicurses.KEY_ENTER or lineIn == ' ' or lineIn == unicurses.KEY_LEFT):
            if(selected == 0):
                # Game world set-up
                world = worldManager()
                pantheon = Pantheon()
                config.world = world
                config.pantheon = pantheon
                world.pantheon = config.pantheon
                stdscr.refresh()

                # Main loop
                while(True):
                    world.update()
            elif(selected == 1):
                # Game world set-up
                world = worldManager()
                world.load()
                config.world = world
                config.pantheon = world.pantheon
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