from actor import *

class Enemy(Actor):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'damage': 1,
            'description': "A generic enemy.",
            'display': "x", # Perhaps this should be ("X", "cyan")
            'displayColor': "red",
            'displayPriority': 1,
            'health': 3,
            'memoryDisplayColor': "blue",
            'moveCost': 3,
            'name': "generic enemy",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def act(self):
        xDiff = self.xpos - self.level.currentPlayer.xpos
        yDiff = self.ypos - self.level.currentPlayer.ypos
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

def Zombie(x, y, level):
    return Enemy(x, y, level, name="zombie", display='X', moveCost=8,
                 description="A lumbering zombie.")
