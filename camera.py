import unicurses

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
            for ypos in range(min(self.lensHeight,player_ypos - self.adjLensHeight), min(self.lensHeight+1, player_ypos + self.adjLensHeight)):
                try:
                    if(self.level.grid.getCell(xpos, ypos).hasBeenSeen):
                        self.level.grid.drawCellRelativeFromMemory(xpos, ypos, player_xpos, player_ypos, self.adjLensWidth, self.adjLensHeight)
                except IndexError:
                    pass

    def drawArbitrary(self, xpos, ypos, display, displayColor):
        #xpos = self.level.player.xpos+1
        #ypos = self.level.player.ypos+1
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict[displayColor][0]))
        unicurses.mvaddch(-ypos+2*self.level.player.ypos-self.adjLensHeight+1, xpos-self.level.player.xpos+self.adjLensWidth, display)
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict[displayColor][0]))