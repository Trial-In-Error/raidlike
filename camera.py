class Camera():
    def __init__(self, lensWidth, lensHeight, level):
        self.level = level
        self.lensWidth = lensWidth
        self.adjLensWidth = int((lensWidth/2))
        self.lensHeight = lensHeight
        self.adjLensHeight = int((lensHeight/2))
        self.grid = self.level.grid
        self.player = self.level.player
    def draw(self, player_xpos, player_ypos): #these are actually the player positions!
        self.drawFromMemory(player_xpos, player_ypos)
        self.level.grid.spreadDraw(player_xpos, player_ypos, 5, 5, self.adjLensWidth, self.adjLensHeight)
    def drawFromMemory(self, player_xpos, player_ypos):
        for xpos in range(max(1, player_xpos - self.adjLensWidth), max(1,player_xpos + self.adjLensWidth)):
            for ypos in range(min(self.lensHeight,player_ypos - self.adjLensHeight), min(self.lensHeight,player_ypos + self.adjLensHeight)):
                #self.level.output_buffer.add(xpos+", "+ypos+"\r")
                #system.quit()
                try:
                    if(self.level.grid.getCell(xpos, ypos).hasBeenSeen):
                        #pass
                        self.level.grid.drawCellRelativeFromMemory(xpos, ypos, player_xpos, player_ypos, self.adjLensWidth, self.adjLensHeight)
                except IndexError:
                    pass
        #for cell in self.grid:
        #    if cell.hasBeenSeen:
        #        cell.drawContentsFromMemory(cell.xpos, cell.ypos)
        #self.level.grid.spreadDraw(self.level.player.xpos, self.level.player.ypos,
        #self.adjLensWidth, self.adjLensHeight, self.adjLensWidth, self.adjLensHeight)
        #pass
