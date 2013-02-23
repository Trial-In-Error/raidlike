from entity import *
from masterInputParser import *

class player(entity):
	def __init__(self, display='@'):
		self.display = display
	def act(self):
		masterInputParser()
	def doMove(self):
		pass