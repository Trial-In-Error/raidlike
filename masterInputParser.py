import sys
from unicurses import *
import string
import config
#from levelManager import levelManager
#from main import world


"""
The input parser. Called as the second half of the player's act() function; the
first half consists of draw().
"""

def masterInputParser(player, level):
    lineIn = ""
    lineIn = getch()
    if(lineIn==CCHAR('q')):
        #os.environ['TERM'] = "xterm"
        config.world.save()
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
        lookInputParser(player, level)
        player.doNotWait()
    elif(lineIn==CCHAR('i')):
        inventoryInputParser(player, level)
        player.doNotWait()
    elif(lineIn==CCHAR('d')): #inventory drop code!
        dropInputParser(player, level)
        player.doNotWait()
    elif(lineIn==CCHAR('g')):
        player.get()
    elif(lineIn==CCHAR('s')):
        config.world.save()
        player.doNotWait()
    else:
        level.output_buffer.add("Unknown command.")
        player.doNotWait()

def inventoryInputParser(player, level):
    lineIn=""
    while(True):
        if(lineIn==CCHAR('q')):
            break
        level.drawInventoryInputParser()
        lineIn = ""
        lineIn = getch()

def dropInputParser(player, level):
    lineIn=""
    level.drawDropInputParser()
    charList = {}
    for letter in string.ascii_letters:
        charList[CCHAR(letter)] = letter
    while(True):
        if(lineIn in charList):
            player.drop(charList[lineIn])
            break
        level.drawDropInputParser()
        lineIn = ""
        lineIn = getch()
    #level.draw()


def lookInputParser(player, level):
    xLook = player.xpos
    yLook = player.ypos
    lineIn=""
    while(True):
        if(lineIn!=CCHAR('z')):
            level.output_buffer.add("Press z to inspect the current tile or q to stop looking.")
            #if(level.grid.getCell(xLook, yLook).hasBeenSeen):
            if(level.grid.getCell(xLook, yLook).hasBeenSeen and level.camera.isInView(xLook, yLook)):
                level.output_buffer.add(
                level.grid.getCell(xLook, yLook).getTopContent().name)
            else:
                level.output_buffer.add("unknown tile")
        level.draw()
        level.drawLookInputParser(xLook, yLook)
        lineIn = ""
        lineIn = getch()
        if(lineIn==CCHAR('h') or lineIn==KEY_LEFT):
            if(xLook > 1):
                xLook = xLook - 1
        elif(lineIn==CCHAR('j') or lineIn==KEY_DOWN):
            if(yLook > 1):
                yLook = yLook - 1
        elif(lineIn==CCHAR('k') or lineIn==KEY_UP):
            if(yLook < level.height):
                yLook = yLook + 1
        elif(lineIn==CCHAR('l') or lineIn==KEY_RIGHT):
            if(xLook < level.width):
                xLook = xLook + 1
        elif(lineIn==CCHAR('y') or lineIn==KEY_HOME):
            if(xLook > 1):
                xLook = xLook - 1
            if(yLook < level.height):
                yLook = yLook + 1
        elif(lineIn==CCHAR('b') or lineIn==KEY_END):
            if(xLook > 1):
                xLook = xLook - 1
            if(yLook > 1):
                yLook = yLook - 1
        elif(lineIn==CCHAR('u') or lineIn==KEY_PPAGE):
            if(xLook < level.width):
                xLook = xLook + 1
            if(yLook < level.height):
                yLook = yLook + 1
        elif(lineIn==CCHAR('n') or lineIn==KEY_NPAGE):
            if(xLook < level.width):
                xLook = xLook + 1
            if(yLook > 1):
                yLook = yLook - 1
        elif(lineIn==KEY_ENTER or lineIn==CCHAR('z')):
            if(level.grid.getCell(xLook, yLook).hasBeenSeen):
                level.output_buffer.add(level.grid.getCell(xLook, yLook).getTopContent().describe())
        else:
            if(lineIn==CCHAR('q')):
                break     