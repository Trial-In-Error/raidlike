from grid import Grid
from timeline import Timeline
from entity import *
from enemy import *
from player import *
from outputBuffer import *
from camera import *
import os
import os.path

class levelManager():
    """
    The workhorse of the game engine. It updates() every
    iteration of the main while loop. Every update act()s
    for every actor in that quantum of the timeline. It
    also contains the draw() function, which is called
    as the first part of the player's act().

    Currently, the __init__() is taking the place of
    load(), because there is no data structure in place
    for loading levels.

    The player must always be initialized last, or else
    the enemies will appear to double-move on the first
    turn. It looks really awkward.
    """

    timeline = Timeline(16)
    viewDistance = 3

    def __init__(self, playerSaveState, width, height, player=None):
        self.levelWidth = width
        self.levelHeight = height
        self.currentGrid = Grid(width, height)
        self.currentOutputBuffer = outputBuffer(height)
        self.currentPlayer = player
        self.currentCamera = camera(5,5,self)
        #these should be in entity, not levelmanager...
        self.coloringDict = {"enemy":"yellow"}
        self.colorDict = {"yellow":[1, COLOR_YELLOW, COLOR_BLACK],
            "cyan":[2, COLOR_CYAN, COLOR_BLACK],
            "red":[3, COLOR_RED, COLOR_BLACK],
            "white":[4, COLOR_WHITE, COLOR_BLACK],
            "blue":[5, COLOR_BLUE, COLOR_BLACK]
            }
        for entry in self.colorDict:
            init_pair(self.colorDict[entry][0], self.colorDict[entry][1], self.colorDict[entry][2])

    @staticmethod
    def load(name):
        filename = os.path.join('levels', name + '.txt')
        with open(filename, encoding='utf-8') as f:
            data = f.read()
        map_data, not_map = data.split('Glyphs')
        glyphs_data, triggers_data = not_map.split('Triggers')
        datas = (glyphs_data, triggers_data)
        glyphs, triggers = [d.strip().split('\n') for d in datas]
        # Load the glyphs
        import entity
        classes = {name.lower(): getattr(entity, name) for name in dir(entity)
                                                       if name[0].isupper()}
        class_dict = {}
        for line in (g for g in glyphs if g.strip()):
            glyph, name = map(str.strip, line.split(':'))
            try:
                class_dict[glyph] = classes[name]
            except KeyError:
                raise KeyError("Error parsing glyph {!r}: no class named {}"
                               "".format(glyph, name))
        # Parse the map
        map_ = [line.rstrip() for line in map_data.rstrip().split('\n')]
        width = max(len(line) for line in map_)
        height = len(map_)
        # Create the level instance

        level = levelManager("blah", width, height)
        print("level width={} height={}".format(width, height), file=sys.stderr)
        for y, line in enumerate(map_[::-1], 1):
            for x, char in enumerate(line, 1):
                if char != ' ':
                    if class_dict[char] is Player:
                        level.setPlayer(Player(x, y, level))
                    else:
                        print("adding {} at x={} y={}".format(class_dict[char], x, y), file=sys.stderr)
                        class_dict[char](x, y, level)
        # Triggers ...?
        return level

    def setPlayer(self, player):
        self.currentPlayer = player

    def update(self):
        for actor in self.timeline:
            actor.act()
        self.timeline.progress()

    def draw(self):
        if self.currentPlayer is None:
            raise RuntimeError("You didn't call levelManager.setPlayer()!!!!")
        clear()
        self.drawHUD()
        self.currentCamera.draw(self.currentPlayer.xpos, self.currentPlayer.ypos)
        self.currentOutputBuffer.output()

    def drawHUD(self):
        if self.currentPlayer is None:
            raise RuntimeError("You didn't call levelManager.setPlayer()!!!!")
        attron(COLOR_PAIR(self.colorDict["white"][0]))
        mvaddstr(0, self.levelWidth, self.currentPlayer.playerName)
        mvaddstr(1, self.levelWidth, self.currentPlayer.className)
        mvaddstr(2, self.levelWidth, "Health: "+str(self.currentPlayer.health))
        attroff(COLOR_PAIR(self.colorDict["white"][0]))

    def populateFloor(self):
        for y in range(1, self.levelHeight+1):
            for x in range(1, self.levelWidth+1):
                if all(not isinstance(i, Wall)
                       for i in self.currentGrid.get(x, y)):
                    #for debugging, use below to print column/row indices
                    #entity(x, y, self, str(y))
                    Entity(x, y, self, display='.')

    def populateWalls(self):
        for x in range(1, self.levelWidth+1):
            Wall(x, 1, self)
            Wall(x, self.levelHeight, self)
        for y in range(2, self.levelHeight):
            Wall(1, y, self)
            Wall(self.levelWidth, y, self)
