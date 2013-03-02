import sys

"""
The input parser. Called as the second half of the player's act() function; the
first half consists of draw().

Currently does NOT support arrow keys, diagonals, or any new-fangled fanciness.
"""

def masterInputParser(player, currentLevel):
    lineIn = ""
    lineIn = getch() #for right now, case insensitive
    #if(lineIn[0]!='\x1b'):
    #    lineIn = str(lineIn[0])
    #else:
    #if(len(lineIn)==2):
    #    lineIn = lineIn[1]
    #else:
    lineIn = str(lineIn[0])
    if(lineIn=='q'):
        sys.exit()
    elif(lineIn=='h' or lineIn=="D"):
        player.move("west")
    elif(lineIn=='j' or lineIn=="B"):
        player.move("south")
    elif(lineIn=='k' or lineIn=="A"):
        player.move("north")
    elif(lineIn=='l' or lineIn=="C"):
        player.move("east")
    elif(lineIn=='r' or lineIn=='.'):
        player.andWait(1)
    #elif(lineIn=='R'):
        #
    elif(lineIn=='x'):
        lookInputParser(player, currentLevel)
        player.andWait(0)
        currentLevel.draw()
    else:
        #currentLevel.currentOutputBuffer.add("Unknown command.")
        player.andWait(0)
    #urrentLevel.currentOutputBuffer.add(str(ord(lineIn)))

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
        if(lineIn=='h' or lineIn=="D"):
            xLook = xLook - 1
            #currentLevel.currentOutputBuffer.add("~")
        elif(lineIn=='j' or lineIn=="B"):
            yLook = yLook - 1
            #currentLevel.currentOutputBuffer.add("~")
        elif(lineIn=='k' or lineIn=="A"):
            yLook = yLook + 1
            #currentLevel.currentOutputBuffer.add("~")
        elif(lineIn=='l' or lineIn=="C"):
            xLook = xLook + 1
            #currentLevel.currentOutputBuffer.add("~")
        #elif(ord(lineIn)==27 or lineIn=='q'):
        else:
            if(lineIn=='q' or ord(lineIn)==27):
                break     


class _Getch:
    #Gets a single character from standard input.  Does not echo to the screen.
    #Found at http://code.activestate.com/recipes/134892/
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        ch=""
        sys.stdin.flush()
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if(ord(ch) == 27):
                ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdin.flush()
        #print("On its way out... "+str(ord(ch))+"\r\n")
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    """def __call__(self):
        import msvcrt
        return msvcrt.getch()"""
    def __call__(echo=False):
        "Get a single character on Windows."
        while msvcrt.kbhit():
            msvcrt.getch()
        ch = msvcrt.getch()
        while ch in b'\x00\xe0':
            msvcrt.getch()
            ch = msvcrt.getch()
            #if(ch=='27'):
            #    ch = msvcrt.getch()
        if echo:
            msvcrt.putch(ch)
        return ch.decode()


getch = _Getch()

"""import os
import sys    
import termios
import fcntl

def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

"""