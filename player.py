from entity import *
from masterInputParser import *
from grid import *
from actor import *
from sys import *
import os

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
        self.className = className
        self.playerName = playerName

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
        getch()
        clear()
        refresh()
        endwin()
        print("Be seeing you...")
        sys.exit()
