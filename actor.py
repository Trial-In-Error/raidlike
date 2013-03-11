from entity import *

class actor(entity):
    health = 1
    def __init__(self, xpos, ypos, currentLevel, display='~'):
        self.currentLevel = currentLevel
        self.currentGrid = currentLevel.currentGrid
        self.currentOutputBuffer = currentLevel.currentOutputBuffer
        self.xpos = xpos
        self.ypos = ypos
        self.name = "actor"
        self.displayColor = 4
        self.description = "An actor."
    def act(self):
        pass
    def isAttacked(self, attacker):
        if(self.isHit(attacker)):
            self.isDamaged(attacker)
    def isHit(self, attacker):
        return(True)
    def isDamaged(self, attacker): #note: things only die if isDamaged
        self.health = self.health - attacker.damage
        if(self.health <= 0):
            self.die(attacker)
        else:
            self.currentOutputBuffer.add(attacker.name.capitalize() +
                " hit " + self.name + " for " +
            str(attacker.damage) + " damage.\r")
    def die(self, killer):
        self.currentOutputBuffer.add("AURGH! " + self.name.capitalize() + 
        " was killed by " + killer.name + ".\r")
        self.currentGrid.remove(self, self.xpos, self.ypos)
        self.currentTimeLine.remove(self)
    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0]}
        temp = []
        for entity in self.currentGrid.get(
        self.xpos+moveDict[direction][0], 
        self.ypos+moveDict[direction][1]):
            temp.append(entity.collide())
        if(temp.count("true")==0
        and temp.count("combat_player")==0
        and temp.count("combat_enemy")==0):
            self.doMove(moveDict[direction][0], moveDict[direction][1])
        elif(temp.count("combat_player")==1):
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
        else:
            self.andWait(1)
    def andWait(self, time):
        self.currentTimeLine.add(self, time)
    def doMove(self, xDiff, yDiff):
        self.currentGrid.add(self, self.xpos + xDiff, self.ypos + yDiff)
        self.currentGrid.remove(self, self.xpos, self.ypos)
        self.xpos = self.xpos + xDiff
        self.ypos = self.ypos + yDiff
        self.andWait(3)
    def doAttack(self, xDiff, yDiff):
        sorted(self.currentGrid.get(self.xpos + xDiff, self.ypos + yDiff),
        reverse=True)[0].isAttacked(self)
        self.andWait(2)