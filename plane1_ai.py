# you may put whatever code you want in this file, so long as it doesn't perform input or output of any kind (except when debugging)
# your code must not depend on external libraries, but you are still allowed to use python's built-in modules like math, random, etc.
# you are also allowed to use the "numpy" mathematics library in any way you want
# global varibles are also allowed

# your code must contain the function "plane_ai", which accepts three arguments:
# - an object containing the following properties of your plane:
#   - `.x`: its distance from the left edge of the arena (float)
#   - `.y`: its distance from the top edge of the arena (float)
#   - `.rotation`: its rotation (anticlockwise from due east), in degrees (float)
#   - `.health`: its health, from 0 to 5 (integer)
#   - `.shoot_cooldown`: the number of ticks left until the plane can shoot another bullet (integer)
# - another object containing the same properties of the enemy plane
# - a list of objects containing the following information about each bullet on the map:
#   - `.x`: its distance from the left edge of the arena (float)
#   - `.y`: its distance from the top edge of the arena (float)
#   - `.rotation`: its rotation (anticlockwise from due east), in degrees (float)
#   - `.lifetime`: the number of ticks left until the bullet is destroyed (integer)
# this function will be called every tick (20 milliseconds), and must return a tuple containing the following:
# - a float indicating the speed that the plane should travel at, between 0 and 1 (inclusive)
# - the direction that the plane should point toward (anticlockwise from due east, in degrees)
# - whether the plane should fire bullets (True or False)

# some helpful information:
# - there are 50 ticks per second
# - the arena is 800 pixels wide and 600 pixels tall
# - your plane's hitbox is a circle with a radius of 10 pixels
# - your bullet's hitbox is a circles with a radius of 5 pixels
# - there are invisible walls on all sides of the arena, which only bullets can pass through
# - bullets always move at 8 pixels per tick, and planes can move at between 0 and 4 pixels per tick
# - your plane's turning speed is capped at 10 degrees per tick

# plane2's AI will have a flipped perspective so that it thinks it is plane1
# this means you can send your AI to someone else and they can copy it into plane2_ai.py and it will work as expected

import numpy
from constants import *

def plane_ai(me, them, bullets):
    # set the plane's speed to 100%, set its angle to 40 degrees anticlockwise from due east, and make it fire bullets
    return 1, 40, True