import pygame

import plane1_ai
import plane2_ai

from types import SimpleNamespace

GAME_WIDTH = 800
GAME_HEIGHT = 600

MAX_ANGLE = 360

PLANE_SIZE = 25
BULLET_SIZE = 5

image_plane1 = pygame.image.load("assets/plane1.png")
image_plane2 = pygame.image.load("assets/plane2.png")

image_bullet = pygame.image.load("assets/bullet.png")


class Plane:
    def __init__(self, name, image, p, r, ai_f):
        self.image = image
        self.p = p
        self.r = r
        self.ai_f = ai_f or (lambda *x: (10, True))
        self.shooting = False
        self.shoot_cooldown = 0
        self.health = 5
        self.name = name


class Bullet:
    def __init__(self, p, r):
        self.p = p
        self.r = r
        self.hit = False
        self.life = 100


pygame.init()

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()

running = True

plane1 = Plane(
    "PLANE1 (BLUE)", image_plane1, pygame.math.Vector2(100, 300), 0, plane1_ai.plane_ai
)
plane2 = Plane(
    "PLANE2 (RED)", image_plane2, pygame.math.Vector2(700, 300), 180, plane2_ai.plane_ai
)

planes = [plane1, plane2]


def flip_angle(a):
    return (MAX_ANGLE / 2 - a) % 360


bullets = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    (plane1.r, plane1.shooting) = plane1.ai_f(
        SimpleNamespace(x = plane1.p.x, y = plane1.p.y, rot = plane1.r),
        SimpleNamespace(x = plane2.p.x, y = plane2.p.y, rot=  plane2.r),
        [SimpleNamespace(x=b.p.x, y=b.p.y, rot=b.r) for b in bullets],
    )
    (plane2.r, plane2.shooting) = plane2.ai_f(
        SimpleNamespace(
            x = GAME_WIDTH - plane2.p.x,
            y = plane2.p.y,
            rot = flip_angle(plane2.r),
        ),
        SimpleNamespace(
            x = GAME_WIDTH - plane1.p.x,
            y = plane1.p.y,
            rot = flip_angle(plane1.r),
        ),
        [SimpleNamespace(x=GAME_WIDTH - b.p.x, y=b.p.y, rot=flip_angle(b.r)) for b in bullets],
    )
    plane1.r = plane1.r % 360
    plane2.r = flip_angle(plane2.r)

    screen.fill("black")

    for plane in planes:
        plane.p = plane.p + pygame.math.Vector2.from_polar((4, -plane.r))

        plane.p.update(
            min(max(plane.p.x, 0), GAME_WIDTH), min(max(plane.p.y, 0), GAME_HEIGHT)
        )

        if plane.shooting and plane.shoot_cooldown == 0:
            plane.shoot_cooldown = 60

            bullets.append(
                Bullet(
                    plane.p
                    + pygame.math.Vector2.from_polar((PLANE_SIZE + 5, -plane.r)),
                    plane.r,
                )
            )

        if plane.shoot_cooldown > 0:
            plane.shoot_cooldown -= 1

        screen.blit(
            pygame.transform.rotate(plane.image, plane.r),
            (plane.p.x - 25, plane.p.y - 25),
        )

    for bullet in bullets:
        bullet.p = bullet.p + pygame.math.Vector2.from_polar((8, -bullet.r))

        bullet.life -= 1

        screen.blit(
            pygame.transform.rotate(image_bullet, bullet.r),
            (bullet.p.x - 5, bullet.p.y - 5),
        )

    for bullet in bullets:
        for plane in planes:
            if bullet.p.distance_to(plane.p) <= BULLET_SIZE + PLANE_SIZE:
                plane.health -= 1
                bullet.life = 0

    bullets = [
        b
        for b in bullets
        if b.life > 0
        and pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT).collidepoint(b.p.x, b.p.y)
    ]

    planes = [p for p in planes if p.health > 0]

    if len(planes) == 0:
        print("\nTIE")
        running = False
    elif len(planes) == 1:
        print(f"\n{planes[0].name} WINS!")
        running = False

    pygame.display.flip()

    clock.tick(50)

pygame.quit()
