from entity import *
from masterInputParser import *
from grid import *
from actor import *
from sys import *
import os

class player(actor):
    def __init__(self, xpos, ypos, currentLevel, display='@'):
        self.currentLevel = currentLevel
        self.display = display
        self.displayPriority = 1
        self.damage = 1
        self.health = 10
        self.currentGrid = currentLevel.currentGrid
        self.xpos = xpos
        self.ypos = ypos
        self.currentGrid.add(self, self.xpos, self.ypos)
        self.currentTimeLine = currentLevel.currentTimeLine
        self.currentTimeLine.add(self)
        self.currentOutputBuffer = currentLevel.currentOutputBuffer
        self.name = "player"
        self.displayColor = 3
        self.description = "It's you."
    def act(self):
        self.currentLevel.draw()
        masterInputParser(self, self.currentLevel)
    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0],
                    'northwest': [-1, 1],
                    'northeast': [1, 1],
                    'southwest': [-1 ,-1],
                    'southeast': [1, -1]}
        temp = []
        for entity in self.currentGrid.get(self.xpos + moveDict[direction][0],
        self.ypos + moveDict[direction][1]):
            temp.append(entity.collide())
        if(temp.count("true")==0 and temp.count("combat_enemy")==0):
            self.doMove(moveDict[direction][0], moveDict[direction][1])
        elif(temp.count("combat_enemy")==1):
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
        else:
            self.andWait(0)
    def collide(self):
        return "combat_player"
    def die(self, killer):
        #self.currentLevel.currentOutputBuffer.clear()
        print("\n\rYou died! Game over.")
        getch()
        clear()
        refresh()
        endwin()
        # WHY DOESN'T THIS WORK?
        #self.currentLevel.currentOutputBuffer.add("You died! Game over.")
        #self.currentLevel.draw()
        #print("You died! Game over.\r")
        print("Be seeing you...")
        sys.exit()