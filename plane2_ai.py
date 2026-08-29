# this file is where the AI of your opponent goes
# below is a dodgy enemy AI example

import math

cooldown = 0

def plane_ai(me, them, bullets):
    global cooldown

    a = math.atan2(me[1] - them[1], them[0] - me[0]) * 180 / math.pi

    d = ((them[0] - me[0]) ** 2 + (them[1] - me[1]) ** 2) ** 0.5

    if cooldown < 1 or d > 300:
        pass
    elif d < 300:
        a += 180
    else:
        a += 90

    if cooldown == 0:
        cooldown = 60

    cooldown -= 1

    return a, True