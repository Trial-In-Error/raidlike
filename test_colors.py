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

try:
    bool(os.environ['TERM']) #?
except KeyError:
    os.environ['TERM'] = foo
os.environ['TERM'] = "xterm-256color"  

stdscr = initscr()
noecho()
LINES, COLS = getmaxyx(stdscr)

if (has_colors() == False):
    endwin()
    print("Your terminal does not support color!")
    exit(1)

if (can_change_color() == False):
    endwin()
    print("Your terminal does not support color changes!")
    exit(1)

start_color()
init_pair(1, COLOR_RED, COLOR_BLACK)

border()
attron(COLOR_PAIR(1))
print_in_middle(stdscr, int(LINES / 2), 0, 0, "This line should be displayed in red color.")
attroff(COLOR_PAIR(1))
input = getch()
init_pair(2, 46, COLOR_BLACK)
attron(COLOR_PAIR(2))
print_in_middle(stdscr, int(LINES / 2), 0, 0, "Now it's another color!")
input = getch()
attroff(COLOR_PAIR(2))
endwin()
