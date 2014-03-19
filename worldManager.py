from levelManager import levelManager
import pickle
import config

class worldManager():
	"""
	The entire game world as one class. Primarily exists to ease saving and
	loading via pickle and to store a mapping of level names to levelManagers.

	Most probable point of failure involves not properly setting currentLevel.
	"""
	
	def __init__(self):
		#self.levelOne = levelManager.load("level_mockup")
		#self.levelTwo = levelManager.load("los_test")
		self.throneRoom = levelManager.load("throne_room")
		self.jailCellOne = levelManager.load("jail_floor_one")
		self.jailCellTwo = levelManager.load("jail_floor_two")
		#self.levelTwo.camera.lineOfSight = 5
		self.currentLevel = self.jailCellOne
		self.pantheon = None
		self.levelDict = {
			#'one' : self.levelOne,
			'throneRoom' : self.throneRoom,
			'jailCellOne' : self.jailCellOne,
			'jailCellTwo' : self.jailCellTwo,
		}
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
		with open('./levels/save', mode='rb') as io_test:
		    a = pickle.load(io_test)
		    for entry in self.__dict__:
		    	self.__dict__[entry] = a.__dict__[entry]

	def swapLevels(self, portalInc):
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


