import unicurses
from masterInputParser import masterInputParser
from sys import exit
from inventory import Inventory

class Entity():
    def __init__(self, xpos, ypos, level, *,
                 description="A floor.",
                 display='.',
                 displayColor="yellow",
                 displayPriority=1,
                 memoryDisplayColor="blue",
                 name="floor", collideType="false"):
        self.xpos = xpos
        self.ypos = ypos
        self.level = level
        self.description = description
        self.display = display
        self.displayColor = displayColor
        self.displayPriority = displayPriority
        self.memoryDisplayColor = memoryDisplayColor
        self.name = name
        self.level.grid.add(self, xpos, ypos)

    def __lt__(self, other):
        if self.displayPriority < other.displayPriority:
            return True
        else:
            return False

    def drawRelative(self, player_xpos, player_ypos, lensWidth, lensHeight):
        #TO CHANGE THE WAY COLOR DICT WORKS, REMOVE self.level.colorDict TO SELF.COLORDICT
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict[self.displayColor][0]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict[self.displayColor][0]))

    def drawRelativeBold(self, player_xpos, player_ypos, lensWidth, lensHeight):
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict[self.displayColor][0]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display, unicurses.A_REVERSE)
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict[self.displayColor][0]))

    def drawRelativeFromMemory(self,player_xpos, player_ypos, lensWidth, lensHeight):
        unicurses.attron(unicurses.COLOR_PAIR(self.level.colorDict[self.memoryDisplayColor][0]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(self.level.colorDict[self.memoryDisplayColor][0]))

    def describe(self):
        return self.description

    def collide(self):
        return self.collideType

    def __str__(self):
        return self.display

class Actor(Entity):
    def __init__(self, xpos, ypos, level, *, collideType="actor", attackCost=2, damage=1, health=3, moveCost=3,
                 **kwargs):
        defaults = {
            'description': "An actor. This shouldn't be instantiated!",
            'display': "x",
            'displayColor': "red",
            'displayPriority': 2,
            'memoryDisplayColor': "blue",
            'name': "actor",
            'collideType': "actor",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        self.attackCost = attackCost
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
        self.health = self.health - int(attacker.damage)
        if(self.health <= 0):
            self.die(attacker)
        else:
            self.level.output_buffer.add(attacker.name.capitalize() +
                " hit " + self.name + " for " +
            str(attacker.damage) + " damage.\r")

    def die(self, killer):
        self.level.output_buffer.add("AURGH! " + self.name.capitalize() + 
        " was killed by " + killer.name + ".\r")
        self.level.grid.remove(self, self.xpos, self.ypos)
        self.level.timeline.remove(self)

    def move(self, direction):
        moveDict = {'north': [0, 1],
                    'south': [0, -1],
                    'west': [-1, 0],
                    'east': [1, 0]}
        temp = []
        for entity in self.level.grid.get(
        self.xpos+moveDict[direction][0], 
        self.ypos+moveDict[direction][1]):
            temp.append(entity.collide())
        if(temp.count("actor")>0):
            raise IndexError #HOW DO I DO EXCEPTIONS???
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

    def doNotWait(self):
        self.level.timeline.addToTop(self)

    def doMove(self, xDiff, yDiff):
        self.level.grid.add(self, self.xpos + xDiff, self.ypos + yDiff)
        self.level.grid.remove(self, self.xpos, self.ypos)
        self.xpos = self.xpos + xDiff
        self.ypos = self.ypos + yDiff
        self.andWait(self.moveCost)

    def doAttack(self, xDiff, yDiff):
        sorted(self.level.grid.get(self.xpos + xDiff, self.ypos + yDiff),
               reverse=True)[0].isAttacked(self)
        self.andWait(self.attackCost)

class Player(Actor):
    def __init__(self, xpos, ypos, level, *, collideType="combat_player", playerName=None, className=None,
                 **kwargs):
        defaults = {
            'damage': 1,
            'description': "It's you.",
            'display': '@',
            'displayColor': "player",
            'displayPriority': 3,
            'health': 10,
            'moveCost': 3,
            'name': "player",
            'collideType': "combat_player",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        #default name/class
        self.collideType = collideType
        self.className = "Blessed of Kaia"
        self.playerName = "Roderick"
        self.inventory = Inventory(self, self.level)

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
        #MOVE THIS CODE TO GRID/CELL
        temp = []
        for entity in self.level.grid.get(self.xpos + moveDict[direction][0],
        self.ypos + moveDict[direction][1]):
            temp.append(entity.collide())
        if(temp.count("actor")>0):
            raise IndexError #HOW DO I DO EXCEPTIONS???
        if(temp.count("true")==0 and temp.count("combat_enemy")==0):
            self.doMove(moveDict[direction][0], moveDict[direction][1])
            self.postMoveDescribe()
        elif(temp.count("combat_enemy")==1):
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
        else:
            self.andWait(0)

    def postMoveDescribe(self):
        cell = self.level.grid.getCell(self.xpos, self.ypos)
        for content in cell.getContents():
            if(isinstance(content, Item)):
                self.level.output_buffer.add("You're standing on an "+content.name+".")

    #def collide(self):
    #    return self.collideType

    def get(self):
        grounded_item = self.level.grid.getItem(self.xpos, self.ypos)
        if(not isinstance(grounded_item, Item)):
            self.level.output_buffer.add("There's no item here!")
            self.andWait(0)
            return
        elif(not self.inventory.hasSpace(more=1)):
            self.level.output_buffer.add("You're carrying too many things to pick that up.")
            self.andWait(0)
            return
        elif(not self.inventory.hasWeightSpace(more=grounded_item.weight)):
            self.level.output_buffer.add("You're carrying too much weight to pick that up.")
            self.andWait(0)
            return
        self.inventory.add(grounded_item)
        self.level.output_buffer.add("You picked up an "+grounded_item.name+".")
        self.andWait(1)

    def drop(self, letter):
        if(isinstance(self.inventory.get(letter), Item)):
            self.level.output_buffer.add("You dropped "+str(self.inventory.get(letter).name+"."))
            self.inventory.drop(letter)
            #self.level.draw()
            self.andWait(1)
        else:
            self.level.output_buffer.add("That item isn't in your inventory!")
            #self.level.draw()
            self.andWait(0)
        self.andWait(0)            

    def die(self, killer):
        self.level.output_buffer.clear()
        self.level.output_buffer.add("You died! Game over.")
        self.level.draw()
        unicurses.getch()
        unicurses.clear()
        unicurses.refresh()
        unicurses.endwin()
        print("Be seeing you...")
        exit()

class Enemy(Actor):
    def __init__(self, xpos, ypos, level, collideType="combat_enemy", **kwargs):
        defaults = {
            'damage': 1,
            'description': "A generic enemy.",
            'display': "x",
            'displayColor': "red",
            'displayPriority': 2,
            'health': 3,
            'memoryDisplayColor': "blue",
            'moveCost': 3,
            'name': "generic enemy",
            'collideType': "combat_enemy"
        }
        self.collideType = collideType
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def act(self):
        xDiff = self.xpos - self.level.player.xpos
        yDiff = self.ypos - self.level.player.ypos
        if(abs(xDiff) >= abs(yDiff)):
            if(xDiff >= 0):
                self.move("west")
            else:
                self.move("east")
        elif(yDiff >= 0):
            self.move("south")
        else:
            self.move("north")

    #def collide(self):
    #    return "combat_enemy"

def Zombie(x, y, level):
    return Enemy(x, y, level, name="zombie", display='X', moveCost=8,
                 description="A lumbering zombie.")

class Item(Entity):
    def __init__(self, xpos, ypos, level, weight=1, collideType='false', **kwargs):
        defaults = {
            'description': "An item",
            'display': '?',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': "item",
            'collideType':"false",
        }
        self.weight = weight
        self.collideType = collideType
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def collide(self):
        return self.collideType

class Equippable(Item):
    def __init__(self, xpos, ypos, level, slot='???', **kwargs):
        defaults = {
            'description': "A weapon",
            'display': '/',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'weapon',
            'weight': "1"
        }
        self.slot = slot
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults) 

class Armor(Equippable):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'description': "A weapon",
            'display': '/',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'weapon',
            'weight': "1",
            #'slot': '???'
        }
        moveCost = 0
        armorBonus = 0
        poise = 0
        #self.slot = slot
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults) 

class Weapon(Equippable):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'description': "A weapon",
            'display': '/',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'weapon',
            'weight': "1",
            'slot': 'weapon'
        }
        self.damage = 2 #what damage system to use later?
        self.toHitBonus = 0
        #self.sizeClass
        self.attackCost = 2
        #self.poiseDamage
        #self.handRequirements
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)    

class Floor(Entity):
    def __init__(self, xpos, ypos, level, collideType="false", type='solid', moveCost='0', **kwargs):
        defaults = {
            'description': "A floor.",
            'display': '.',
            'displayPriority': 0,
            'displayColor': "yellow",
            'memoryDisplayColor': "blue",
            'name': "floor",
            'collideType':"false",
        }
        self.moveCost = moveCost
        self.collideType = collideType
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

class Wall(Entity):
    def __init__(self, xpos, ypos, level, collideType="true", **kwargs):
        defaults = {
            'description': "A wall.",
            'display': '#',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'wall',
            'collideType': "true",
        }
        self.collideType = collideType
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def collide(self):
        return self.collideType