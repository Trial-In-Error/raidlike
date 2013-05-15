class Camera():
    def __init__(self, lensWidth, lensHeight, level):
        self.level = level
        self.lensWidth = lensWidth
        self.adjLensWidth = int((lensWidth/2))
        self.lensHeight = lensHeight
        self.adjLensHeight = int((lensHeight/2))
        self.grid = self.level.grid
        self.player = self.level.player
    def draw(self, xpos, ypos): #these are actually the player positions!
        self.drawFromMemory(xpos, ypos)
        #for x in range(max(1,xpos-self.adjLensWidth), max(1,xpos+self.adjLensWidth + 1)):
        #    for y in range(max(1, ypos-self.adjLensWidth), min(ypos+self.adjLensHeight + 1, self.level.height + 1)):
        #        self.grid.drawCell(x,y)
        self.level.grid.spreadDraw(self.level.player.xpos, self.level.player.ypos,
        5, 5, self.adjLensWidth, self.adjLensHeight)
    def drawFromMemory(self, player_xpos, player_ypos):
        for xpos in range(player_xpos - self.adjLensWidth, player_xpos + self.adjLensWidth):
            for ypos in range(player_ypos - self.adjLensHeight, player_ypos + self.adjLensHeight):
                #self.level.output_buffer.add(xpos+", "+ypos+"\r")
                #system.quit()
                try:
                    if(self.level.grid.getCell(xpos, ypos).hasBeenSeen):
                        self.level.grid.drawCellRelativeFromMemory(xpos, ypos, player_xpos, player_ypos, self.lensWidth, self.lensHeight)
                except IndexError:
                    pass
        #for cell in self.grid:
        #    if cell.hasBeenSeen:
        #        cell.drawContentsFromMemory(cell.xpos, cell.ypos)
        #self.level.grid.spreadDraw(self.level.player.xpos, self.level.player.ypos,
        #self.adjLensWidth, self.adjLensHeight, self.adjLensWidth, self.adjLensHeight)
        pass
"""
How do do this...
Request that the player's square ask its width and height neighbors
to draw recursively. seek->draw->decrement. in the square case,
width = height.

spreadDraw(3,3,3)

"""
