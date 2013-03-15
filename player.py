from entity import *
from masterInputParser import *
from grid import *
from actor import *
from sys import *
import os

class player(actor):
    def __init__(self, xpos, ypos, currentLevel, display='@'):
        super().__init__(xpos, ypos, currentLevel, '@') #why doesn't this work?
        self.display = '@' #why is this necessary explicitly?
        self.displayPriority = 1
        self.damage = 1
        self.health = 10
        self.name = "player"
        self.playerName = "Roderick"
        self.className = "Blessed of Kaia"
        self.displayColor = "white"
        self.description = "It's you."
        self.moveCost = 3
    def act(self):
        self.currentLevel.draw()
        masterInputParser(self, self.currentLevel)
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
        for entity in self.currentGrid.get(self.xpos + moveDict[direction][0],
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
        self.currentLevel.currentOutputBuffer.clear()
        self.currentLevel.currentOutputBuffer.add("You died! Game over.")
        self.currentLevel.draw()
        getch()
        clear()
        refresh()
        endwin()
        print("Be seeing you...")
        sys.exit()