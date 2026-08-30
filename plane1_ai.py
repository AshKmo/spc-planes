# you may put whatever code you want in this file, so long as it doesn't perform input or output of any kind (except for debugging)
# your code must also not depend on external libraries, but you are still allowed to use python's built-in libraries like math, random, etc.
# use of global varibles to maintain state is both permitted and encouraged

# your code must contain the function "plane_ai", which accepts the following arguments:
# - a tuple containing the x position, y position and rotation (in degrees) of the plane
# - a tuple containing the x position, y position and rotation (in degrees) of the enemy's plane
# - a list of tuples containing the x position, y position and rotation (in degrees) of each bullet on the map
# this function will be called every tick, and must return a tuple containing the new rotation of the plane (in degrees) and whether or not the plane should be firing bullets (True or False)
# all angles are in degrees of anticlockwise rotation from due east

# helpful information:
# - the arena is 800 pixels wide and 600 pixels long
# - planes are modeled by circles with a radius of 25 pixels
# - bullets are modeled by circles with a radius of 5 pixels
# - bullets disappear as soon as their position is outside the arena
# - the positions of planes are limited to the arena
# - bullets travel at 8 pixels per tick, while planes travel at 4 pixels per tick

# plane2's AI will have a flipped perspective so that it thinks it is plane1
# this means that you can copy someone else's plane AI into plane2_ai.py and it will always work as expected

def plane_ai(me, them, bullets):
    # set the plane's angle to 40 degrees anticlockwise from due east, and make it fire bullets
    return 40, True