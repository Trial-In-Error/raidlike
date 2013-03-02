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
    def act(self):
        self.currentLevel.draw()
        masterInputParser(self, self.currentLevel)
        #os.system('cls' if os.name=='nt' else 'clear')
    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0]}
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
    def die(self):
        print("You died! Game over.\r")
        sys.exit()