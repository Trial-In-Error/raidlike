import string, entity, config

class Inventory():
    def __init__(self, player, level):
        self.player = player
        self.level = level
        self.inventoryList = []
        self.letterList = {}
        for index, letter in enumerate(string.ascii_letters):
            self.letterList[index+1] = letter
            self.letterList[letter] = index+1
        self.MAGICALCARRYWEIGHT = 100

    def hasSpace(self, more=0):
        if(len(self.inventoryList)+more >= 52):
            return False
        else:
            return True

    def hasWeightSpace(self, more=0):
        if(self.getWeight()+more > self.MAGICALCARRYWEIGHT):
            return False
        else:
            return True

    def getWeight(self):
        weight = 0
        for item in self.inventoryList:
            weight += item.weight
        return weight

    def add(self, item):
        self.inventoryList.append(item)

    def drop(self, letter):
        config.world.currentLevel.grid.dropItem(self.level.player.xpos, self.level.player.ypos, self.get(letter))
        temp = self.remove(letter)

    def remove(self, letter):
        del self.inventoryList[self.getIndex(letter)]

    def get(self, letter):
        try:
            return self.inventoryList[self.letterList[letter]-1]
        except:
            pass

    def getIndex(self, letter):
        return self.letterList[letter]-1

    def sort(self):
        pass

    def consume(self):
        pass

class Equipment():
    def __init__(self):
        self.equipmentSlots = ["weapon", "offhand", "armor"]
        self.slotCount = len(self.equipmentSlots)
        self.equipmentList = [[] for x in range(slotCount)]
        self.letterList = {}
        try:
            for index, letter in enumerate(string.ascii_letters[:self.slotCount]):
                self.letterList[index+1] = letter
                self.letterList[letter] = index+1
        except:
            pass
        self.MAGICALEQUIPWEIGHT = 100

    def equip(self, equipmentSlots):
        pass