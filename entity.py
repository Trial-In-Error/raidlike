import unicurses
from masterInputParser import masterInputParser
from sys import exit
from inventory import Inventory
import config
from religion import Boon

class Entity():
    def __init__(self, xpos, ypos, level, *,
                 description="A floor.",
                 display='.',
                 displayColor="yellow",
                 displayPriority=1,
                 memoryDisplayColor="blue",
                 name="floor", collideType="false",
                 moveCost=1):
        self.xpos = xpos
        self.ypos = ypos
        self.level = level
        self.description = description
        self.display = display
        self.displayColor = displayColor
        self.displayPriority = displayPriority
        self.memoryDisplayColor = memoryDisplayColor
        self.collideType = collideType
        self.name = name
        self.moveCost = moveCost
        try:
            self.level.grid.add(self, xpos, ypos)
        except AttributeError:
            pass 

    def __lt__(self, other):
        if self.displayPriority < other.displayPriority:
            return True
        else:
            return False

    def drawRelative(self, player_xpos, player_ypos, lensWidth, lensHeight):
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))

    def drawRelativeBold(self, player_xpos, player_ypos, lensWidth, lensHeight):
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display, unicurses.A_REVERSE)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))

    def drawRelativeFromMemory(self,player_xpos, player_ypos, lensWidth, lensHeight):
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[self.memoryDisplayColor]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[self.memoryDisplayColor]))

    def describe(self):
        return self.description

    def collide(self):
        return self.collideType

    def __str__(self):
        return self.display

class Obelisk(Entity):
    def __init__(self, xpos, ypos, level, textColor="white", **kwargs):
        defaults = {
            'display': "",
            'displayColor': "94",
            'memoryDisplayColor': "94",
            'collideType': "obelisk",
            'name': "obelisk",
            'description': "An ancient stone obelisk.",
        }
        defaults.update(kwargs)
        self.level = level
        self.textColor = textColor
        super().__init__(xpos, ypos, level, **defaults)

class TriggerTile(Entity):
    def __init__(self, xpos, ypos, level, repeatable=True, triggerDescription=None, internalName=None, textColor="white", **kwargs):
        defaults = {
        }
        defaults.update(kwargs)
        self.triggerDescription = triggerDescription
        self.level = level
        self.textColor = textColor
        try:
            self.repeatable = eval(repeatable)
        except TypeError:
            self.repeatable = repeatable
        self.hasBeenCollided = False
        self.internalName = internalName
        if(self.internalName and not self.repeatable):
            self.level.triggerTileList.append(self)
        super().__init__(xpos, ypos, level, **defaults)

    def collide(self):
        if(self.triggerDescription and self.repeatable
            or self.triggerDescription and not self.hasBeenCollided):
            config.world.currentLevel.output_buffer.add_formatted([self.triggerDescription, self.textColor])
            for entry in self.level.triggerTileList:
                if(entry.internalName == self.internalName):
                    entry.hasBeenCollided = True
        self.hasBeenCollided = True
        return self.collideType

class Door(Entity):
    def __init__(self, xpos, ypos, level, isOpen=False, keyInternalName=None, openDescription="The door opens.", closeDescription=None, openDisplay="'", closedDisplay="+", textColor="white", **kwargs):
        defaults = {
            'display': "+",
            'displayColor': "94",
            'memoryDisplayColor': "94",
            'name': "door",
            'description': "A closed door.",
        }
        defaults.update(kwargs)
        self.level = level
        self.textColor = textColor
        self.openDisplay = openDisplay
        self.closedDisplay = closedDisplay
        self.openDescription = openDescription
        self.closeDescription = closeDescription
        self.keyInternalName = keyInternalName
        self.isOpen = isOpen
        if(self.isOpen):
            defaults['collideType'] = "open_door"
        else:
            defaults['collideType'] = "closed_door"

        super().__init__(xpos, ypos, level, **defaults)

    def open(self, opener):
        hasKey = False
        if isinstance(opener, Player):
            for entity in self.level.player.inventory.inventoryList:
                if(isinstance(entity, Key) and entity.internalName == self.keyInternalName):
                    hasKey = True
        if((not self.isOpen and self.keyInternalName == None)
            or (not self.isOpen and hasKey)):
            if isinstance(opener, Player):
                config.world.currentLevel.output_buffer.add(self.openDescription)
            self.collideType = "open_door"
            self.display = "'"
            self.description = self.openDescription
            opener.andWait(1)
        else:
            opener.andWait(0)
            if isinstance(opener, Player):
                config.world.currentLevel.output_buffer.add("The "+ self.name + " is locked.")
            # make it cost time to check?

class Portal(Entity):
    def __init__(self, xpos, ypos, level, *, internalName, toWhichPortal, toWhichLevel, direction, **kwargs):
        defaults = {
            'description': "A portal to somewhere else.",
            'display': "*",
            'displayColor': "red",
            'displayPriority': 2,
            'memoryDisplayColor': "red",
            'name': "portal",
            'collideType': "portal",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        self.internalName = internalName
        self.toWhichLevel = toWhichLevel
        #self.name = name
        self.toWhichPortal = toWhichPortal
        self.direction = direction
        level.portalList.append(self)
    def collide(self):
        config.world.swapLevels(self)
        return self.collideType


class Actor(Entity):
    def __init__(self, xpos, ypos, level, *, canOpenDoors=False, guaranteedDropList=[], attackCost=2, damage=1, health=3, moveCost=3,
                 **kwargs):
        defaults = {
            'description': "An actor. This shouldn't be instantiated!",
            'display': "x",
            'displayColor': "red",
            'displayPriority': 2,
            'memoryDisplayColor': "blue",
            'name': "actor",
            'collideType': "false",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        self.attackCost = attackCost
        self.damage = damage
        self.health = health
        self.moveCost = moveCost
        self.canOpenDoors = canOpenDoors
        self.guaranteedDropList = guaranteedDropList
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
        self.level.timeline.remove(self)
        self.level.grid.remove(self, self.xpos, self.ypos)
        self.level.output_buffer.add("AURGH! " + self.name.capitalize() + 
        " was killed by " + killer.name + ".\r")
        if self.guaranteedDropList:
            for item in self.guaranteedDropList.split("),"):
                try:
                    item = eval(item)
                except SyntaxError:
                    item = eval(item+")")
                item.xpos = self.xpos
                item.ypos = self.ypos
                item.level = self.level
                self.level.grid.add(item, self.xpos, self.ypos)
        # percent drop chance items go here

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


        if(temp.count("portal")>0):
            return
        if(temp.count("closed_door")>0 and self.canOpenDoors):
            self.openDoor(moveDict[direction][0], moveDict[direction][1])
            return
        if(temp.count("closed_door")>0 and not self.canOpenDoors):
            self.andWait(1)
            return
        if(temp.count("actor")>0):
            raise IndexError #HOW DO I DO EXCEPTIONS???
        if(temp.count("true")==0
        and temp.count("combat_player")==0
        and temp.count("combat_enemy")==0 and temp.count("portal")==0 and temp.count("see_through")==0 and temp.count("closed_door")==0):
            self.doMove(moveDict[direction][0], moveDict[direction][1])
            return
        if(temp.count("combat_player")==1):
            self.doAttack(moveDict[direction][0], moveDict[direction][1])
            return
        self.andWait(1)
        #else:
            #why must this be 1??
            #self.andWait(1)

    def openDoor(self, xDiff, yDiff):
        for entity in self.level.grid.get(self.xpos+xDiff, self.ypos+yDiff):
            if(isinstance(entity, Door)):
                entity.open(self)
        #self.andWait(0)

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
    def __init__(self, xpos, ypos, level, *, playerName=None, title=None, worshipping=None,
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
            'canOpenDoors': True,
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        #default name/class
        self.title = "Chosen of Brand"
        self.playerName = "Roderick"
        self.worshipping = worshipping
        self.inventory = Inventory(self, self.level)
        self.boonList = []

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
        if(temp.count("portal")>0):
            return
        if(temp.count("closed_door")>0):
            self.openDoor(moveDict[direction][0], moveDict[direction][1])
            return
        if(temp.count("actor")>0):
            raise IndexError #HOW DO I DO EXCEPTIONS???
        if(temp.count("true")==0 and temp.count("combat_enemy")==0 and temp.count("portal")==0 and temp.count("see_through")==0 and temp.count("closed_door")==0):
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
            config.world.currentLevel.output_buffer.add("You dropped "+str(self.inventory.get(letter).name+"."))
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
        self.level.output_buffer.add("Press 'q' to quit.") #CHANGE TO SPACE
        self.level.draw()
        while(True):
            lineIn = unicurses.getch()
            if(lineIn==unicurses.CCHAR('q')):
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
            'display': "x",
            'displayColor': "red",
            'displayPriority': 2,
            'health': 3,
            'memoryDisplayColor': "blue",
            'moveCost': 3,
            'name': "generic enemy",
            'collideType': "combat_enemy"
        }
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

def Zombie(x, y, level):
    return Enemy(x, y, level, name="zombie", display='X', moveCost=8,
                 description="A lumbering zombie.")

class Item(Entity):
    def __init__(self, xpos, ypos, level, weight=1, **kwargs):
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
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

class Key(Item):
    def __init__(self, xpos, ypos, level, internalName, **kwargs):
        defaults = {
            'description': "A key.",
            'display': '?',
            'displayPriority': 2,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'key',
            'weight': 0,
        }
        self.internalName = internalName
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults) 

    @classmethod
    def fromString(cls, string):
        tempList = string.split(',')
        kwargs = {}
        for entry in tempList:
            temp = entry.split('=')
            try:
                kwargs[temp[0].strip()] = temp[1].strip()
            except IndexError:
                pass
        return cls(xpos=None, ypos=None, level=None, internalName=tempList[0], **kwargs)

class Equippable(Item):
    def __init__(self, xpos, ypos, level, slot='???', **kwargs):
        defaults = {
            'description': "A weapon.",
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
    def __init__(self, xpos, ypos, level, type='solid', moveCost='0', **kwargs):
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
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

class Wall(Entity):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'description': "A wall.",
            'display': '#',
            'displayPriority': 1,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': 'wall',
            'collideType': "true",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def collide(self):
        return self.collideType

class Hound(Enemy):
    def __init__(self, xpos, ypos, level, **kwargs):
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
        defaults.update(kwargs)
        self.hasBeenSeen = False
        super().__init__(xpos, ypos, level, **defaults)

    def act(self):
        if(self.hasBeenSeen):
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

    def drawRelative(self, player_xpos, player_ypos, lensWidth, lensHeight):
        if(not self.hasBeenSeen):
            self.level.timeline.add(self, 0)
            self.hasBeenSeen = True
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))

    def drawRelativeBold(self, player_xpos, player_ypos, lensWidth, lensHeight):
        if(not self.hasBeenSeen):
            self.level.timeline.add(self, 0)
            self.hasBeenSeen = True
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display, unicurses.A_REVERSE)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))