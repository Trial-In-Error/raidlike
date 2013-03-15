from grid import *
from timeLine import *
from entity import *
from enemy import *
from player import *
from outputBuffer import *
from camera import *
import os

stdscr = initscr()
start_color()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)
start_color()

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
        e2 = zombie(5,2,self)
        self.currentPlayer = player(4,4,self)
        self.stdscr = stdscr
        self.currentCamera = camera(5,5,self)
        #these should be in entity, not levelmanager...
        self.coloringDict = {"enemy":"yellow"}
        self.colorDict = {"yellow":[1, COLOR_YELLOW, COLOR_BLACK],
            "cyan":[2, COLOR_CYAN, COLOR_BLACK],
            "red":[3, COLOR_RED, COLOR_BLACK],
            "white":[4, COLOR_WHITE, COLOR_BLACK],
            "blue":[5, COLOR_BLUE, COLOR_BLACK]
            }
        for entry in self.colorDict:
            init_pair(self.colorDict[entry][0], self.colorDict[entry][1], self.colorDict[entry][2])
    def load(self, levelName):
        toParse = open(levelName, 'r')
        # EXTEND ME HERE

    def update(self):
        for actor in self.currentTimeLine:
            actor.act()
        self.currentTimeLine.progress()

    def draw(self):
        clear()
        self.drawHUD()
        self.currentCamera.draw(self.currentPlayer.xpos, self.currentPlayer.ypos)
        self.currentOutputBuffer.output()
    def drawHUD(self):
        attron(COLOR_PAIR(self.colorDict["white"][0]))
        mvaddstr(0, self.levelWidth, self.currentPlayer.playerName)
        mvaddstr(1, self.levelWidth, self.currentPlayer.className)
        mvaddstr(2, self.levelWidth, "Health: "+str(self.currentPlayer.health))
        attroff(COLOR_PAIR(self.colorDict["white"][0]))
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