class Camera():
    def __init__(self, lensWidth, lensHeight, level):
        self.level = level
        self.lensWidth = lensWidth
        self.adjLensWidth = int((lensWidth/2))
        self.lensHeight = lensHeight
        self.adjLensHeight = int((lensHeight/2))
        self.grid = self.level.grid
        self.player = self.level.player
    def draw(self, xpos, ypos):
        self.drawFromMemory()
        #for x in range(max(1,xpos-self.adjLensWidth), max(1,xpos+self.adjLensWidth + 1)):
        #    for y in range(max(1, ypos-self.adjLensWidth), min(ypos+self.adjLensHeight + 1, self.level.height + 1)):
        #        self.grid.drawCell(x,y)
        self.level.grid.spreadDraw(self.level.player.xpos, self.level.player.ypos, self.level.player.xpos, self.level.player.ypos, 5, 5)
    def drawFromMemory(self):
        for cell in self.grid:
            if cell.hasBeenSeen:
                cell.drawContentsFromMemory()

"""
How do do this...
Request that the player's square ask its width and height neighbors
to draw recursively. seek->draw->decrement. in the square case,
width = height.

spreadDraw(3,3,3)

"""
