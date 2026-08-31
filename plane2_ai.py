# this file is where the AI of your opponent goes
# below is a dodgy enemy AI example

import numpy as np

def angle_diff(a, b):
    return (a - b + 180) % 360 - 180

def plane_ai(me, them, bullets):
    at = np.atan2(me.y - them.y, them.x - me.x)
    p = np.array([me.x, me.y])

    a = at if me.shoot_cooldown < 20 and np.linalg.norm(p - np.array([400, 300])) < 200 else np.atan2(me.y - 300, 400 - me.x)

    closest = 1e9
    for bullet in bullets:
        ba = np.radians(bullet.rotation)
        rp = p - np.array([bullet.x, bullet.y])
        bd = np.array([np.cos(ba), -np.sin(ba)])

        dotd = rp.dot(bd)
        dotr = rp.dot(np.array([bd[1], -bd[0]]))

        if -10 < dotd <= 120 and abs(dotr) <= 40 and dotd < closest:
            closest = dotd
            a = ba + (90 if dotr > 0 else -90)

    return np.degrees(a), True