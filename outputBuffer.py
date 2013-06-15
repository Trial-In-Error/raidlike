from unicurses import *

class OutputBuffer(): #rename outputManager?
    def __init__(self, cameraHeight):
        self.oBuffer = []
        self.cameraHeight = cameraHeight
    def add(self, string):
        self.oBuffer.append(string)
    def output(self):
        for stringCount, string in enumerate(self.oBuffer):
            mvaddstr(self.cameraHeight + stringCount, 0, str(string))
        self.clear()
    def clear(self):
        self.oBuffer = []