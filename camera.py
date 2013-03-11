class camera():
    def __init__(self, lensWidth, lensHeight, currentLevel):
        self.currentLevel = currentLevel
        self.lensWidth = lensWidth
        self.adjLensWidth = int((lensWidth/2))
        self.lensHeight = lensHeight
        self.adjLensHeight = int((lensHeight/2))
        self.grid = self.currentLevel.currentGrid
        self.player = self.currentLevel.currentPlayer
    def draw(self, xpos, ypos):
        for x in range(max(1,xpos-self.adjLensWidth), max(1,xpos+self.adjLensWidth + 1)):
            for y in range(max(1, ypos-self.adjLensWidth), min(ypos+self.adjLensHeight + 1, self.currentLevel.levelHeight + 1)):
                self.currentLevel.currentGrid.drawCell(x,y)

"""
How do do this...
Request that the player's square ask its width and height neighbors
to draw recursively. seek->draw->decrement. in the square case,
width = height.

spreadDraw(3,3,3)

"""