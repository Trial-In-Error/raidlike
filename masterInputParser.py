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
    elif(lineIn==CCHAR('r') or lineIn==CCHAR('.')):
        player.andWait(1)
    #elif(lineIn=='R'):
        #
    elif(lineIn==CCHAR('x')):
        lookInputParser(player, currentLevel)
        player.andWait(0)
        currentLevel.draw()
    else:
        #currentLevel.currentOutputBuffer.add("Unknown command.")
        player.andWait(0)
    #urrentLevel.currentOutputBuffer.add(str(ord(lineIn)))

"""NOT YET UP TO DATE WITH CURSES"""

def lookInputParser(player, currentLevel):
    xLook = player.xpos
    yLook = player.ypos
    while(True):
        currentLevel.currentOutputBuffer.add(sorted(
        currentLevel.currentGrid.get(xLook, yLook), reverse=True)[0].name)
        currentLevel.draw()
        currentLevel.currentOutputBuffer.output()
        lineIn = ""
        lineIn = getch()
        #currentLevel.currentOutputBuffer.add("LINE IN: "+str(ord(lineIn)))
        if(lineIn==CCHAR('h') or lineIn==KEY_LEFT):
            xLook = xLook - 1
            #currentLevel.currentOutputBuffer.add("~")
        elif(lineIn==CCHAR('j') or lineIn==KEY_DOWN):
            yLook = yLook - 1
            #currentLevel.currentOutputBuffer.add("~")
        elif(lineIn==CCHAR('k') or lineIn==KEY_UP):
            yLook = yLook + 1
            #currentLevel.currentOutputBuffer.add("~")
        elif(lineIn==CCHAR('l') or lineIn==KEY_RIGHT):
            xLook = xLook + 1
            #currentLevel.currentOutputBuffer.add("~")
        #elif(ord(lineIn)==27 or lineIn=='q'):
        else:
            if(lineIn==CCHAR('q')):
                break     