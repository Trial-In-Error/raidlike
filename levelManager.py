from grid import Grid
from timeline import Timeline
from entity import *
from outputBuffer import OutputBuffer
from camera import Camera
import unicurses
import os
import os.path
import sys
import pickle
import config

class levelManager():
    """
    The workhorse of the game engine. It update()s every
    iteration of the main while loop. Every update act()s
    for every actor in that quantum of the timeline. It
    also contains the draw() function, which is called
    as the first part of the player's act() and which
    draw()s and clear()s the output_buffer.

    The player must always be initialized last, or else
    enemies will appear to double-move on the first
    turn. It looks really awkward.
    """

    def __init__(self, playerSaveState, width, height, player=None):
        self.width = width
        self.height = height
        self.grid = Grid(width, height)
        self.player = Player
        self.camera = Camera(51, 19, self)
        self.output_buffer = OutputBuffer(self.camera.lensHeight)
        self.timeline = Timeline(16)
        self.portalList = []
        self.triggerTileList = []

        #not used
        self.viewDistance = 3

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
        arg_dict = {}
        for line in (g for g in glyphs if g.strip()):
            glyph, name, args = map(str.strip, line.split('::'))
            args = args.split(',,')
            argLeft = []
            argRight = []
            for arg in args:
                if arg:
                    argLeft.append(arg.split('==')[0])
                    try:
                        argRight.append(arg.split('==')[1])
                    except IndexError:
                        raise IndexError("\n"+str(arg)+"\n"+str(argLeft)+"\n"+str(argRight))
            args = {}
            #for arg, index in argLeft, range(0,argLeft):
            #    args[argLeft[index]] = argRight[index]
            for index in range(len(argLeft)):
                args[argLeft[index].strip()] = argRight[index].strip()
            #for argument in argRight:
            #    if "[" in argument:
            #        argument = eval(argument)
            try:
                class_dict[glyph] = classes[name]
            except KeyError:
                raise KeyError("Error parsing glyph {!r}: no class named {}"
                               "".format(glyph, name))
            arg_dict[glyph] = args
        # Parse the map
        map_ = [line.rstrip() for line in map_data.rstrip().split('\n')]
        width = max(len(line) for line in map_)
        height = len(map_)
        # Create the level instance

        level = levelManager("blah", width, height)
        #print("level width={} height={}".format(width, height), file=sys.stderr)
        for y, line in enumerate(map_[::-1], 1):
            for x, char in enumerate(line, 1):
                if char != ' ':
                    #try: #this almost works, but I don't have a python resource at hand
                        if class_dict[char] is Player:
                            level.setPlayer(Player(x, y, level))
                            level.camera.player = level.player
                            class_dict["."](x, y, level, **arg_dict["."])
                        else:
                            # automatically places floors under all non-floor, non-wall, non-triggertile tiles! 
                            if class_dict[char] in (Wall, Floor, TriggerTile, Door):
                                #print("adding {} at x={} y={}".format(class_dict[char], x, y), file=sys.stderr)
                                try:
                                    class_dict[char](x, y, level, **arg_dict[char])
                                except TypeError:
                                    raise TypeError("Error parsing glyph {!r}: no class named {}"
                                                    "".format(char, arg_dict[char]))
                            else:
                                class_dict[char](x, y, level, **arg_dict[char])
                                class_dict["."](x, y, level, **arg_dict["."])
                    #except:
                        #raise(KeyError ("There isn't a matching line for glyph: ", char))
        # Triggers ...?
        return level

    def setPlayer(self, player):
        self.player = player

    def update(self):
        if(config.world.currentLevel == self):
            for actor in self.timeline:
                actor.act()
            self.timeline.progress()
        else:
            config.world.currentLevel.timeline.addToTop(config.player)
            config.world.update()

    def draw(self):
        if self.player is None:
            raise RuntimeError("You didn't call levelManager.setPlayer()!!!!")
        if(config.world.currentLevel == self):
            unicurses.erase()
            self.camera.draw(self.player.xpos, self.player.ypos)
            self.output_buffer.output()

    def drawDropInputParser(self):
        self.drawInventoryInputParser()

    def drawInventoryInputParser(self):
        unicurses.erase()
        for index, item in enumerate(self.player.inventory.inventoryList):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict["white"]))
            unicurses.mvaddstr(index, 0, self.player.inventory.letterList[index+1]+") "+self.player.inventory.inventoryList[index].description)
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict["white"]))

    def drawLookInputParser(self, xLook, yLook):
        if(self.grid.getCell(xLook, yLook).hasBeenSeen):
            self.grid.drawCellBold(xLook, yLook, self.player.xpos, self.player.ypos, int(self.camera.lensWidth/2), int(self.camera.lensHeight/2))
        elif (abs(xLook - self.player.xpos) < self.camera.adjLensWidth) and abs(self.player.ypos-yLook) < self.camera.adjLensHeight:
            self.camera.drawArbitrary(xLook, yLook, '*', 'blue')

    def populateFloor(self):
        for y in range(1, self.height+1):
            for x in range(1, self.width+1):
                if all((not isinstance(i, Wall) and (not isinstance(i, TriggerTile))) for i in self.grid.get(x, y)):
                    #for debugging, use below to print column/row indices
                    #entity(x, y, self, str(y))
                    #if(not isinstance(i, TriggerTile)):
                    Floor(x, y, self, display='.')

    def populateWalls(self):
        for x in range(1, self.width+1):
            Wall(x, 1, self)
            Wall(x, self.height, self)
        for y in range(2, self.height):
            Wall(1, y, self)
            Wall(self.width, y, self)