import sys
from unicurses import *


"""
The input parser. Called as the second half of the player's act() function; the
first half consists of draw().

Currently does NOT support arrow keys, diagonals, or any new-fangled fanciness.
"""

def masterInputParser(player, currentLevel):
    lineIn = ""
    lineIn = getch()
    if(lineIn==CCHAR('q')):
        clear()
        refresh()
        endwin()
        print("Be seeing you...")
        sys.exit()
    elif(lineIn==CCHAR('h') or lineIn==KEY_LEFT):
        player.move("west")
    elif(lineIn==CCHAR('j') or lineIn==KEY_DOWN):
        player.move("south")
    elif(lineIn==CCHAR('k') or lineIn==KEY_UP):
        player.move("north")
    elif(lineIn==CCHAR('l') or lineIn==KEY_RIGHT):
        player.move("east")
    elif(lineIn==CCHAR('y') or lineIn==KEY_HOME):
        player.move("northwest")
    elif(lineIn==CCHAR('b') or lineIn==KEY_END):
        player.move("southwest")
    elif(lineIn==CCHAR('u') or lineIn==KEY_PPAGE):
        player.move("northeast")
    elif(lineIn==CCHAR('n') or lineIn==KEY_NPAGE):
        player.move("southeast")
    elif(lineIn==CCHAR('r') or lineIn==CCHAR('.')):
        player.andWait(1)
    #elif(lineIn=='R'):
        #
    elif(lineIn==CCHAR('x')):
        lookInputParser(player, currentLevel)
        player.andWait(0)
        currentLevel.draw()
    else:
        currentLevel.currentOutputBuffer.add("Unknown command.")
        player.andWait(0)


def lookInputParser(player, currentLevel):
    xLook = player.xpos
    yLook = player.ypos
    lineIn=""
    while(True):
        if(lineIn!=CCHAR('z')):
            currentLevel.currentOutputBuffer.add(
            currentLevel.currentGrid.getTop(xLook, yLook).name)
        currentLevel.draw()
        lineIn = ""
        lineIn = getch()
        if(lineIn==CCHAR('h') or lineIn==KEY_LEFT):
            xLook = xLook - 1
        elif(lineIn==CCHAR('j') or lineIn==KEY_DOWN):
            yLook = yLook - 1
        elif(lineIn==CCHAR('k') or lineIn==KEY_UP):
            yLook = yLook + 1
        elif(lineIn==CCHAR('l') or lineIn==KEY_RIGHT):
            xLook = xLook + 1
        elif(lineIn==KEY_ENTER or lineIn==CCHAR('z')):
            currentLevel.currentOutputBuffer.add(currentLevel.currentGrid.getTop(xLook, yLook).describe())
        else:
            if(lineIn==CCHAR('q')):
                break     