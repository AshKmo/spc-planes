# this file is where the AI of your opponent goes
# below is a dodgy enemy AI example

import math

cooldown = 0

def plane_ai(me, them, bullets):
    global cooldown

    a = math.atan2(me.y - them.y, them.x - me.x) * 180 / math.pi

    d = ((them.x - me.x) ** 2 + (them.y - me.y) ** 2) ** 0.5

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
