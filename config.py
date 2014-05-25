#NOTE: THIS FILE MAY ONLY CONTAIN
#IMMUTABLE REFERENCES
#BECAUSE IT IS NOT SAVED OR LOADED

import unicurses
world = None
player = None
error_out = None
directions = {
	"n":[0, 1],
    "north":[0, 1],
	"s":[0, -1],
    "south":[0, -1],
	"e":[1, 0],
    "east":[1, 0],
	"w":[-1, 0],
    "west":[-1, 0],
	"ne":[1, 1],
    "northeast":[1, 1],
	"nw":[-1, 1],
    "northwest":[-1, 1],
	"se":[1, -1],
    "southeast":[1, -1],
	"sw":[-1, -1],
    "southwest":[-1, -1],
    (0, 1):"north",
    (0, -1):"south",
    (1, 0):"east",
    (-1, 0):"west",
    (1, 1):"northeast",
    (-1, 1):"northwest",
    (1, -1):"southeast",
    (-1, -1):"southwest"
}

collideType = {
    "blocksLoS":False,
    "blocksWalking":False,
    "blocksFlight":False, #unused
    "isObelisk":False,
    "isDoor":False,
    "isOpen":False,
    "isPortal":False,
    "initiatesCombat":False,
    "isPlayer":False,
    "isEnemy":False #unsure if needed!
}

colorDict = {
	"yellow":3,
    "cyan":6,
    "red":1,
    "white":15,
    "blue":4,
    "black":0,
    "player":15,
    "one":124,
    "two":56,
    "three":210,
    "g1":232,
    "g2":233,
    "g3":234,
    "g4":235,
    "g5":236,
    "g6":237,
    "g7":238,
    "g8":239,
    "g9":240,
    "g10":241,
    "g11":242,
    "g12":243,
    "g13":244,
    "g14":245,
    "g15":246,
    "g16":247,
    "g17":248,
    "g18":249,
    "g19":250,
    "g20":251,
    "g21":252,
    "g22":253,
    "g23":254,
    "g24":255,
    "stained_glass":196,
    "grass_memory":34,
    "grass":46,
    "stained_glass_memory":88,
    "sand_floor":220,
    "sand":226,
    "mud_wall":130,
    "wood_door":94,
    "memory":240,
    "wood_stair":142,
    "slaver":181,
    "hound": 228,
    }

# All possible 256 colors
# Formatted as [color_pair, foreground, background]
# Where color_pair is also the 256 color number for xterm
# See: http://blog.davewilkinsonii.com/images/tmux-configuration-for-great-good/256-color-palette.png
colorPalette = {}