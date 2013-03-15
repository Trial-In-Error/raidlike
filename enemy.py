from actor import *

class enemy(actor):
    def __init__(self, xpos, ypos, currentLevel, display='x'):
        super().__init__(xpos, ypos, currentLevel)
        self.display = 'x'
        self.health = 3
        self.damage = 1
        self.currentOutputBuffer = currentLevel.currentOutputBuffer
        self.name = "generic enemy"
        self.displayColor = "red"
        self.description = "A generic enemy."
        self.memoryDisplayColor = "blue"
        self.moveCost = 3
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
    def collide(self):
        return "combat_enemy"

class zombie(enemy):
    def __init__(self, xpos, ypos, currentLevel, display='X'):
        super().__init__(xpos,ypos,currentLevel)
        self.display='X'
        self.health = 3
        self.damage = 1
        self.currentOutputBuffer = currentLevel.currentOutputBuffer
        self.name = "zombie"
        self.displayColor = "cyan"
        self.description = "A lumbering zombie."
        self.memoryDisplayColor = "blue"
        self.moveCost = 8
        self.display = 'X'