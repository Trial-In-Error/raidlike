import unicurses
from masterInputParser import masterInputParser
from sys import exit

class Entity():
    def __init__(self, xpos, ypos, level, *,
                 description="A floor.",
                 display='.',
                 displayColor="yellow",
                 displayPriority=0,
                 memoryDisplayColor="blue",
                 name="floor"):
        self.xpos = xpos
        self.ypos = ypos
        self.level = level
        self.description = description
        self.display = display
        self.displayColor = displayColor
        self.displayPriority = displayPriority
        self.memoryDisplayColor = memoryDisplayColor
        self.name = name
        self.level.currentGrid.add(self, xpos, ypos)

    def __lt__(self, other):
        if self.displayPriority < other.displayPriority:
            return True
        else:
            return False

    def draw(self):
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict[self.displayColor][0]))
        unicurses.mvaddch(self.level.levelHeight-self.ypos, self.xpos-1, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict[self.displayColor][0]))
    def drawFromMemory(self):
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict[self.memoryDisplayColor][0]))
        unicurses.mvaddch(self.level.levelHeight-self.ypos, self.xpos-1, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict[self.memoryDisplayColor][0]))
    def describe(self):
        return(self.description)
    def remove(self):
        pass
    def collide(self):
        return "false"
    def __str__(self):
        return self.display

Floor = Entity

class Wall(Entity):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'description': "A wall.",
            'display': '#',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'wall',
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def collide(self):
        return "true"

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

class Player(Actor):
    def __init__(self, xpos, ypos, level, *, playerName=None, className=None,
                 **kwargs):
        defaults = {
            'damage': 1,
            'description': "It's you.",
            'display': '@',
            'displayColor': "white",
            'displayPriority': 1,
            'health': 10,
            'moveCost': 3,
            'name': "player",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        #default name/class
        self.className = "Blessed of Kaia"
        self.playerName = "Roderick"

    def act(self):
        self.level.draw()
        masterInputParser(self, self.level)

    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0],
                    'northwest': [-1, 1],
                    'northeast': [1, 1],
                    'southwest': [-1 ,-1],
                    'southeast': [1, -1]}
        temp = []
        for entity in self.level.currentGrid.get(self.xpos + moveDict[direction][0],
        self.ypos + moveDict[direction][1]):
            temp.append(entity.collide())
        if(temp.count("true")==0 and temp.count("combat_enemy")==0):
            self.doMove(moveDict[direction][0], moveDict[direction][1])
        elif(temp.count("combat_enemy")==1):
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
        else:
            self.andWait(0)

    def collide(self):
        return "combat_player"

    def die(self, killer):
        self.level.currentOutputBuffer.clear()
        self.level.currentOutputBuffer.add("You died! Game over.")
        self.level.draw()
        unicurses.getch()
        unicurses.clear()
        unicurses.refresh()
        unicurses.endwin()
        print("Be seeing you...")
        exit()

class Enemy(Actor):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'damage': 1,
            'description': "A generic enemy.",
            'display': "x", # Perhaps this should be ("X", "cyan")
            'displayColor': "red",
            'displayPriority': 1,
            'health': 3,
            'memoryDisplayColor': "blue",
            'moveCost': 3,
            'name': "generic enemy",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def act(self):
        xDiff = self.xpos - self.level.currentPlayer.xpos
        yDiff = self.ypos - self.level.currentPlayer.ypos
        if(abs(xDiff) >= abs(yDiff)):
            if(xDiff >= 0):
                self.move("west")
            else:
                self.move("east")
        elif(yDiff >= 0):
            self.move("south")
        else:
            self.move("north")

    def collide(self):
        return "combat_enemy"

def Zombie(x, y, level):
    return Enemy(x, y, level, name="zombie", display='X', moveCost=8,
                 description="A lumbering zombie.")
