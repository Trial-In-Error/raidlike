from entity import *
from masterInputParser import *
from grid import *

class player(entity):
    #currentGrid = grid("foo",5,5)
    def __init__(self, xpos, ypos, currentGrid, display='@'):
        self.display = display
        self.displayPriority = 1
        self.damage = 1
        self.health = 5
        self.currentGrid = currentGrid
        self.xpos = xpos
        self.ypos = ypos
        self.currentGrid.add(self, self.xpos, self.ypos)
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
        print("I was asked to move "+direction+" "+str(moveDict[direction][0])+" "+str(moveDict[direction][1]))
        if(temp.count("true")==0 and temp.count("combat")==0):
            self.doMove(moveDict[direction][0], moveDict[direction][1])
        if(temp.count("combat")==1):
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
    def doMove(self, xdisplacement, ydisplacement):
        self.currentGrid.add(self, self.xpos+xdisplacement, self.ypos+ydisplacement)
        self.currentGrid.remove(self)
        self.xpos = self.xpos+xdisplacement
        self.ypos = self.ypos+ydisplacement
    def doAttack(self, xdisplacement, ydisplacement):
        sorted(self.currentGrid.get(self.xpos+xdisplacement, self.ypos+ydisplacement), reverse=True)[0].isAttacked(self)