from levelManager import levelManager
import pickle
import config
import religion

class worldManager():
    """
    The entire game world as one class. Primarily exists to ease saving and
    loading via pickle and to store a mapping of level names to levelManagers.

    Most probable point of failure involves not properly setting currentLevel.
    """
    
    def __init__(self):
        self.throneRoom = levelManager.load("throne_room")
        self.slaversOne = levelManager.load("slavers_floor_one")
        self.slaversTwo = levelManager.load("slavers_floor_two")
        self.slaversBasement = levelManager.load("slavers_basement")
        #self.levelTwo.camera.lineOfSight = 5
        self.currentLevel = self.slaversOne
        config.player = self.currentLevel.player
        self.pantheon = religion.Pantheon()
        self.levelDict = {
            'throneRoom' : self.throneRoom,
            'slaversOne' : self.slaversOne,
            'slaversTwo' : self.slaversTwo,
            'slaversBasement' : self.slaversBasement
        }

        #CHANGE THIS LATER
        config.player.worshipping = self.pantheon.Brand
    def update(self):
        self.currentLevel.update()
    def menu(self):
        pass
    def renderMenu(self):
        pass
    def save(self):
        with open('./levels/save', mode='wb') as io_test:
            a = pickle.dump(self, io_test)
    def load(self):
        # wrap this in a try / catch block!
        with open('./levels/save', mode='rb') as io_test:
            a = pickle.load(io_test)
            for entry in self.__dict__:
                self.__dict__[entry] = a.__dict__[entry]
    def player_pos(self):
        return [self.currentLevel.player.xpos, self.currentLevel.player.ypos]
    def swapLevels(self, portalInc):
            # clear the output buffer
            config.player.level.output_buffer.clear()
            self.levelDict[portalInc.toWhichLevel].timeline.absoluteTime = self.currentLevel.timeline.absoluteTime
            # remove player from old level
            config.player = self.currentLevel.player
            # DESCRIPTIVE TEXT GOES HERE
            self.currentLevel.grid.remove(config.player, config.player.xpos, config.player.ypos)
            self.currentLevel.timeline.remove(config.player)
            self.currentLevel.player = config.player
            # swap control to the new level
            self.currentLevel = self.levelDict[portalInc.toWhichLevel]
            config.player.level = self.currentLevel
            self.currentLevel.setPlayer(config.player)
            # place player in new level
            for portal in self.currentLevel.portalList:
                if(portal.internalName == portalInc.toWhichPortal):
                    self.currentLevel.grid.add(config.player, portal.xpos + config.directions[portal.direction][0], portal.ypos + config.directions[portal.direction][1])
                    self.currentLevel.player = config.player
                    self.currentLevel.player.xpos = portal.xpos + config.directions[portal.direction][0]
                    self.currentLevel.player.ypos = portal.ypos + config.directions[portal.direction][1]
                    self.currentLevel.camera.player = config.player
                    #self.currentLevel.draw()
                    self.currentLevel.timeline.addToTop(config.player)
            #    else:
            #        raise IndexError

    def swapViaDeath(self, obelisk):
            # remove player from old level
            config.player = self.currentLevel.player
            if(self.currentLevel.player.level == obelisk.level):
                self.currentLevel.timeline.remove(self.currentLevel.player)
                self.currentLevel.player.andWait(0)
            else:
                obelisk.level.timeline.addToTop(config.player)
                self.currentLevel.timeline.remove(config.player)
            # DESCRIPTIVE TEXT GOES HERE
            self.currentLevel.grid.remove(config.player, config.player.xpos, config.player.ypos)
            self.currentLevel.player = config.player
            # swap control to the new level
            self.currentLevel = obelisk.level
            config.player.level = self.currentLevel
            self.currentLevel.setPlayer(config.player)
            # place player in new level
            self.currentLevel.grid.add(config.player, obelisk.xpos + config.directions[obelisk.exitDirection][0], obelisk.ypos + config.directions[obelisk.exitDirection][1])
            self.currentLevel.player = config.player
            config.player.xpos = obelisk.xpos + config.directions[obelisk.exitDirection][0]
            config.player.ypos = obelisk.ypos + config.directions[obelisk.exitDirection][1]
            self.currentLevel.camera.player = config.player