import string

class Inventory():
    def __init__(self):
        self.inventoryList = []
        self.letterList = [letter for letter in string.ascii_letters]
        self.MAGICALCARRYWEIGHT = 100

    def hasSpace(self, more=0):
        if(len(self.inventoryList)+more >= 52):
            return False
        else:
            return True

    def hasWeightSpace(self, more=0):
        if(self.getWeight()+more >= self.MAGICALCARRYWEIGHT):
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

    def remove(self, letter):
        #self.inventoryList.
        pass

    def sort(self):
        pass

    def consume(self):
        pass

class Equipment():
    def __init__(self):
        self.equipmentSlots = ["weapon", "offhand", "armor"]
        self.slotCount = len(self.equipmentSlots)
        self.equipmentList = [[[x], [self.equipmentSlots[x]]] for x in range(slotCount)]
