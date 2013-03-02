from actor import *

class enemy(actor):
    def __init__(self, xpos, ypos, currentLevel, display='x'):
        self.currentLevel = currentLevel
        self.display=display
        self.displayPriority=1
        self.health = 3
        self.damage = 1
        self.currentGrid = currentLevel.currentGrid
        self.xpos = xpos
        self.ypos = ypos
        self.currentGrid.add(self, self.xpos, self.ypos)
        self.currentTimeLine = currentLevel.currentTimeLine
        self.currentTimeLine.add(self)
    def act(self):
        xDiff = self.xpos - self.currentLevel.currentPlayer.xpos
        yDiff = self.ypos - self.currentLevel.currentPlayer.ypos
        if(abs(xDiff) >= abs(yDiff)):
            if(xDiff >= 0):
                self.move("west")
            else:
                self.move("east")
        elif(yDiff >= 0):
            self.move("south")
        else:
            self.move("north")
        #self.move("north")
    def collide(self):
        return "combat_enemy"