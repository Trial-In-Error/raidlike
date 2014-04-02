"""
A data structure for managing a game timeline.
Conceptually a circular buffer, where each cell in the buffer
is a list.

Data is added to the currentLocation's list.
Progressing clears the currentLocation's list.
Thus, the workflow is as such:
    for element in currentLocation:
        1. operate on element
        2. add element to when it gets its next turn
    progress()

Note that the first turn, t=0, should have every actor
initialized in it before it begins operating.

Newly iterable. Iteration goes through all cells in
currentLocation.
"""

class Timeline():
    currentLocation = 0
    line = []
    absoluteTime = 0
    iterator = 0
    def __init__(self, size):
        self.size = size
        self.line = [[] for x in range(0, size)]
        self.absoluteTime = 0
    def __iter__(self):
        iterator = 0
        while(iterator < len(self.line[self.currentLocation])):
            try:
                result = self.line[self.currentLocation][iterator]
            except IndexError:
                raise StopIteration
            yield result
            iterator += 1
    def lengthen(self):
        self.size = self.size+1
        self.line.append([])
    def add(self, object, displacement = 0):
        displacement = (self.currentLocation + displacement) % self.size
        self.line[displacement].append(object)
    def addToTop(self, object, displacement = 0):
        displacement = (self.currentLocation + displacement) % self.size
        self.line[displacement].insert(0, object)
    def get(self):
        return self.line[self.currentLocation]
    def clear(self, displacement = 0):
        self.line[self.currentLocation+displacement] = []
    def progress(self, displacement = 1):
        displacement = (self.currentLocation + displacement) % self.size
        self.line[self.currentLocation] = []
        self.currentLocation = displacement
        self.absoluteTime = self.absoluteTime + displacement
        iterator = 0
    def delay(self, object, displacement = 0):
        self.remove(object)
        self.add(object, displacement)
    def remove(self, object):
        for quantum in self.line:
            for entry in quantum:
                if entry == object:
                    quantum.remove(object)
