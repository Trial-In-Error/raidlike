import unicurses
import config

class Camera():
    def __init__(self, lensWidth, lensHeight, level):
        self.level = level
        self.lensWidth = lensWidth
        self.adjLensWidth = int((lensWidth/2))
        self.lensHeight = lensHeight
        self.adjLensHeight = int((lensHeight/2))
        self.hudWidth = 25
        try:
            self.grid = self.level.grid
        except AttributeError:
            pass
        try:
            self.player = self.level.player
        except AttributeError:
            pass
        self.lineOfSight = 5

    def isInView(self, xpos, ypos):
        if(xpos > (self.player.xpos - self.adjLensWidth) and
            xpos < self.player.xpos + self.adjLensWidth and
            ypos > self.player.ypos - self.adjLensHeight and
            ypos < self.player.ypos + self.adjLensHeight):
            return True
        else:
            return False

    def draw(self, player_xpos, player_ypos):
        self.drawFromMemory(player_xpos, player_ypos)
        self.level.grid.spreadDraw(player_xpos, player_ypos, self.lineOfSight, self.lineOfSight, self.adjLensWidth, self.adjLensHeight)
        self.drawHUD()

    def drawFromMemory(self, player_xpos, player_ypos):
        for xpos in range(max(1, player_xpos - self.adjLensWidth), min(self.level.width+1, player_xpos + self.adjLensWidth)):
            for ypos in range(max(1, player_ypos - self.adjLensHeight), min(self.level.height+1, player_ypos + self.adjLensHeight)):
                try:
                    if(self.level.grid.getCell(xpos, ypos).hasBeenSeen
                        and (max(player_xpos - xpos, 0) < self.adjLensWidth)
                        and (max(ypos - player_ypos, 0) < self.adjLensHeight)):
                        self.level.grid.drawCellRelativeFromMemory(xpos, ypos, player_xpos, player_ypos, self.adjLensWidth, self.adjLensHeight)
                except IndexError:
                    pass

    def drawArbitrary(self, xpos, ypos, display, displayColor):
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[displayColor]))
        unicurses.mvaddch(-ypos+self.level.player.ypos +self.adjLensHeight, xpos-self.level.player.xpos+self.adjLensWidth, display)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[displayColor]))

    def drawHUD(self):
        if self.player is None:
            raise RuntimeError("You didn't call levelManager.setPlayer()!!!!")
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"]))
        unicurses.mvaddstr(1, self.lensWidth, self.level.player.playerName)
        unicurses.mvaddstr(2, self.lensWidth, self.level.player.title)
        unicurses.mvaddstr(3, self.lensWidth, "Health: "+str(self.level.player.health))
        unicurses.mvaddstr(4, self.lensWidth, "Shards of Divinity: "+str(self.player.shardCount))
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"]))
        self.drawHUDBoundaries()

    def drawHUDBoundaries(self):
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"]))
        for ypos in range(0, self.lensHeight):
            unicurses.mvaddch(ypos, self.lensWidth-1, "|")
            unicurses.mvaddch(ypos, 0, "|")
        for xpos in range(0, self.lensWidth):
            unicurses.mvaddch(0, xpos, "-")
            unicurses.mvaddch(self.lensHeight-1, xpos, "-")
        for ypos in range(0, self.lensHeight):
            unicurses.mvaddch(ypos, self.lensWidth+self.hudWidth, "|")
        for xpos in range(self.lensWidth, self.lensWidth+self.hudWidth+1):
            unicurses.mvaddch(0, xpos, "-")
            unicurses.mvaddch(self.lensHeight-1, xpos, "-")
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"]))