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
    #currentPlayer = player(2,2,"a", "a")
    def __init__(self, playerSaveState):
        self.currentGrid = grid(self.levelWidth, self.levelHeight)
        self.populateWalls()
        self.populateFloor()
        self.currentPlayer = player(2,2,self.currentGrid, self.currentTimeLine)
        e1 = enemy(5,5,self)
        e2 = enemy(5,2,self)
        e3 = enemy(2,5,self)

    def load(self):
        pass
    def update(self):
        for actor in self.currentTimeLine:
            actor.act()
        self.currentTimeLine.progress()

    def draw(self):
        if (self.currentPlayer in self.currentTimeLine.line[self.currentTimeLine.currentLocation]):
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
    def populateFloor(self):
        for y in range(1, self.levelHeight+1):
            for x in range(1, self.levelWidth+1):
                if(self.currentGrid.get(x, y) == []):
                    self.currentGrid.add(entity(str(y), x, y), x, y)
    def populateWalls(self):
        for x in range(0, self.levelWidth):
            wall(x, 1, self.currentGrid)
            wall(x, self.levelHeight, self.currentGrid)
        for y in range(2, self.levelHeight):
            wall(1, y, self.currentGrid)
            wall(self.levelWidth, y, self.currentGrid)