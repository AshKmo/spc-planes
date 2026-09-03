import numpy as np
from constants import (
    GAME_WIDTH,
    GAME_HEIGHT,
    TICK_TIME,
    TIME_LIMIT,
    PLANE_SPEED,
    PLANE_TURN_SPEED,
    PLANE_SHOOT_COOLDOWN,
    PLANE_RADIUS,
    PLANE_HEALTH,
    BULLET_SPAWN_DISTANCE,
    BULLET_SPEED,
    BULLET_RADIUS,
    BULLET_LIFETIME,
)



last_enemy_x = None
last_enemy_y = None

def plane_ai(me, them, bullets):
    global last_enemy_x
    global last_enemy_y


    my_np_array = np.array([me.x, me.y])
    them_np_array = np.array([them.x, them.y])

    next_x = 0
    next_y = 0

    if last_enemy_x is None:
        last_enemy_x = them.x
        last_enemy_y = them.y
        next_x = them.x
        next_y = them.y

    else:
        enemy_dx = them.x - last_enemy_x
        enemy_dy = them.y - last_enemy_y

        distance = np.linalg.norm(my_np_array - them_np_array)
        time = distance / BULLET_SPEED

        next_x = them.x + enemy_dx * time
        next_y = them.y + enemy_dy * time

    a = np.atan2(next_y - me.y, next_x - me.x)

    last_enemy_x = them.x
    last_enemy_y = them.y

    return 0, np.degrees(a), True