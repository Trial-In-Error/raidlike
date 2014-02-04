from levelManager import levelManager
import pickle

class worldManager():
	def __init__(self):
		self.levelOne = levelManager.load("level_mockup")
		self.levelTwo = levelManager.load("los_test")
		self.currentLevel = self.levelOne
		#levelList = {levelOne, levelTwo}
	def update(self):
		self.levelOne.update()
		#pass
	def menu(self):
		pass
	def renderMenu(self):
		pass
	def save(self):
		with open('./levels/original/io_test', mode='wb') as io_test:
		    a = pickle.dump(io_test)
	def load(self):
		with open('./levels/original/io_test', mode='rb') as io_test:
		    a = pickle.load(io_test)
		    for entry in self.__dict__:
		    	self.__dict__[entry] = a.__dict__[entry]

