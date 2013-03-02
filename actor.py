from entity import *

class actor(entity):
    health = 1
    def __init__(self, xpos, ypos, currentGrid, currentTimeLine, display='~'):
        self.currentGrid = currentGrid
        self.xpos = xpos
        self.ypos = ypos
    def act(self):
        pass
    def isAttacked(self, attacker):
        if(self.isHit(attacker)):
            self.isDamaged(attacker)
    def isHit(self, attacker):
        return(True)
    def isDamaged(self, attacker):
        self.health = self.health - attacker.damage
        if(self.health <= 0):
            self.die()
    def die(self):
        self.currentGrid.remove(self)
        #for space in currentTimeLine
            #space.remove(self)
    def andWait(self, time):
        self.currentTimeLine.add(self, time)
        #self.currentTimeLine.remove(self)