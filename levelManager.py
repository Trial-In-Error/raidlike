from grid import Grid
from timeline import Timeline
from entity import *
from outputBuffer import OutputBuffer
from camera import Camera
import unicurses
import os
import os.path
import sys

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
        self.width = width
        self.height = height
        self.grid = Grid(width, height)
        self.player = Player
        self.camera = Camera(width,height,self)
        self.output_buffer = OutputBuffer(self.camera.lensHeight)



        #these should be in entity, not levelmanager...
        self.coloringDict = {"enemy":"yellow"}
        self.colorDict = {"yellow":[1, unicurses.COLOR_YELLOW, unicurses.COLOR_BLACK],
            "cyan":[2, unicurses.COLOR_CYAN, unicurses.COLOR_BLACK],
            "red":[3, unicurses.COLOR_RED, unicurses.COLOR_BLACK],
            "white":[4, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK],
            "blue":[5, unicurses.COLOR_BLUE, unicurses.COLOR_BLACK]
            }
        for entry in self.colorDict:
            unicurses.init_pair(self.colorDict[entry][0], self.colorDict[entry][1], self.colorDict[entry][2])

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
            glyph, name, args = map(str.strip, line.split(':'))
            args = args.split(',')
            argLeft = []
            argRight = []
            for arg in args:
                if arg:
                    argLeft.append(arg.split('=')[0])
                    argRight.append(arg.split('=')[1])
                    #    except:
                    #        raise IndexError("\n"+str(arg)+"\n"+str(argLeft)+"\n"+str(argRight))
            args = {}
            #for arg, index in argLeft, range(0,argLeft):
            #    args[argLeft[index]] = argRight[index]
            for index in range(len(argLeft)):
                args[argLeft[index].strip()] = argRight[index].strip()
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
        print("level width={} height={}".format(width, height), file=sys.stderr)
        for y, line in enumerate(map_[::-1], 1):
            for x, char in enumerate(line, 1):
                if char != ' ':
                    if class_dict[char] is Player:
                        level.setPlayer(Player(x, y, level))
                        classes["floor"](x, y, level)
                    else:
                        if class_dict[char] in (Wall, Floor):
                            #print("adding {} at x={} y={}".format(class_dict[char], x, y), file=sys.stderr)
                            class_dict[char](x, y, level, **arg_dict[char])
                        else:
                            class_dict[char](x, y, level, **arg_dict[char])
                            classes["floor"](x, y, level)
        # Triggers ...?
        return level

    def setPlayer(self, player):
        self.player = player

    def update(self):
        for actor in self.timeline:
            actor.act()
        self.timeline.progress()

    def draw(self):
        if self.player is None:
            raise RuntimeError("You didn't call levelManager.setPlayer()!!!!")
        unicurses.erase()
        #self.drawHUD()
        self.camera.draw(self.player.xpos, self.player.ypos)
        #self.drawHUD()
        self.output_buffer.output()

    def drawLookInputParser(self, xpos, ypos): #actually xlook, ylook
        if(self.grid.getCell(xpos,ypos).hasBeenSeen):
            self.grid.drawCellBold(xpos, ypos, self.player.xpos, self.player.ypos, int(self.camera.lensWidth/2), int(self.camera.lensHeight/2))
        else:
            #self.grid.drawCellBold(xpos, ypos, self.player.xpos, self.player.ypos, int(self.camera.lensWidth/2), int(self.camera.lensHeight/2))
            self.camera.drawArbitrary(xpos, ypos, '*', 'blue')
        #self.output_buffer.add("Press z to inspect the current object or q to stop looking.")

    def populateFloor(self):
        for y in range(1, self.height+1):
            for x in range(1, self.width+1):
                if all(not isinstance(i, Wall)
                       for i in self.grid.get(x, y)):
                    #for debugging, use below to print column/row indices
                    #entity(x, y, self, str(y))
                    Floor(x, y, self, display='.')

    def populateWalls(self):
        for x in range(1, self.width+1):
            Wall(x, 1, self)
            Wall(x, self.height, self)
        for y in range(2, self.height):
            Wall(1, y, self)
            Wall(self.width, y, self)
