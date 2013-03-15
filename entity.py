from unicurses import *

class entity():
    def __init__(self, xpos, ypos, currentLevel, display='.'):
        self.currentLevel = currentLevel
        self.currentGrid = currentLevel.currentGrid
        self.display = display
        self.displayPriority = 0
        self.xpos = xpos
        self.ypos = ypos
        self.name = 'floor'
        self.displayColor = "yellow"
        self.memoryDisplayColor = "blue"
        self.currentGrid.add(self, xpos, ypos)
        self.description = "A floor."
    def __lt__(self, other):
        if(self.displayPriority < other.displayPriority):
            return True
        elif(self.displayPriority < other.displayPriority):
            return False
        #else:
            #raise CustomException #they're equal! D:
    def draw(self):
        attron(COLOR_PAIR(self.currentLevel.colorDict[self.displayColor][0]))
        mvaddch(self.currentLevel.levelHeight-self.ypos, self.xpos-1, self.display)
        attroff(COLOR_PAIR(self.currentLevel.colorDict[self.displayColor][0]))
    def drawFromMemory(self):
        attron(COLOR_PAIR(self.currentLevel.colorDict[self.memoryDisplayColor][0]))
        mvaddch(self.currentLevel.levelHeight-self.ypos, self.xpos-1, self.display)
        attroff(COLOR_PAIR(self.currentLevel.colorDict[self.memoryDisplayColor][0]))
    def describe(self):
        return(self.description)
    def remove(self):
        pass
    def collide(self):
        return "false"

class wall(entity):
    def __init__(self, xpos, ypos, currentLevel, display='#'):
        super().__init__(xpos, ypos, currentLevel, display='#')
        self.name = 'wall'
        self.displayPriority=1
        self.displayColor = "cyan"
        self.description = "A wall."
        self.memoryDisplayColor = "blue"
    def collide(self):
        return "true"