from unicurses import *

class Entity():
    def __init__(self, xpos, ypos, level, *,
                 description="A floor.",
                 display='.',
                 displayColor="yellow",
                 displayPriority=0,
                 memoryDisplayColor="blue",
                 name="floor"):
        self.xpos = xpos
        self.ypos = ypos
        self.level = level
        self.description = description
        self.display = display
        self.displayColor = displayColor
        self.displayPriority = displayPriority
        self.memoryDisplayColor = memoryDisplayColor
        self.name = name
        self.level.currentGrid.add(self, xpos, ypos)

    def __lt__(self, other):
        if self.displayPriority < other.displayPriority:
            return True
        else:
            return False

    def draw(self):
        attron(COLOR_PAIR(self.level.colorDict[self.displayColor][0]))
        mvaddch(self.level.levelHeight-self.ypos, self.xpos-1, self.display)
        attroff(COLOR_PAIR(self.level.colorDict[self.displayColor][0]))
    def drawFromMemory(self):
        attron(COLOR_PAIR(self.level.colorDict[self.memoryDisplayColor][0]))
        mvaddch(self.level.levelHeight-self.ypos, self.xpos-1, self.display)
        attroff(COLOR_PAIR(self.level.colorDict[self.memoryDisplayColor][0]))
    def describe(self):
        return(self.description)
    def remove(self):
        pass
    def collide(self):
        return "false"

class Wall(Entity):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'description': "A wall.",
            'display': '#',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'wall',
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def collide(self):
        return "true"
