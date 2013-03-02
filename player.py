from entity import *
from masterInputParser import *
from grid import *
from actor import *

class player(actor):
    #currentGrid = grid("foo",5,5)
    def __init__(self, xpos, ypos, currentGrid, currentTimeLine, display='@'):
        self.display = display
        self.displayPriority = 1
        self.damage = 1
        self.health = 5
        self.currentGrid = currentGrid
        self.xpos = xpos
        self.ypos = ypos
        self.currentGrid.add(self, self.xpos, self.ypos)
        self.currentTimeLine = currentTimeLine
        self.currentTimeLine.add(self)
    def act(self):
        masterInputParser(self)
    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0]}
        temp = []
        for entity in list(self.currentGrid.get(self.xpos+moveDict[direction][0], self.ypos+moveDict[direction][1])):
            temp.append(entity.collide())
        if(temp.count("true")==0 and temp.count("combat")==0):
            print("I moved "+direction+".")
            self.doMove(moveDict[direction][0], moveDict[direction][1])
        elif(temp.count("combat")==1):
            print("I attacked.")
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
        else:
            self.andWait(0)
            print("I tried to move "+direction+" but couldn't.\r")
    def doMove(self, xdisplacement, ydisplacement):
        self.currentGrid.add(self, self.xpos+xdisplacement, self.ypos+ydisplacement)
        self.currentGrid.remove(self)
        self.xpos = self.xpos+xdisplacement
        self.ypos = self.ypos+ydisplacement
        self.andWait(3)
    def doAttack(self, xdisplacement, ydisplacement):
        sorted(self.currentGrid.get(self.xpos+xdisplacement, self.ypos+ydisplacement), reverse=True)[0].isAttacked(self)
        self.andWait(2)