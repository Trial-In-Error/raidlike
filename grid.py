class grid():
    def __init__(self, levelWidth, levelHeight):
        self.levelHeight = levelHeight
        self.levelWidth = levelWidth
        self.grid = [[[] for i in range(levelWidth)] for x in range(levelHeight)]
    def __iter__(self):
        xIterator = 1
        yIterator = 1
        #goes row by row, starting at bottom left as per get/set ^> coordinates
        while(yIterator <= self.levelHeight):
            xIterator = 1
            while(xIterator <= self.levelWidth):
                try:
                    result = self.get(xIterator, yIterator)
                except IndexError:
                    print("INDEXXXXX at x= "+xIterator+" and y= "+xIterator)
                    raise StopIteration
                yield result
                xIterator += 1
            yIterator += 1
    def get(self, xpos, ypos):
        return self.grid[xpos-1][self.levelHeight-ypos]
    def add(self, value, xpos, ypos):
        self.grid[xpos-1][self.levelHeight-ypos].append(value)
    def remove(self, value): #uses ^> coordinates
        self.grid[value.xpos-1][self.levelHeight-value.ypos].remove(value)
    def clear(self):
        for y in range(1, self.levelHeight):
            for x in range(1, self.levelWidth):
                self.grid[x-1][self.levelHeight-y] = []
    def clearCell(self, xpos, ypos):
        self.grid[xpos-1][self.levelHeight-ypos] = []
    def load(self):
        pass