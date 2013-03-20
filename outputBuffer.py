from unicurses import *

class OutputBuffer(): #rename outputManager?
    def __init__(self, levelHeight):
        self.oBuffer = []
        self.levelHeight = levelHeight
    def add(self, string):
        self.oBuffer.append(string)
    def output(self):
        for stringCount, string in enumerate(self.oBuffer):
            mvaddstr(self.levelHeight+stringCount, 0, str(string))
        self.oBuffer = []
    def clear(self):
        self.oBuffer = []