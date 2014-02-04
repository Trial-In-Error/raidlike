from levelManager import levelManager
import pickle

class worldManager():
	def __init__(self):
		self.levelOne = levelManager.load("level_mockup")
		self.levelTwo = levelManager.load("los_test")
		self.currentLevel = self.levelOne
		self.levelDict = {
			'one' : self.levelOne,
			'two' : self.levelTwo,
		}
	def update(self):
		self.currentLevel.update()
		#pass
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
