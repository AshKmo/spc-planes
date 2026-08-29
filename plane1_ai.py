# You may put whatever code you want in this file, so long as it doesn't perform input or output of any kind (except for debugging).
# Your code must also not depend on external libraries, but you are still allowed to use python's built-in libraries like math, random, etc.
# Use of global variables to maintain state is both permitted and encouraged.

# Your code must contain the function "plane_ai", which accepts the following arguments:
# - me: An object containing your plane's state with attributes: me.x, me.y, me.rot (in degrees)
# - them: An object containing the enemy plane's state with attributes: them.x, them.y, them.rot (in degrees)
# - bullets: A list of objects containing bullet data on the map. Each bullet has: b.x, b.y, b.rot (in degrees)
#
# This function will be called every tick, and must return a tuple containing:
# 1. The target rotation/angle of the plane (in degrees)
# 2. A boolean value indicating whether or not the plane should fire bullets (True or False)
#
# All angles are in degrees of anticlockwise rotation from due east.

# Helpful information:
# - The arena is 800 pixels wide and 600 pixels long
# - Planes are modeled by circles with a radius of 25 pixels
# - Bullets are modeled by circles with a radius of 5 pixels
# - Bullets disappear as soon as their position is outside the arena
# - The positions of planes are limited to the arena boundaries
# - Bullets travel at 8 pixels per tick, while planes travel at 4 pixels per tick

# Plane 2's AI will have a flipped perspective so that it thinks it is Plane 1.
# This means that you can copy someone else's plane AI into plane2_ai.py and it will always work as expected.

def plane_ai(me, them, bullets):
    # set the plane's angle to 40 degrees anticlockwise from due east, and make it fire bullets
    return 40, True
