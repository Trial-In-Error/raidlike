from grid import *
from timeLine import *
from entity import *
from enemy import *
from player import *
from outputBuffer import *
import os

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
    levelWidth = 7;
    levelHeight = 7;
    def __init__(self, playerSaveState, stdscr):
        self.currentGrid = grid(self.levelWidth, self.levelHeight)
        self.populateWalls()
        self.populateFloor()
        self.currentOutputBuffer = outputBuffer()
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
        #os.system('cls' if os.name=='nt' else 'clear')
        #clear()
        if (self.currentPlayer in self.currentTimeLine.get()):
            temp2 = ""
            for square in self.currentGrid:
                try:
                    temp2 += str(sorted(square, reverse=True)[0].draw())
                except IndexError:
                    print("Some cell is completely empty.")
                    # We could fill it with a floor tile entity!
                    temp2 += "?"
                    # Instead, it's filled with a '?' for debugging purposes.
            for y in reversed(range(0, self.levelHeight)):
                print(temp2[y*self.levelWidth:(y+1)*self.levelWidth],
                end="\r\n")
        self.currentOutputBuffer.output()
        refresh()
    def populateFloor(self):
        for y in range(1, self.levelHeight+1):
            for x in range(1, self.levelWidth+1):
                if(self.currentGrid.get(x, y) == []):
                    #for debugging, use below to print column/row indices
                    #self.currentGrid.add(entity(y, x, str(y), x, y)
                    self.currentGrid.add(entity(x, y, '.'), x, y)
    def populateWalls(self):
        for x in range(0, self.levelWidth):
            wall(x, 1, self.currentGrid)
            wall(x, self.levelHeight, self.currentGrid)
        for y in range(2, self.levelHeight):
            wall(1, y, self.currentGrid)
            wall(self.levelWidth, y, self.currentGrid)