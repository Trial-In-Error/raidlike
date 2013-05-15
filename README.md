raidlike
========

a little game project

running raidlike
================
requires unicurses library to be in the same directory
unicurses is available at: http://sourceforge.net/projects/pyunicurses/
to run a boring, square level, type: python3 main.py
to run a less boring level, type: python3 main.py level_mockup
to run an interesting line of sight test, type: python3 main.py los_test

playing raidlike
================
as per most roguelikes
implemented keys are:
    arrows: move
    hyujklbn: move
    x: look
    q: quit (or leave look context)

editing raidlike levels
================
the level (block one)
---------------------
this is a one-to-one map of the level, using 'glyphs' to represent in-game entities



the glyph set (block two)
------------------------
this starts at the keyword "Glyphs"

each glyph is mapped to one in-game class

after the class name, you can change attributes by adding a colon and specifying the attributes

for example, an enemy with 1 health and 0 damage might be E:enemy:health=1,damage=0

the available classes and attributes are:

*entity: xpos, ypos, description, display, displayColor, displayPriority, memoryDisplayColor, name
*wall: (all above)
*enemy: (all above, plus) moveCost, health, damage
*player: (all above, plus) playerName, className

the trigger set (block three)

this starts at the keyword "Triggers"

it currently does nothing, but they keyword must be present!

 
quirks, tips, and warnings
--------------------------
if no player glyph is added, the level will never render

if multiple player glyphs are added, they will take turns taking turns

if a ring of outer walls are not added, the player CAN take a long walk into nowhere

    if a wall exists on the opposite side of the level, they cannot

        but seriously, just make a ring of walls around all levels, please

if you specify an attribute that doesn't exist (or typo!), it will crash with a TypeError at runtime, 
specifying the offending attribute

if you get a ValueError ("need more than 1 value to unpack"), make sure you have all keywords (Glyphs, Triggers) in the level file
