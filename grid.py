import sys
from entity import Wall

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

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.grid = [[Cell(x,y,self) for x in range(width)] for y in range(height)]

    def __iter__(self):
        #goes row by row, starting at bottom left as per get/set ^> coordinates
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
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
        return self.grid[self.height-ypos][xpos-1]

    def add(self, value, xpos, ypos):
        self.getCell(xpos, ypos).add(value)

    def remove(self, value, xpos, ypos):
        self.getCell(xpos, ypos).remove(value)

    def clear(self): #rewrite using iterator and .get
        for y in range(1, self.height):
            for x in range(1, self.width):
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

    def clearLine(self, player_xpos, player_ypos, xpos, ypos):
        if xpos == player_xpos:
            for cell in range(min(player_ypos, ypos), max(player_ypos, ypos)):
                if type(self.getCell(xpos, cell).getBottomContent()) is Wall:
                    return False
        if ypos == player_ypos:
            for cell in range(min(player_xpos, xpos), max(player_xpos, xpos)):
                if type(self.getCell(cell, ypos).getBottomContent()) is Wall:
                    return False
            pass
        return True

    def spreadDraw(self, xpos, ypos, player_xpos, player_ypos, width, height, direction="all"):
        # invert spread/move dict's names
        moveDict = {'north': [0, 1, 0, -1, "north", "northeast", "northwest"],
                    'south': [0, -1, 0, -1, "south", "southeast", "southwest"],
                    'west': [-1, 0, -1, 0, "west", "northwest", "southwest"],
                    'east': [1, 0, -1, 0, "east", "northeast", "southeast"],
                    'northwest': [-1, 1, -1, -1, "north", "west", "northwest"],
                    'northeast': [1, 1, -1, -1, "north", "east", "northeast"],
                    'southwest': [-1 ,-1, -1, -1, "south", "west", "southwest"],
                    'southeast': [1, -1, -1, -1, "south", "east", "southeast"]}
        orthogonals = ['north',
                       'south',
                       'west',
                       'east']
        diagonals = ['northwest',
                     'northeast',
                     'southwest',
                     'southeast']
        """
        if direction=="all":
            for direction in orthogonals + diagonals:
                self.grid.drawCell(xpos, ypos)
                new_xpos = self.xpos + moveDict[direction][0]
                new_ypos = self.ypos + moveDict[direction][1]
                self.grid.get(new_xpos, new_ypos).spreadDraw(width+moveDict[2],
                height+moveDict[3], direction)
        """
        if direction=="all":
            player_xpos = xpos
            player_ypos = ypos
            self.drawCell(xpos, ypos)
            for direction in orthogonals + diagonals:
                new_xpos = xpos + moveDict[direction][0]
                new_ypos = ypos + moveDict[direction][1]
                if(new_xpos > 0 and new_xpos < self.width+1 and new_ypos > 0 and new_ypos < self.height+1):
                    self.spreadDraw(new_xpos, new_ypos, player_xpos, player_ypos, width+moveDict[direction][2],
                    height+moveDict[direction][3], direction)
        else:
            self.drawCell(xpos, ypos)
            if(type(self.getCell(xpos, ypos).getBottomContent()) is not Wall):
                if direction in diagonals:
                    for newDirection in moveDict[direction][4:]:
                        new_xpos = xpos + moveDict[newDirection][0]
                        new_ypos = ypos + moveDict[newDirection][1]
                        if(new_xpos>0 and new_xpos<=self.width and new_ypos>0 and new_ypos<=self.height):
                            if(width+moveDict[direction][2] > 0 and height+moveDict[direction][3] > 0):
                                self.spreadDraw(new_xpos, new_ypos, player_xpos, player_ypos, width+moveDict[direction][2],
                                height+moveDict[direction][3], newDirection)
                if direction in orthogonals:

                    for newDirection in moveDict[direction][4:]:
                        new_xpos = xpos + moveDict[newDirection][0]
                        new_ypos = ypos + moveDict[newDirection][1]
                        if(new_xpos>0 and new_xpos<=self.width and new_ypos>0 and new_ypos<=self.height):
                            if(width+moveDict[direction][2] > 0 and height+moveDict[direction][3] > 0):
                                if(newDirection in orthogonals):
                                    self.spreadDraw(new_xpos, new_ypos, player_xpos, player_ypos, width+moveDict[direction][2],
                                    height+moveDict[direction][3], newDirection)
                                else:
                                    if(self.clearLine(player_xpos, player_ypos, new_xpos, new_ypos)):
                                        self.spreadDraw(new_xpos, new_ypos, player_xpos, player_ypos, 1,
                                        1, newDirection)

class Cell():
    def __init__(self, xpos, ypos, grid):
    # probably doesn't need access to grid
        self.grid = grid
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
