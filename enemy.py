from actor import *

class enemy(actor):
    def __init__(self, xpos, ypos, currentGrid, display='x'):
        self.display=display
        self.displayPriority=1
        self.health = 5
        self.currentGrid = currentGrid
        self.xpos = xpos
        self.ypos = ypos
        self.currentGrid.add(self, self.xpos, self.ypos)
    def act(self):
        pass
    def collide(self):
        return "combat"