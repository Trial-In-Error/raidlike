"""
A data structure for managing a game grid.
Conceptually a one-indexed grid, with the origin in the
lower left. Thus, the bottom leftmost corner is (1, 1),
and the top rightmost corner is (max, max).

All addresses to the grid should be made in this coordinate
system; it does conversions to the array innately.

Newly iterable. Iteration goes through every cell and
returns the whole list of data in each cell, starting
at the bottom left and moving row by row.
"""

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
                    print("INDEXXXXX at x= "+str(xIterator)+" and y= "+str(xIterator))
                    raise StopIteration
                yield result
                xIterator += 1
            yIterator += 1
    def get(self, xpos, ypos):
        return self.grid[xpos-1][self.levelHeight-ypos]
    def getTop(self, xpos, ypos):
        return sorted(self.grid[xpos-1][self.levelHeight-ypos], reverse=True)[0]
    def add(self, value, xpos, ypos):
        self.grid[xpos-1][self.levelHeight-ypos].append(value)
    def remove(self, value):
        self.grid[value.xpos-1][self.levelHeight-value.ypos].remove(value)
    def clear(self):
        for y in range(1, self.levelHeight):
            for x in range(1, self.levelWidth):
                self.grid[x-1][self.levelHeight-y] = []
    def clearCell(self, xpos, ypos):
        self.grid[xpos-1][self.levelHeight-ypos] = []
    def load(self):
        pass
    def doubleCheck(self):
        for element in self:
            if(len(element)>1):
                print("Double at:" +str(element[0].xpos)+", " + str(element[0].ypos))