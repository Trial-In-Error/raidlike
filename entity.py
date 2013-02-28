class entity():
    xpos = 'null'
    ypos = 'null'
    def __init__(self, xpos, ypos, display='.'):
        self.display = display
        self.displayPriority = 0
    def __lt__(self, other):
        if(self.displayPriority < other.displayPriority):
            return True
        elif(self.displayPriority < other.displayPriority):
            return False
        #else:
            #raise CustomException #they're equal! D:
    def draw(self):
        return(self.display)
    def describe(self):
        pass
    def remove(self):
        pass
    def collide(self):
        return "false"

class wall(entity):
    def __init__(self, xpos, ypos, grid, display='#'):
        self.display=display
        self.displayPriority=1
        self.xpos=xpos
        self.ypos=ypos
        grid.add(self, xpos, ypos)
    def collide(self):
        return "true"