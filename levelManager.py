from grid import *
from timeLine import *
from entity import *
from enemy import *
from player import *

class levelManager():
    currentTimeLine = timeLine(16)
    viewDistance = 3;
    levelWidth = 7;
    levelHeight = 7;
    def __init__(self, playerSaveState):
        self.currentGrid = grid(self.levelWidth, self.levelHeight)
        currentPlayer = player(2,2,self.currentGrid)
        for y in range(1, self.levelHeight+1):
            for x in range(1, self.levelWidth+1):
                self.currentGrid.add(entity(str(y), x, y), x, y)
        self.currentTimeLine.add(currentPlayer)
        e1 = enemy(3,3,self.currentGrid)
        for x in range(0,self.levelWidth+1):
            wall(x, 1, self.currentGrid)
            wall(x, self.levelHeight, self.currentGrid)
        for y in range(1, self.levelHeight):
            wall(1, y, self.currentGrid)
            wall(self.levelWidth, y, self.currentGrid)


    def load(self):
        pass
    def update(self):
        for actor in self.currentTimeLine:
            actor.act() 

    def draw(self):
        temp = []
        temp2 = ""
        for square in self.currentGrid:
            try:
                temp2 += str(sorted(square, reverse=True)[0].draw())
            except IndexError:
                print("Some cell is completely empty.")
                #raise IndexError("Some cell is completely empty.")
                temp2 += "?"
                #we could fill it with a floor tile entity!
        for y in reversed(range(0, self.levelHeight)):
            print(temp2[y*self.levelWidth:(y+1)*self.levelWidth], end="\r\n")