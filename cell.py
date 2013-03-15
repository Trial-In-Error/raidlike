class cell():
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
        return sorted(self.contents)[0]
    def drawContents(self):
        self.hasBeenSeen = True
        self.getTopContent().draw()
    def drawContentsFromMemory(self):
        self.getBottomContent().drawFromMemory()
    def remove(self, value):
        self.contents.remove(value)
    def add(self, value):
        self.contents.append(value)