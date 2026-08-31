# this file is where the AI of your opponent goes
#
# DEMO AI: "The Kiter"
#
# Role in the demo pair: ash_ai.py is a brawler - it rallies to the center
# of the map and, once close, gets aggressive and sprays shots liberally.
# This AI is the opposite philosophy: it treats distance as a resource.
# It tries to stay near KITE_RANGE from the enemy at all times, backing off
# if they close in and re-approaching if they run. It only commits to
# firing when its nose is well-aligned with the enemy (tight aim window),
# rather than spraying on cooldown - so on stream it should read as
# "patient and precise" next to ash's "aggressive and relentless".
#
# This is a demo/reference AI for contestants, not a tuned meta-strategy -
# feel free to read through it as a template for structuring your own.

import numpy as np

KITE_RANGE = 130  # preferred standoff distance from the enemy - close
# enough that shots actually land at a decent rate,
# far enough to still read as "kiting" vs a brawl
KITE_BAND = 35  # how much slack before we start closing/retreating
AIM_WINDOW = 25  # degrees of nose misalignment we tolerate before firing
STRAFE_DIRECTION = 1  # 1 = clockwise strafe, -1 = counter-clockwise
STRAFE_AIM_BIAS = 0.5  # 0 = pure sideways strafe, 1 = nose always on enemy
# (needs to be >0 or the plane swings broadside and
# can never line up a shot while holding range)

# bullet dodge tuning (same cone-check idea as ash_ai.py)
DODGE_FORWARD_MIN = -10
DODGE_FORWARD_MAX = 140  # kiter looks a bit further ahead than ash since
# it's not committed to closing distance anyway
DODGE_SIDE_MAX = 45


def angle_diff(a, b):
    """Smallest signed difference a - b, wrapped to [-180, 180]."""
    return (a - b + 180) % 360 - 180


def plane_ai(me, them, bullets):
    p = np.array([me.x, me.y])
    e = np.array([them.x, them.y])

    to_enemy = e - p
    dist = np.linalg.norm(to_enemy)

    # bearing straight at the enemy (screen y grows downward, so flip y
    # like ash_ai.py does to get a normal math angle)
    angle_to_enemy = np.degrees(np.arctan2(-to_enemy[1], to_enemy[0]))

    # --- movement: hold at KITE_RANGE, strafing sideways rather than
    # sitting still, so we're not just parked as an easy target ---
    strafe_tangent = angle_to_enemy + STRAFE_DIRECTION * 90

    if dist > KITE_RANGE + KITE_BAND:
        # enemy is far - close the gap
        desired_angle = angle_to_enemy
        speed = 1.0
    elif dist < KITE_RANGE - KITE_BAND:
        # enemy is too close - back off (fly away from them)
        desired_angle = (angle_to_enemy + 180) % 360
        speed = 1.0
    else:
        # in the sweet spot - strafe sideways to stay evasive, but bias the
        # heading toward the enemy so the nose can still track them; a pure
        # 90-degree strafe makes the plane fly broadside and it can never
        # line up a shot (the turn takes many ticks, fighting the aim check
        # the whole time)
        desired_angle = strafe_tangent + STRAFE_AIM_BIAS * angle_diff(
            angle_to_enemy, strafe_tangent
        )
        speed = 0.8

    # --- bullet dodging takes priority over the kiting movement ---
    closest = 1e9
    dodge_angle = None
    for bullet in bullets:
        ba = np.radians(bullet.rotation)
        rel = p - np.array([bullet.x, bullet.y])
        bullet_dir = np.array([np.cos(ba), -np.sin(ba)])

        # component of our offset along the bullet's travel direction,
        # and perpendicular to it
        along = rel.dot(bullet_dir)
        side = rel.dot(np.array([bullet_dir[1], -bullet_dir[0]]))

        if (
            DODGE_FORWARD_MIN < along <= DODGE_FORWARD_MAX
            and abs(side) <= DODGE_SIDE_MAX
            and along < closest
        ):
            closest = along
            dodge_angle = np.degrees(ba) + (90 if side > 0 else -90)

    if dodge_angle is not None:
        desired_angle = dodge_angle

    # --- firing: only shoot when the nose is actually lined up, not on
    # every available cooldown tick. this is the core contrast with
    # ash_ai.py's "shoot whenever possible" approach ---
    aim_error = abs(angle_diff(angle_to_enemy, me.rotation))
    shooting = aim_error < AIM_WINDOW

    return speed, desired_angle % 360, shooting
