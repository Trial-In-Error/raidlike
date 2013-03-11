from unicurses import *

class entity():
    def __init__(self, xpos, ypos, currentLevel, display='.'):
        self.currentLevel = currentLevel
        self.display = display
        self.displayPriority = 0
        self.xpos = xpos
        self.ypos = ypos
        self.name = 'floor'
        self.displayColor = 1
        self.memoryDisplayColor = 5
        self.currentLevel.currentGrid.add(self, xpos, ypos)
        self.description = "A floor."
    def __lt__(self, other):
        if(self.displayPriority < other.displayPriority):
            return True
        elif(self.displayPriority < other.displayPriority):
            return False
        #else:
            #raise CustomException #they're equal! D:
    def draw(self):
        attron((COLOR_PAIR(self.displayColor)))
        mvaddch(self.currentLevel.levelHeight-self.ypos, self.xpos-1, self.display)
        attroff(COLOR_PAIR(self.displayColor))
    def drawFromMemory(self):
        attron((COLOR_PAIR(self.memoryDisplayColor)))
        mvaddch(self.currentLevel.levelHeight-self.ypos, self.xpos-1, self.display)
        attroff(COLOR_PAIR(self.memoryDisplayColor))
    def describe(self):
        return(self.description)
    def remove(self):
        pass
    def collide(self):
        return "false"

class wall(entity):
    def __init__(self, xpos, ypos, currentLevel, display='#'):
        self.name = 'wall'
        self.display=display
        self.displayPriority=1
        self.xpos=xpos
        self.ypos=ypos
        self.currentLevel = currentLevel
        self.currentLevel.currentGrid.add(self, xpos, ypos)
        self.displayColor = 2
        self.description = "A wall."
        self.memoryDisplayColor = 5
    def collide(self):
        return "true"