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
    def draw(self, player_xpos, player_ypos):
        self.drawFromMemory(player_xpos, player_ypos)
        self.level.grid.spreadDraw(player_xpos, player_ypos, 5, 5, self.adjLensWidth, self.adjLensHeight)
        self.drawHUD()

    def drawFromMemory(self, player_xpos, player_ypos):
        for xpos in range(max(1, player_xpos - self.adjLensWidth), max(1,player_xpos + self.adjLensWidth)):
            for ypos in range(min(self.lensHeight,player_ypos - self.adjLensHeight), min(self.lensHeight+1, player_ypos + self.adjLensHeight)):
                try:
                    if(self.level.grid.getCell(xpos, ypos).hasBeenSeen and abs(player_xpos - xpos) < self.adjLensWidth and abs(player_ypos - ypos) < self.adjLensHeight):
                        self.level.grid.drawCellRelativeFromMemory(xpos, ypos, player_xpos, player_ypos, self.adjLensWidth, self.adjLensHeight)
                except IndexError:
                    pass

    def drawArbitrary(self, xpos, ypos, display, displayColor):
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict[displayColor][0]))
        unicurses.mvaddch(-ypos+self.level.player.ypos +self.adjLensHeight, xpos-self.level.player.xpos+self.adjLensWidth, display)
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict[displayColor][0]))

    def drawHUD(self):
        if self.player is None:
            raise RuntimeError("You didn't call levelManager.setPlayer()!!!!")
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict["white"][0]))
        unicurses.mvaddstr(1, self.lensWidth, self.level.player.playerName)
        unicurses.mvaddstr(2, self.lensWidth, self.level.player.className)
        unicurses.mvaddstr(3, self.lensWidth, "Health: "+str(self.level.player.health))
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict["white"][0]))
        self.drawHUDBoundaries()

    def drawHUDBoundaries(self):
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict["white"][0]))
        for ypos in range(0,self.lensHeight):
            unicurses.mvaddch(ypos, self.lensWidth-1, "|")
            unicurses.mvaddch(ypos, 0, "|")
        for xpos in range(0,self.lensWidth):
            unicurses.mvaddch(0, xpos, "-")
            unicurses.mvaddch(self.lensHeight-1, xpos, "-")
        for ypos in range(0, self.lensHeight):
            unicurses.mvaddch(ypos, self.lensWidth+15, "|")
        for xpos in range(self.lensWidth, self.lensWidth+16):
            unicurses.mvaddch(0, xpos, "-")
            unicurses.mvaddch(self.lensHeight-1, xpos, "-")
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict["white"][0]))