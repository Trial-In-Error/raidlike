from entity import *

class Actor(Entity):
    def __init__(self, xpos, ypos, level, *, damage=1, health=3, moveCost=3,
                 **kwargs):
        defaults = {
            'description': "An actor. This shouldn't be instantiated!",
            'display': "x", # Perhaps this should be ("X", "cyan")
            'displayColor': "red",
            'displayPriority': 1,
            'memoryDisplayColor': "blue",
            'name': "actor",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        self.damage = damage
        self.health = health
        self.moveCost = moveCost # preferred spelling would be move_cost
        self.level.timeline.add(self)

    def act(self):
        pass

    def isAttacked(self, attacker):
        if(self.isHit(attacker)):
            self.takeDamage(attacker)

    def isHit(self, attacker):
        return(True)

    def takeDamage(self, attacker): #note: things only die if isDamaged
        self.health = self.health - attacker.damage
        if(self.health <= 0):
            self.die(attacker)
        else:
            self.level.currentOutputBuffer.add(attacker.name.capitalize() +
                " hit " + self.name + " for " +
            str(attacker.damage) + " damage.\r")

    def die(self, killer):
        self.level.currentOutputBuffer.add("AURGH! " + self.name.capitalize() + 
        " was killed by " + killer.name + ".\r")
        self.level.currentGrid.remove(self, self.xpos, self.ypos)
        self.level.timeline.remove(self)

    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0]}
        temp = []
        for entity in self.level.currentGrid.get(
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
        self.level.timeline.add(self, time)

    def doMove(self, xDiff, yDiff):
        self.level.currentGrid.add(self, self.xpos + xDiff, self.ypos + yDiff)
        self.level.currentGrid.remove(self, self.xpos, self.ypos)
        self.xpos = self.xpos + xDiff
        self.ypos = self.ypos + yDiff
        self.andWait(self.moveCost)

    def doAttack(self, xDiff, yDiff):
        sorted(self.level.currentGrid.get(self.xpos + xDiff, self.ypos + yDiff),
               reverse=True)[0].isAttacked(self)
        self.andWait(2)
