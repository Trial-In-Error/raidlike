import unicurses
import config

class OutputBuffer(): #rename outputManager?
    def __init__(self, cameraHeight):
        self.oBuffer = []
        self.cameraHeight = cameraHeight
    def add(self, string):
        self.oBuffer.append([string, "white"])
    def add_formatted(self, inTuple):
        self.oBuffer.append(inTuple)
    def output(self):
         for tupleCount, inTuple in enumerate(self.oBuffer):
            unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[inTuple[1]]))
            unicurses.mvaddstr(self.cameraHeight + tupleCount, 0, str(inTuple[0]))
            unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[inTuple[1]]))
        self.clear()
    def clear(self):
        self.oBuffer = []