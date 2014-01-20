from unicurses import *

def print_in_middle(win, starty, startx, width, string):
    
    if (win == None): win = stdscr
    y, x = getyx(win)
    if (startx != 0): x = startx
    if (starty != 0): y = starty
    if (width == 0): width = 80
    length = len(string)
    temp = (width - length) / 2
    x = startx + int(temp)
    mvaddstr(y, x, string)
    

stdscr = initscr()
noecho()
LINES, COLS = getmaxyx(stdscr)

if (has_colors() == False):
    endwin()
    print("Your terminal does not support color!")
    exit(1)

start_color()
use_default_colors()
init_pair(1, COLOR_RED, COLOR_BLACK)

border()
attron(COLOR_PAIR(1))
print_in_middle(stdscr, int(LINES / 2), 0, 0, "This line should be displayed in red color.")
attroff(COLOR_PAIR(1))
init_color(18, 100, 300, 450)

while(True):
    input = getstr()
    
    #erase()
    #stdscr.refresh()
    #attron(COLOR_RED)
    #init_pair(10, COLOR_CYAN, COLOR_BLACK)
    #init_color(COLOR_TEST, 1000, 0, 0)
    #init_pair(10, COLOR_TEST , COLOR_BLACK)
    #init_pair(COLOR_CYAN, 18, COLOR_BLACK)   
    #attron(COLOR_PAIR(10))
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
    print_in_middle(stdscr, int(LINES / 2), 0, 0, "Now it's another color! It's " + str(input))
    #attron(COLOR_PAIR(10))
    #attroff(COLOR_RED)
getch()
endwin()
