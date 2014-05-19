import sys
from entity import Wall, Item, Portal, Door, Key, Obelisk

class Grid():
    """
    A data structure for managing a game grid.
    Conceptually a one-indexed grid, with the origin in the
    lower left. Thus, the bottom leftmost corner is (1, 1),
    and the top rightmost corner is (max, max).

    All addresses to the grid should be made in this coordinate
    system; it does conversions to the array innately.

    Iterable; iteration goes through every cell and
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
        if(xpos <= 0 or ypos <= 0):
            raise IndexError
        return self.getCell(xpos,ypos).getContents()

    def getCell(self, xpos, ypos):
        return self.grid[self.height-ypos][xpos-1]

    def add(self, value, xpos, ypos):
        self.getCell(xpos, ypos).add(value)

    def remove(self, value, xpos, ypos):
        self.getCell(xpos, ypos).remove(value)

    def clear(self):
        for y in range(1, self.height):
            for x in range(1, self.width):
                self.getCell(x, y).clear()

    def clearCell(self, xpos, ypos):
        self.getCell(xpos,ypos).clear()

    def load(self):
        pass

    def drawCellRelative(self, xpos, ypos, player_xpos, player_ypos, lensWidth, lensHeight):
        try:
            self.getCell(xpos,ypos).drawContentsRelative(player_xpos, player_ypos, lensWidth, lensHeight)
        except IndexError:
            pass

    def drawCellBold(self, xpos, ypos, player_xpos, player_ypos, lensWidth, lensHeight):
        try:
            self.getCell(xpos,ypos).drawContentsBold(player_xpos, player_ypos, lensWidth, lensHeight)
        except IndexError:
            pass

    def drawCellRelativeFromMemory(self, xpos, ypos, player_xpos, player_ypos, lensWidth, lensHeight):
        try:
            self.getCell(xpos,ypos).drawContentsRelativeFromMemory(player_xpos, player_ypos, lensWidth, lensHeight)
        except IndexError:
            pass

    def checkForDoubles(self):
        for element in self:
            if(len(element.contents)>1):
                print("Double at:" +str(element[0].xpos)+", " + str(element[0].ypos))

    def getItem(self, xpos, ypos):
        return self.getCell(xpos, ypos).getItem() 

    def dropItem(self, xpos, ypos, item):
        item.xpos = xpos
        item.ypos = ypos
        self.getCell(xpos, ypos).dropItem(item)               

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

    def spreadDraw(self, xpos, ypos, width, height, lensWidth, lensHeight, direction="all"):
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
        directions = diagonals + orthogonals
        if direction=="all":
            player_xpos = xpos
            player_ypos = ypos
            self.drawCellRelative(xpos, ypos, xpos, ypos, lensWidth, lensHeight)
            for direction in (diagonals + orthogonals):
                new_xpos = xpos + moveDict[direction][0]
                new_ypos = ypos + moveDict[direction][1]
                if(new_xpos>0 and new_xpos<=self.width and new_ypos>0 and new_ypos<=self.height): #necessary?
                    if direction in orthogonals:
                        self.spreadPrimeOrthogonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, width, height, moveDict, lensWidth, lensHeight)
                    if direction in diagonals:
                        self.spreadDiagonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, width, height, moveDict, lensWidth, lensHeight)

    def spreadOrthogonal(self,xpos, ypos, player_xpos, player_ypos, direction, width, height, moveDict, lensWidth, lensHeight):
        #MOVE THIS CODE TO GRID/CELL
        temp = []
        for entity in self.level.grid.get(xpos, ypos):
            temp.append(entity.collide())
        if(temp.count("vision_block")>0 or temp.count("true")>0 or temp.count("closed_door")>0):
            return
        self.drawCellRelative(xpos, ypos, player_xpos, player_ypos, lensWidth, lensHeight)
        temp = self.getCell(xpos, ypos).getBottomContent()
        if((type(temp) is not Wall and type(temp) is not Door) or (type(temp) is Wall and temp.collideType=="see_through")
            or (type(temp) is Door and temp.collideType=="open_door")):
            #and (type(self.getCell(xpos, ypos).getBottomContent()) is not Door or self.getCell(xpos, ypos).getBottomContent().collideType == closed_door)
            #or (type(self.getCell(xpos, ypos).getBottomContent()) is Wall
            #    and self.getCell(xpos, ypos).getBottomContent().collideType=="see_through")):
        #THIS LINE
                new_xpos = xpos + moveDict[direction][0]
                new_ypos = ypos + moveDict[direction][1]
                if(new_xpos>0 and new_xpos<=self.width and new_ypos>0 and new_ypos<=self.height): #necessary?
                    if(width+moveDict[direction][2] > 0 and height+moveDict[direction][3] > 0):
                        if(direction in ["north", "west", "east", "south"]):
                            self.spreadOrthogonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, width+moveDict[direction][2], height+moveDict[direction][3], moveDict, lensWidth, lensHeight)
                        else:
                            self.spreadDiagonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, width, height, moveDict, lensWidth, lensHeight)

    def spreadDiagonal(self, xpos, ypos, player_xpos, player_ypos, direction, width, height, moveDict, lensWidth, lensHeight):
        try:
            self.drawCellRelative(xpos, ypos, player_xpos, player_ypos, lensWidth, lensHeight)
            temp = self.getCell(xpos, ypos).getBottomContent()
            if(not temp.collideType["blocksLoS"]):
                for newDirection in moveDict[direction][4:]:
                    new_xpos = xpos + moveDict[newDirection][0]
                    new_ypos = ypos + moveDict[newDirection][1]
                    if(new_xpos>0 and new_xpos<=self.width and new_ypos>0 and new_ypos<=self.height): #necessary?
                        if(width+moveDict[direction][2] > 0 and height+moveDict[direction][3] > 0): #ND??
                            if(direction in ["north", "west", "east", "south"]):
                                self.spreadOrthogonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, width+moveDict[direction][2], height+moveDict[direction][3], moveDict, lensWidth, lensHeight)
                            else:
                                self.spreadDiagonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, width+moveDict[direction][2], height+moveDict[direction][3], moveDict, lensWidth, lensHeight)
        except IndexError:
            pass

    def spreadPrimeOrthogonal(self,xpos, ypos, player_xpos, player_ypos, direction, width, height, moveDict, lensWidth, lensHeight):
        try:
            self.drawCellRelative(xpos, ypos, player_xpos, player_ypos, lensWidth, lensHeight)
            temp = self.getCell(xpos, ypos).getBottomContent()
            if(not temp.collideType["blocksLoS"]):
                for newDirection in moveDict[direction][4:]:
                    new_xpos = xpos + moveDict[newDirection][0]
                    new_ypos = ypos + moveDict[newDirection][1]
                    if(new_xpos>0 and new_xpos<=self.width and new_ypos>0 and new_ypos<=self.height): #necessary?
                        if(width+moveDict[direction][2] > 0 and height+moveDict[direction][3] > 0):
                            if(direction == newDirection):
                                self.spreadPrimeOrthogonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, width+moveDict[direction][2], height+moveDict[direction][3], moveDict, lensWidth, lensHeight)
                            else:
                                #check for clearLine(player_xpos, player_ypos, xpos, ypos)?
                                self.spreadDiagonal(new_xpos, new_ypos, player_xpos, player_ypos, direction, 1, 1, moveDict, lensWidth, lensHeight)
        except IndexError:
            pass



class Cell():
    def __init__(self, xpos, ypos, grid):
    # probably doesn't need access to grid
        self.grid = grid
        self.xpos = xpos
        self.ypos = ypos
        self.gridxpos = self.xpos+1
        self.gridypos = self.grid.height-ypos
        self.contents = []
        self.hasBeenSeen = False

    def clear(self):
        self.contents = []

    def getContents(self):
        return self.contents

    def getTopContent(self):
        try:
            return sorted(self.contents, reverse=True)[0]
        except IndexError:
            raise RuntimeError("Attempted to get top content, but there's an empty cell at: ("+str(self.gridxpos)+", "+str(self.gridypos)+").")

    def getBottomContent(self):
        try:
            #if there exists a portal, return it?
            for element in self.contents:
                if(type(element) == Portal or type(element) == Item or type(element) == Obelisk
                    or type(element) == Key):
                    return element
            return sorted(self.contents)[0]
        except IndexError:
            raise RuntimeError("Attempted to get bottom content, but there's an empty cell at: ("+str(self.gridxpos)+", "+str(self.gridypos)+").")

    def drawContentsRelative(self, player_xpos, player_ypos, lensWidth, lensHeight):
        self.hasBeenSeen = True
        self.getTopContent().drawRelative(player_xpos, player_ypos, lensWidth, lensHeight)

    def drawContentsRelativeFromMemory(self, player_xpos, player_ypos, lensWidth, lensHeight):
        try:
            self.getBottomContent().drawRelativeFromMemory(player_xpos, player_ypos, lensWidth, lensHeight)
        except AttributeError:
            pass

    def remove(self, value):
        self.contents.remove(value)

    def add(self, value):
        self.contents.append(value)

    def getItem(self):
        for element in self.contents:
            if(isinstance(element, Item)):
                self.contents.remove(element)
                return element

    def dropItem(self, item):
        self.contents.append(item)
        self.contents = sorted(self.contents)

    def drawContentsBold(self, player_xpos, player_ypos, lensWidth, lensHeight):
        self.getTopContent().drawRelativeBold(player_xpos, player_ypos, lensWidth, lensHeight)