from grid import *
from timeLine import *
from entity import *
from enemy import *
from player import *
from outputBuffer import *
import os

stdscr = initscr()
start_color()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)

"""
The workhorse of the game engine. It updates() every
iteration of the main while loop. Every update act()s
for every actor in that quantum of the timeline. It
also contains the draw() function, which is called
as the first part of the player's act().

Currently, the __init__() is taking the place of
load(), because there is no data structure in place
for loading levels.

The player must always be initialized last, or else
the enemies will appear to double-move on the first
turn. It looks really awkward.
"""

start_color()
init_pair(1, COLOR_YELLOW, COLOR_BLACK) # used for the status bar
init_pair(2, COLOR_CYAN, COLOR_BLACK) # used for the walls
init_pair(3, COLOR_RED, COLOR_BLACK) # used for the statues
init_pair(4, COLOR_RED, COLOR_BLACK) # used for low hit points

class levelManager():
    currentTimeLine = timeLine(16)
    viewDistance = 3;
    levelWidth = 8;
    levelHeight = 8;
    def __init__(self, playerSaveState, stdscr):
        self.currentGrid = grid(self.levelWidth, self.levelHeight)
        self.populateWalls()
        self.populateFloor()
        self.currentOutputBuffer = outputBuffer(self.levelHeight)
        e1 = enemy(5,5,self)
        e2 = enemy(5,2,self)
        self.currentPlayer = player(2,2,self)
        self.stdscr = stdscr
    def load(self):
        pass
    def update(self):
        for actor in self.currentTimeLine:
            actor.act()
        self.currentTimeLine.progress()

    def draw(self):
        clear()
        if (self.currentPlayer in self.currentTimeLine.get()):
            #temp2 = ""
            for square in self.currentGrid:
                try:
                    sorted(square, reverse=True)[0].draw()
                except IndexError:
                    print("Some cell is completely empty.")
                    # We could fill it with a floor tile entity!
                    #temp2 += "?"
                    #    Instead, it's filled with a '?' for debugging purposes.
        self.currentOutputBuffer.output()
    def populateFloor(self):
        for y in range(1, self.levelHeight+1):
            for x in range(1, self.levelWidth+1):
                if(self.currentGrid.get(x, y) == []):
                    #for debugging, use below to print column/row indices
                    #entity(x, y, self, str(y))
                    entity(x, y, self, '.')
    def populateWalls(self):
        for x in range(1, self.levelWidth+1):
            wall(x, 1, self)
            wall(x, self.levelHeight, self)
        for y in range(2, self.levelHeight):
            wall(1, y, self)
            wall(self.levelWidth, y, self)