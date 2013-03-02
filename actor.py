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
        print("ARURURUGH!")
        self.currentGrid.remove(self)
        self.currentTimeLine.remove(self)
    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0]}
        temp = []
        for entity in list(self.currentGrid.get(self.xpos+moveDict[direction][0], self.ypos+moveDict[direction][1])):
            temp.append(entity.collide())
        if(temp.count("true")==0 and temp.count("combat")==0):
            self.doMove(moveDict[direction][0], moveDict[direction][1])
        elif(temp.count("combat")==1):
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
        else:
            self.andWait(1)
    def andWait(self, time):
        self.currentTimeLine.add(self, time)
        #self.currentTimeLine.remove(self)
    def doMove(self, xdisplacement, ydisplacement):
        self.currentGrid.add(self, self.xpos+xdisplacement, self.ypos+ydisplacement)
        self.currentGrid.remove(self)
        self.xpos = self.xpos+xdisplacement
        self.ypos = self.ypos+ydisplacement
        self.andWait(3)
    def doAttack(self, xdisplacement, ydisplacement):
        sorted(self.currentGrid.get(self.xpos+xdisplacement, self.ypos+ydisplacement), reverse=True)[0].isAttacked(self)
        self.andWait(2)