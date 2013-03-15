from cell import *

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
        self.grid = [[cell(i,x,self) for i in range(levelWidth)] for x in range(levelHeight)]
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
        return self.getCell(xpos,ypos).getContents()
    def getCell(self, xpos, ypos):
        return self.grid[xpos-1][self.levelHeight-ypos]
    def add(self, value, xpos, ypos):
        self.getCell(xpos, ypos).add(value)
    def remove(self, value, xpos, ypos):
        self.getCell(xpos, ypos).remove(value)
    def clear(self): #rewrite using iterator and .get
        for y in range(1, self.levelHeight):
            for x in range(1, self.levelWidth):
                self.grid[x-1][self.levelHeight-y].clear()
    def clearCell(self, xpos, ypos):
        self.getCell(xpos,ypos).clear()
    def load(self):
        pass
    def drawCell(self, xpos, ypos):
        try:
            self.getCell(xpos,ypos).drawContents()
        except IndexError:
            pass
    def DrawCellFromMemory(self, xpos, ypos):
        if(self.getCell(xpos,ypos).hasBeenSeen):
            try:
                self.getCell(xpos,ypos).drawContentsFromMemory()
            except IndexError:
                pass
    def checkForDoubles(self):
        for element in self:
            if(len(element.contents)>1):
                print("Double at:" +str(element[0].xpos)+", " + str(element[0].ypos))
    def spreadDraw(self, width, height, direction="any"):
        # invert spread/move dict's names
        moveDict = {'north': [0, 1, 0, -1],
                    'south': [0, -1, 0, -1],
                    'west': [-1, 0, -1, 0],
                    'east': [1, 0, -1, 0],
                    'northwest': [-1, 1, -1, -1, "north", "west", "northwest"],
                    'northeast': [1, 1, -1, -1, "north", "east", "northeast"],
                    'southwest': [-1 ,-1, -1, -1, "south", "west", "southwest"],
                    'southeast': [1, -1, -1, -1, "south", "east", "southeast"]}
        spreadDict = ['north',
                      'south,',
                      'west',
                      'east',
                      'northwest',
                      'northeast',
                      'southwest',
                      'southeast']
        if(direction=="all"):
            for direction in spreadDict: 
                self.currentGrid.get(self.xpos+moveDict[direction][0],
                self.ypos+moveDict[direction][1]).spreadDraw(width+moveDict[2],
                height+moveDict[3], direction).draw()
        else:
            if(direction in spreadDict[4:]):
                for newDirection in moveDict[direction][4:]:
                    self.currentGrid.get(self.xpos+moveDict[newDirection][0],
                    self.ypos+moveDict[newDirection][1]).spreadDraw(width+moveDict[2],
                    height+moveDict[3], newDirection).draw()
            if(direction in spreadDict[:4]):
                self.currentGrid.get(self.xpos+moveDict[direction][0],
                self.ypos+moveDict[direction][1]).spreadDraw(width+moveDict[2],
                height+moveDict[3], direction).draw()                
