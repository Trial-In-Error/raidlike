#NOTE: THIS FILE MAY ONLY CONTAIN
#IMMUTABLE REFERENCES

import unicurses
world = 0
player = 0
directions = {
	"n":[0, 1],
	"s":[0, -1],
	"e":[1, 0],
	"w":[-1, 0],
	"ne":[1, 1],
	"nw":[-1, 1],
	"se":[1, -1],
	"sw":[-1, -1]
}

colorDict = {
	"yellow":[1, unicurses.COLOR_YELLOW, unicurses.COLOR_BLACK],
    "cyan":[2, unicurses.COLOR_CYAN, unicurses.COLOR_BLACK],
    "red":[3, unicurses.COLOR_RED, unicurses.COLOR_BLACK],
    "white":[4, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK],
    "blue":[5, unicurses.COLOR_BLUE, unicurses.COLOR_BLACK],
    "player":[100, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK],
    "one":[6, 124, unicurses.COLOR_BLACK],
    "two":[7, 56, unicurses.COLOR_BLACK],
    "three":[8, 210, unicurses.COLOR_BLACK],
    "g1":[9, 232, unicurses.COLOR_BLACK],
    "g2":[10, 233, unicurses.COLOR_BLACK],
    "g3":[11, 234, unicurses.COLOR_BLACK],
    "g4":[12, 235, unicurses.COLOR_BLACK],
    "g5":[13, 236, unicurses.COLOR_BLACK],
    "g6":[14, 237, unicurses.COLOR_BLACK],
    "g7":[15, 238, unicurses.COLOR_BLACK],
    "g8":[16, 239, unicurses.COLOR_BLACK],
    "g9":[17, 240, unicurses.COLOR_BLACK],
    "g10":[18, 241, unicurses.COLOR_BLACK],
    "g11":[19, 242, unicurses.COLOR_BLACK],
    "g12":[20, 243, unicurses.COLOR_BLACK],
    "g13":[21, 244, unicurses.COLOR_BLACK],
    "g14":[22, 245, unicurses.COLOR_BLACK],
    "g15":[23, 246, unicurses.COLOR_BLACK],
    "g16":[24, 247, unicurses.COLOR_BLACK],
    "g17":[25, 248, unicurses.COLOR_BLACK],
    "g18":[26, 249, unicurses.COLOR_BLACK],
    "g19":[27, 250, unicurses.COLOR_BLACK],
    "g20":[28, 251, unicurses.COLOR_BLACK],
    "g21":[29, 252, unicurses.COLOR_BLACK],
    "g22":[30, 253, unicurses.COLOR_BLACK],
    "g23":[31, 254, unicurses.COLOR_BLACK],
    "g24":[32, 255, unicurses.COLOR_BLACK],
    "stained_glass":[33, 196, unicurses.COLOR_BLACK],
    "grass_memory":[34, 34, unicurses.COLOR_BLACK],
    "grass":[35, 46, unicurses.COLOR_BLACK],
    "stained_glass_memory":[36, 88, unicurses.COLOR_BLACK]
    }

colorPalette = {}