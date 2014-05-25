import unicurses
from masterInputParser import masterInputParser
from sys import exit
from inventory import Inventory
import config
from religion import Boon
import random

class Entity():
    def __init__(self, xpos, ypos, level, *,
                 description="A floor.",
                 display='.', displayColor="yellow",
                 displayPriority=1,
                 memoryDisplayColor="blue",
                 name="floor", collideType={},
                 moveCost=1):
        self.xpos = xpos
        self.ypos = ypos
        self.level = level
        self.description = description
        self.display = display
        self.displayColor = displayColor
        self.displayPriority = displayPriority
        self.memoryDisplayColor = memoryDisplayColor
        try:
            if(len(eval(str(collideType)).keys()) != 0):
                self.collideType = dict(list(config.collideType.items())+list(eval(str(collideType)).items()))
        except (ValueError, NameError, AttributeError):
            raise ValueError("Error initializing entity {!r}'s collideType: local collideType {}"
                               "".format(type(self), collideType))
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
    def __init__(self, xpos, ypos, level,
                exitDirection = "e",
                triggerDescription=None,
                internalName=None,
                shardIncrement=5,
                textColor="white", **kwargs):
        defaults = {
            'display': "",
            'displayColor': "94",
            'memoryDisplayColor': "94",
            'collideType': {"isObelisk":True, "blocksWalking":True},
            'name': "obelisk",
            'description': "An ancient stone obelisk.",
            'display':"&",
        }
        defaults.update(kwargs)
        self.level = level
        self.textColor = textColor
        self.triggerDescription = triggerDescription
        self.hasBeenCollided = False
        self.internalName = internalName
        self.exitDirection = exitDirection
        self.shardIncrement = shardIncrement
        super().__init__(xpos, ypos, level, **defaults)

    def collide(self):
        config.world.currentLevel.output_buffer.add_formatted(["You touch the obelisk.", self.textColor])
        config.world.currentLevel.player.health = config.world.currentLevel.player.maxHealth
        config.world.currentLevel.player.poise = config.world.currentLevel.player.maxPoise
        if(self.triggerDescription and not self.hasBeenCollided):
            config.world.currentLevel.output_buffer.add_formatted([self.triggerDescription, self.textColor])
            config.player.shardCount = config.player.shardCount + self.shardIncrement
        elif(config.player.shardCount <= 0):
            config.player.shardCount = 2
            config.world.currentLevel.output_buffer.add("You feel the obelisk lending you strength.")
        self.hasBeenCollided = True
        config.player.lastObelisk = self
        #put code to increment healing items here
        return self.collideType

class TriggerTile(Entity):
    def __init__(self, xpos, ypos, level,
                repeatable=True,
                triggerDescription=None,
                internalName=None, percentChance=100,
                textColor="white", **kwargs):
        defaults = {
            'displayPriority':1,
            'collideType':{"blocksLoS":False}
        }
        defaults.update(kwargs)
        self.triggerDescription = triggerDescription
        self.level = level
        self.textColor = textColor
        self.percentChance = percentChance
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
        temp = random.uniform(1, 100)
        if(self.triggerDescription and self.repeatable
            or self.triggerDescription and not self.hasBeenCollided
            and self.percentChance != 100
            and self.percentChance > temp):
            config.world.currentLevel.output_buffer.add_formatted([self.triggerDescription, self.textColor])
            for entry in self.level.triggerTileList:
                if(entry.internalName == self.internalName):
                    entry.hasBeenCollided = True
        self.hasBeenCollided = True
        return self.collideType

class Door(Entity):
    def __init__(self, xpos, ypos, level, collideType={"isDoor":True},
                keyInternalName=None,
                openDescription="You open the door.",
                closeDescription=None, openDisplay="'",
                closedDisplay="+", textColor="white", **kwargs):
        defaults = {
            'display': "+",
            'displayColor': "94",
            'memoryDisplayColor': "94",
            'name': "door",
            'description': "A closed door.",
            'displayPriority':1,
        }
        defaults.update(kwargs)
        self.collideType = dict(list(config.collideType.items())+list(eval(str(collideType)).items()))
        super().__init__(xpos, ypos, level, **defaults)
        self.level = level
        self.textColor = textColor
        self.openDisplay = openDisplay
        self.closedDisplay = closedDisplay
        self.openDescription = openDescription
        self.closeDescription = closeDescription
        self.keyInternalName = keyInternalName
        try:
            if(self.collideType["isOpen"]):
                if(self.openDescription):
                    self.description = self.openDescription
            else:
                self.collideType["blocksLoS"] = True
                self.collideType["blocksWalking"] = True 
                self.collideType["blocksFlight"] = True 
                if(self.closeDescription):
                    self.description  = self.closeDescription
        except TypeError:
            raise TypeError("Self.collideType = "+str(self.collideType))

    def open(self, opener):
        hasKey = False
        if isinstance(opener, Player):
            for entity in self.level.player.inventory.inventoryList:
                if(isinstance(entity, Key) and entity.internalName == self.keyInternalName):
                    hasKey = True
        if((not self.collideType["isOpen"] and self.keyInternalName == None)
            or (not self.collideType["isOpen"] and hasKey)):
            if isinstance(opener, Player) and not self.openDescription == "None":
                config.world.currentLevel.output_buffer.add(self.openDescription)
            self.collideType["isOpen"] = True
            self.collideType["blocksLoS"] = False
            self.collideType["blocksWalking"] = False
            self.collideType["blocksFlight"] = False
            self.display = self.openDisplay
            self.description = self.openDescription
            opener.andWait(1) #variabilize this
        else:
            opener.andWait(0)
            if isinstance(opener, Player):
                config.world.currentLevel.output_buffer.add("The "+ self.name + " is locked.")
            # make it cost time to check?

    def close(self, closer):
        if((self.collideType["isOpen"])):
            self.collideType["isOpen"] = False
            self.collideType["blocksLoS"] = True #variabilize?
            self.collideType["blocksWalking"] = True
            self.collideType["blocksFlight"] = True
            self.keyInternalName = None #the art of re-locking is a lost one
            self.display = self.closedDisplay
            self.description = self.closeDescription
            closer.andWait(1) #variabilize this
            # make it cost time to check?

class Portal(Entity):
    def __init__(self, xpos, ypos, level, *,
        internalName, toWhichPortal, toWhichLevel,
        direction, portalDescription = None, **kwargs):
        defaults = {
            'description': "A portal to somewhere else.",
            'display': "*",
            'displayColor': "red",
            'displayPriority': 2,
            'memoryDisplayColor': "red",
            'name': "portal",
            'collideType':{"isPortal":True},
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        self.internalName = internalName
        self.toWhichLevel = toWhichLevel
        self.toWhichPortal = toWhichPortal
        self.direction = direction
        self.portalDescription = portalDescription
        level.portalList.append(self)
    def collide(self):
        config.world.swapLevels(self)
        if(self.portalDescription):
            config.world.currentLevel.output_buffer.add(self.portalDescription)
        return self.collideType


class Actor(Entity):
    def __init__(self, xpos, ypos, level, *,
                canOpenDoors=False, guaranteedDropList=[],
                attackCost=10, damage=10, health=3, moveCost=10,
                poise=100, poiseRegen=1, poiseDamage=20,
                maxPoise=100, poiseRecovery=50, staggerCost=15, collideType={},
                **kwargs):
        defaults = {
            'description': "An actor. This shouldn't be instantiated!",
            'display': "x",
            'displayColor': "red",
            'displayPriority': 2,
            'memoryDisplayColor': "blue",
            'name': "actor",
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        self.attackCost = attackCost
        self.damage = damage
        self.health = int(health)
        self.maxHealth = int(health)
        self.moveCost = moveCost
        self.canOpenDoors = canOpenDoors
        self.poise = maxPoise
        self.poiseRegen = poiseRegen
        self.maxPoise = maxPoise
        self.poiseDamage = poiseDamage
        self.poiseRecovery = poiseRecovery
        self.staggerCost = staggerCost
        self.guaranteedDropList = guaranteedDropList
        self.collideType = dict(list(config.collideType.items())+list(collideType.items()))
        self.level.timeline.add(self)

    def act(self):
        pass

    def isAttacked(self, attacker):
        if(self.isHit(attacker)):
            self.takeDamage(attacker)

    def isHit(self, attacker):
        return(True)

    def takeDamage(self, attacker): #note: things only die if isDamaged

        #poise damage
        self.poise = self.poise - attacker.poiseDamage
        if(self.poise <= 0):
            self.poise = self.poiseRecovery
            self.andDelay(self.staggerCost)
            self.level.output_buffer.add_formatted([attacker.name.capitalize() +
                " staggered " + self.name + "!\r", "red"])

        #health damage
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
        temp = config.collideType.copy()
        for entity in self.level.grid.get(self.xpos + config.directions[direction][0],
        self.ypos + config.directions[direction][1]):
            for key in entity.collideType:
                if(entity.collideType[key]):
                    temp[key] = entity.collideType[key]
        if(temp["isPortal"]):
            return
        if(temp["isDoor"] and not temp["isOpen"] and self.canOpenDoors):
            self.openDoor(config.directions[direction][0], config.directions[direction][1])
            return
        if(temp["isDoor"] and not self.canOpenDoors and not temp["isOpen"]):
            self.andWait(1)
            return
        if(not temp["blocksWalking"] and not temp["isEnemy"]):
            self.doMove(config.directions[direction][0], config.directions[direction][1])
            return
        if(temp["isPlayer"]):
            self.doAttack(config.directions[direction][0], config.directions[direction][1])
            return
        self.andWait(1) #why does this have to be andWait(1)?

    def openDoor(self, xDiff, yDiff):
        for entity in self.level.grid.get(self.xpos+xDiff, self.ypos+yDiff):
            if(isinstance(entity, Door)):
                entity.open(self)

    def andWait(self, time):
        self.level.timeline.add(self, time)
        return time

    def doNotWait(self):
        self.level.timeline.addToTop(self)
        return 0

    def andDelay(self, time):
        self.level.timeline.delay(self, time)

    def doMove(self, xDiff, yDiff):
        self.level.grid.add(self, self.xpos + xDiff, self.ypos + yDiff)
        self.level.grid.remove(self, self.xpos, self.ypos)
        self.xpos = self.xpos + xDiff
        self.ypos = self.ypos + yDiff
        return self.andWait(self.moveCost + int(self.level.grid.
            getCell(self.xpos, self.ypos).getBottomContent().moveCost))

    def doAttack(self, xDiff, yDiff):
        for entity in self.level.grid.get(self.xpos + xDiff, self.ypos + yDiff):
            if(entity.collideType["isEnemy"] or entity.collideType["isPlayer"]):
                entity.isAttacked(self)
                return self.andWait(self.attackCost)

class Player(Actor):
    def __init__(self, xpos, ypos, level, *,
                playerName=None, title=None,
                worshipping=None, healCost=10, healValue=30, collideType={},
                **kwargs):
        #EQUIPPING SHIT MUST CHANGE SELF.ATTACKCOST,
        #SELF.POISE, .POISEREGEN, .POISEDAMAGE, .STAGGERCOST
        #ATTACKCOST, MOVECOST, POISERECOVERY, ETC.
        defaults = {
            'damage': 1,
            'description': "It's you.",
            'display': '@',
            'displayColor': "player",
            'displayPriority': 3,
            'health': 100,
            'moveCost': 10,
            'name': "player",
            'collideType': {"isPlayer":True, "initiatesCombat":True, "blocksWalking":True},
            'canOpenDoors': True,
            'poiseRegen': 1,
            'damage': 15,
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)
        #default name/class
        self.title = "Chosen of Brand"
        self.playerName = "Roderick"
        self.worshipping = worshipping
        self.lastObelisk = None
        self.shardCount = 0
        self.inventory = Inventory(self, self.level)
        self.boonList = []
        self.healCost = healCost
        self.healValue = healValue

    def act(self):
        self.level.draw()
        temp = masterInputParser(self, self.level)
        self.poise = min(self.poise+self.poiseRegen*temp, self.maxPoise)

    def heal(self):
        if(self.shardCount > 0 and self.health != self.maxHealth):
            self.health = min(self.maxHealth, self.health+self.healValue)
            self.shardCount = self.shardCount - 1
            self.andWait(self.healCost)
            self.level.output_buffer.add("You heal.")
            return self.healCost
        elif(self.shardCount == 0):
            self.andWait(0)
            self.level.output_buffer.add("You don't have any shards!")
            return 0
        elif(self.health == self.maxHealth and self.shardCount > 0):
            self.andWait(0)
            self.level.output_buffer.add("You're already at max health.")
            return 0

    def move(self, direction):
        temp = config.collideType.copy()
        config.temp = temp
        for entity in self.level.grid.get(self.xpos + config.directions[direction][0],
        self.ypos + config.directions[direction][1]):
            collideType = entity.collide()
            for key in collideType:
                if(collideType[key]):
                    temp[key] = collideType[key]
        if(temp["isPortal"]):
            return 0
        if(temp["isObelisk"]):
            return self.andWait(0)
        if(temp["isDoor"] and not temp["isOpen"]):
            self.openDoor(config.directions[direction][0], config.directions[direction][1])
            return 0
        if(not temp["blocksWalking"] and not temp["isEnemy"]):
            tempNum = self.doMove(config.directions[direction][0], config.directions[direction][1])
            self.postMoveDescribe()
            return tempNum
        elif(temp["isEnemy"] and temp["initiatesCombat"]):
            return self.doAttack(config.directions[direction][0], config.directions[direction][1])
        else:
            return self.andWait(0)

    def postMoveDescribe(self):
        # generalize this!
        cell = self.level.grid.getCell(self.xpos, self.ypos)
        for content in cell.getContents():
            if(isinstance(content, Item)):
                if(content.name[0] in 'aeiouy'):
                    self.level.output_buffer.add("You're standing on an "+content.name+".")
                else:
                    self.level.output_buffer.add("You're standing on a "+content.name+".")

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
        if(grounded_item.name[0] in 'aeiouy'):
            self.level.output_buffer.add("You picked up an "+grounded_item.name+".")
        else:
            self.level.output_buffer.add("You picked up a "+grounded_item.name+".")
        self.andWait(1)

    def drop(self, letter):
        if(isinstance(self.inventory.get(letter), Item)):
            config.world.currentLevel.output_buffer.add("You dropped "+str(self.inventory.get(letter).name+"."))
            self.inventory.drop(letter)
            self.andWait(1)
        else:
            self.level.output_buffer.add("That item isn't in your inventory!")
            self.andWait(0)
        self.andWait(0)

    def die(self, killer):
        if(self.lastObelisk == None):
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
        else:
            if(self.lastObelisk.level != self.level):
                self.level.output_buffer.clear()
            self.lastObelisk.level.output_buffer.add("You died!")
            self.lastObelisk.level.output_buffer.add("You are reborn in a flash of fire at an obelisk.")
            if(self.shardCount <= 0):
                self.shardCount = 2
                self.lastObelisk.level.output_buffer.add("You feel the obelisk lend you strength.")
            config.world.swapViaDeath(self.lastObelisk)
            config.player.health = config.player.maxHealth
            # do terrible things to the player here

class Enemy(Actor):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'damage': 10,
            'description': "A generic enemy.",
            'display': "x",
            'displayColor': "red",
            'displayPriority': 3,
            'health': 100,
            'memoryDisplayColor': "blue",
            'moveCost': 10,
            'name': "generic enemy",
            'collideType': {"isEnemy":True, "initiatesCombat":True, "blocksWalking":True},
            'poiseDamage': 40,
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

    def act(self):
        self.poise = min(self.poise+self.poiseRegen, self.maxPoise)
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
    return Enemy(x, y, level, name="zombie", display='X', moveCost=15,
                 description="A lumbering zombie.")

class Item(Entity):
    def __init__(self, xpos, ypos, level, weight=1, **kwargs):
        defaults = {
            'description': "An item",
            'display': '?',
            'displayPriority': 2,
            'displayColor': "cyan",
            'memoryDisplayColor': "blue",
            'name': "item",
            'collideType':{"blocksLoS":False}
        }
        self.weight = weight
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

class Key(Item):
    def __init__(self, xpos, ypos, level,
                internalName, **kwargs):
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
        return cls(xpos=None, ypos=None, level=None,
                    internalName=tempList[0], **kwargs)

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
    def __init__(self, xpos, ypos, level, type='solid',
                moveCost='0', **kwargs):
        defaults = {
            'description': "A floor.",
            'display': '.',
            'displayPriority': 0,
            'displayColor': "yellow",
            'memoryDisplayColor': "blue",
            'name': "floor",
            'collideType':{"blocksLoS":False},
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
            'collideType':{"blocksLoS":True, "blocksWalking":True, "blocksFlight":True}
        }
        defaults.update(kwargs)
        super().__init__(xpos, ypos, level, **defaults)

class Hound(Enemy):
    def __init__(self, xpos, ypos, level, **kwargs):
        defaults = {
            'damage': 10,
            'description': "A generic enemy.",
            'display': "x",
            'displayColor': "red",
            'displayPriority': 2,
            'health': 3,
            'memoryDisplayColor': "blue",
            'moveCost': 6,
            'name': "generic enemy",
            'attackCost': 8,
        }
        defaults.update(kwargs)
        self.hasBeenSeen = False
        super().__init__(xpos, ypos, level, **defaults)

    def act(self):
        self.poise = min(self.poise+self.poiseRegen, self.maxPoise)
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

    def drawRelative(self, player_xpos, player_ypos,
                    lensWidth, lensHeight):
        if(not self.hasBeenSeen):
            self.level.timeline.add(self, 0)
            self.hasBeenSeen = True
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))

    def drawRelativeBold(self, player_xpos, player_ypos,
                        lensWidth, lensHeight):
        if(not self.hasBeenSeen):
            self.level.timeline.add(self, 0)
            self.hasBeenSeen = True
        unicurses.attron(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))
        unicurses.mvaddch(-self.ypos+player_ypos+lensHeight, self.xpos-player_xpos+lensWidth, self.display, unicurses.A_REVERSE)
        unicurses.attroff(unicurses.COLOR_PAIR(config.colorDict[self.displayColor]))

class Sleeper(Enemy):
    #add wake-up description!!!
    #add awake/asleep name split!
    def __init__(self, xpos, ypos, level,
                awakeDescription=None,
                wakingDescription=None, **kwargs):
        defaults = {
            'damage': 10,
            'description': "A generic enemy.",
            'display': "x",
            'displayColor': "red",
            'displayPriority': 2,
            'health': 3,
            'memoryDisplayColor': "blue",
            'moveCost': 10,
            'name': "generic enemy",
            #'collideType': "combat_enemy",
            'attackCost': 10,
        }
        defaults.update(kwargs)
        self.isAwake = False
        self.wakingDescription = wakingDescription
        self.awakeDescription = awakeDescription
        super().__init__(xpos, ypos, level, **defaults)

    def act(self):
        self.poise = min(self.poise+self.poiseRegen, self.maxPoise)
        if(self.isAwake):
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

    def takeDamage(self, attacker): #note: things only die if isDamaged
        #poise damage
        self.poise = self.poise - attacker.poiseDamage
        if(self.poise <= 0):
            self.poise = self.poiseRecovery
            self.andDelay(self.staggerCost)
            self.level.output_buffer.add_formatted([attacker.name.capitalize() +
                " staggered " + self.name + "!\r", "red"])

        if(not self.isAwake):
            if(not self.wakingDescription):
                self.level.output_buffer.add("The "+self.name+" wakes up, screaming in pain!")
            else:
                self.level.output_buffer.add(self.wakingDescription)
            self.level.timeline.add(self, 0)
            self.isAwake = True
        #this is problematic; it returns a list when I need a string!
        #self.name = self.name.split(' ')[1:]
        self.name = "guard"
        if(not self.awakeDescription):
            self.description = "A guard you've rudely awakened."
        else:
            self.description = self.awakeDescription
        self.health = self.health - int(attacker.damage)
        if(self.health <= 0):
            self.die(attacker)
        else:
            self.level.output_buffer.add(attacker.name.capitalize() +
                " hit " + self.name + " for " +
            str(attacker.damage) + " damage.\r")