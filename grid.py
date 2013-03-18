import sys

class Grid():
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

    def __init__(self, levelWidth, levelHeight):
        self.levelHeight = levelHeight
        self.levelWidth = levelWidth
        self.grid = [[Cell(x,y,self) for x in range(levelWidth)] for y in range(levelHeight)]

    def __iter__(self):
        #goes row by row, starting at bottom left as per get/set ^> coordinates
        for y in range(1, self.levelHeight + 1):
            for x in range(1, self.levelWidth + 1):
                try:
                    result = self.getCell(x, y)
                except IndexError:
                    print("INDEXXXXX at x={} and y={}".format(x, y))
                    raise StopIteration
                yield result

    def get(self, xpos, ypos):
        return self.getCell(xpos,ypos).getContents()

    def getCell(self, xpos, ypos):
        #print('\n'.join(' '.join(str(cell.getTopContent()) if len(cell.getContents()) > 0 else ' ' for cell in line) for line in self.grid), file=sys.stderr)
        return self.grid[self.levelHeight-ypos][xpos-1]

    def add(self, value, xpos, ypos):
        self.getCell(xpos, ypos).add(value)

    def remove(self, value, xpos, ypos):
        self.getCell(xpos, ypos).remove(value)

    def clear(self): #rewrite using iterator and .get
        for y in range(1, self.levelHeight):
            for x in range(1, self.levelWidth):
                self.getCell(x, y).clear()

    def clearCell(self, xpos, ypos):
        self.getCell(xpos,ypos).clear()

    def load(self):
        pass

    def drawCell(self, xpos, ypos):
        try:
            self.getCell(xpos,ypos).drawContents()
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
        orthogonals = ['north',
                       'south,',
                       'west',
                       'east']
        diagonals = ['northwest',
                     'northeast',
                     'southwest',
                     'southeast']
        if direction=="all":
            for direction in orthogonals + diagonals:
                self.currentGrid.get(self.xpos+moveDict[direction][0],
                self.ypos+moveDict[direction][1]).spreadDraw(width+moveDict[2],
                height+moveDict[3], direction).draw()
        else:
            if direction in diagonals:
                for newDirection in moveDict[direction][4:]:
                    self.currentGrid.get(self.xpos+moveDict[newDirection][0],
                    self.ypos+moveDict[newDirection][1]).spreadDraw(width+moveDict[2],
                    height+moveDict[3], newDirection).draw()
            if direction in orthogonals:
                self.currentGrid.get(self.xpos+moveDict[direction][0],
                self.ypos+moveDict[direction][1]).spreadDraw(width+moveDict[2],
                height+moveDict[3], direction).draw()

class Cell():
    def __init__(self, xpos, ypos, currentGrid):
    # probably doesn't need access to currentGrid
        self.currentGrid = currentGrid
        self.xpos = xpos
        self.ypos = ypos
        self.contents = []
        self.hasBeenSeen = False

    def clear(self):
        self.contents = []

    def getContents(self):
        return self.contents

    def getTopContent(self):
        return sorted(self.contents, reverse=True)[0]

    def getBottomContent(self):
        try:
            return sorted(self.contents)[0]
        except IndexError:
            pass

    def drawContents(self):
        self.hasBeenSeen = True
        self.getTopContent().draw()

    def drawContentsFromMemory(self):
        try:
            self.getBottomContent().drawFromMemory()
        except AttributeError:
            pass

    def remove(self, value):
        self.contents.remove(value)

    def add(self, value):
        self.contents.append(value)
