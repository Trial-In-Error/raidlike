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

    # Set up the global colorPalette
    for i in range(0, 256):
        config.colorPalette.update({i:[i, i, unicurses.COLOR_BLACK]})
    config.colorPalette.update({256:[256, unicurses.COLOR_YELLOW, unicurses.COLOR_BLACK]})
    config.colorPalette.update({257:[257, unicurses.COLOR_CYAN, unicurses.COLOR_BLACK]})
    config.colorPalette.update({258:[258, unicurses.COLOR_RED, unicurses.COLOR_BLACK]})
    config.colorPalette.update({259:[259, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK]})
    config.colorPalette.update({260:[260, unicurses.COLOR_BLUE, unicurses.COLOR_BLACK]})
    config.colorPalette.update({261:[261, unicurses.COLOR_BLACK, unicurses.COLOR_BLACK]})
    for entry in config.colorPalette:
        unicurses.init_pair(config.colorPalette[entry][0], config.colorPalette[entry][1], config.colorPalette[entry][2])

    # Main menu
    erase()
    selected = 0
    temp_camera = Camera(51, 19, None)
    temp_camera.drawHUDBoundaries()
    while(True):
        if(selected == 0):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"]))
            unicurses.mvaddstr(1, 1, "New game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"]))
        else:
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["g12"]))
            unicurses.mvaddstr(1, 1, "New game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["g12"]))
        if(selected == 1):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"]))
            unicurses.mvaddstr(2, 1, "Load game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"]))
        else:
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["g12"]))
            unicurses.mvaddstr(2, 1, "Load game")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["g12"]))
        if(selected == 2):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"]))
            unicurses.mvaddstr(3, 1, "Credits")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"]))
        else:
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["g12"]))
            unicurses.mvaddstr(3, 1, "Credits")
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["g12"]))
        lineIn = getch()
        if(lineIn == unicurses.KEY_DOWN or lineIn == 'j'):
            selected = (selected + 1) % 3
        elif(lineIn == unicurses.KEY_UP or lineIn == 'k'):
            selected = (selected - 1) % 3
        elif(lineIn == unicurses.KEY_ENTER or lineIn == ' ' or lineIn == unicurses.KEY_LEFT):
            if(selected == 0):
                # Game world set-up
                world = worldManager()
                #pantheon = Pantheon()
                config.world = world
                #config.pantheon = pantheon
                world.pantheon = Pantheon()
                stdscr.refresh()

                # Main loop
                while(True):
                    world.update()
            elif(selected == 1):
                # Game world load
                world = worldManager()
                world.load()
                config.world = world
                #config.pantheon = world.pantheon
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