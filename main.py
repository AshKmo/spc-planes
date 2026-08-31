from PIL import Image, ImageTk
import numpy as np
from dataclasses import dataclass

import tkinter as tk
from tkinter import messagebox
from time import time

import plane1_ai
import plane2_ai

GAME_WIDTH = 800
GAME_HEIGHT = 600

TICK_TIME = 1000 / 50

TIME_LIMIT = 1500

PLANE_SPEED = 4
PLANE_TURN_SPEED = 10
PLANE_SHOOT_COOLDOWN = 30
PLANE_RADIUS = 10
PLANE_HEALTH = 5

BULLET_SPAWN_DISTANCE = 11
BULLET_SPEED = 8
BULLET_RADIUS = 5
BULLET_LIFETIME = 60

image_plane1 = Image.open("assets/plane1.png")
image_plane2 = Image.open("assets/plane2.png")
image_bullet = Image.open("assets/bullet.png")

def flip_angle(a: float) -> float:
    return (180 - a) % 360

def angle_to_vector(a: float) -> np.ndarray:
    a = np.radians(a)
    return np.array([np.cos(a), -np.sin(a)])

def angle_diff(a, b):
    return (a - b + 180) % 360 - 180

class Plane:
    @dataclass
    class PlaneData:
        x: float
        y: float
        rotation: float
        health: int
        shoot_cooldown: int

    def __init__(self: Plane, canvas: tk.Canvas, name: str, image: Image, ai: callable[[PlaneData, PlaneData, list[Bullet.BulletData]], (int, bool)], position: np.ndarray, rotation: float, flipped: bool = False):
        self.canvas = canvas
        self.name = name

        self.image = image
        self.tk_image = self.canvas.create_image((0, 0))
        self.rendered_image = None

        self.tk_health_text = canvas.create_text((0, 0), font=(None, 16), fill="white")

        self.ai = ai
        self.position = position

        self.rotation = rotation % 360
        self.desired_rotation = self.rotation

        self.flipped = flipped
        self.health = PLANE_HEALTH
        self.shoot_cooldown = 0
        self.shooting = False

    def get_data(self, flipped=False) -> PlaneData:
        return self.PlaneData(
                GAME_WIDTH - self.position[0] if flipped else self.position[0],
                self.position[1],
                flip_angle(self.rotation) if flipped else self.rotation,
                self.health,
                self.shoot_cooldown
                )

    def call_ai(self: Plane, enemy: Plane, bullets: list[Bullet]) -> tuple[float, bool]:
        results = self.ai(self.get_data(flipped=self.flipped), enemy.get_data(flipped=self.flipped), [b.get_data(flipped=self.flipped) for b in bullets])
        new_rotation: float = results[0]
        shooting: bool = results[1]
        return flip_angle(new_rotation) if self.flipped else new_rotation % 360, shooting

    def update_graphics(self):
        self.rendered_image = ImageTk.PhotoImage(self.image.rotate(self.rotation, expand=True))
        self.canvas.coords(self.tk_image, self.position[0], self.position[1])
        self.canvas.itemconfigure(self.tk_image, image=self.rendered_image)

        self.canvas.coords(self.tk_health_text, *np.clip([self.position[0], self.position[1] - 30], min=[20, 20], max=[GAME_WIDTH - 20, GAME_HEIGHT - 20]))
        self.canvas.itemconfigure(self.tk_health_text, text=f"{self.health}")

    def destroy(self):
        self.canvas.delete(self.tk_image)
        self.canvas.delete(self.tk_health_text)

class Bullet:
    @dataclass
    class BulletData:
        x: float
        y: float
        rotation: float
        lifetime: int

    def __init__(self: Bullet, canvas: tk.Canvas, image: Image, position: np.ndarray, rotation: float):
        self.canvas = canvas

        self.image = image
        self.tk_image = self.canvas.create_image((0, 0))
        self.rendered_image = None

        self.position = position
        self.rotation = rotation
        self.lifetime = BULLET_LIFETIME
    
    def get_data(self, flipped=False) -> BulletData:
        return self.BulletData(
                GAME_WIDTH - self.position[0] if flipped else self.position[0],
                self.position[1],
                flip_angle(self.rotation) if flipped else self.rotation,
                self.lifetime
                )

    def update_graphics(self):
        self.canvas.coords(self.tk_image, self.position[0], self.position[1])
        self.rendered_image = ImageTk.PhotoImage(self.image.rotate(self.rotation, expand=True))
        self.canvas.itemconfigure(self.tk_image, image=self.rendered_image)

    def destroy(self):
        self.canvas.delete(self.tk_image)

root = tk.Tk()
root.title("Planes!")
root.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")

canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg="black")
canvas.pack()

tk_game_time_text = canvas.create_text((10, 10), font=(None, 20), fill="white", anchor="nw")

plane1 = Plane(
        canvas,
        "Plane 1",
        image_plane1,
        plane1_ai.plane_ai,
        np.array([100, GAME_HEIGHT / 2]),
        0
        )

plane2 = Plane(
        canvas,
        "Plane 2",
        image_plane2,
        plane2_ai.plane_ai,
        np.array([GAME_WIDTH - 100, GAME_HEIGHT / 2]),
        180,
        True
        )
 
planes: list[Plane] = [plane1, plane2]
bullets: list[Bullet] = []

time_profit = 0

last_tick_time = time()

game_timer = TIME_LIMIT

def tick():
    global game_timer
    global last_tick_time
    global time_profit
    global planes
    global bullets

    plane1_new_rotation, plane1_shooting = plane1.call_ai(plane2, bullets)
    plane2_new_rotation, plane2_shooting = plane2.call_ai(plane1, bullets)

    plane1.desired_rotation = plane1_new_rotation
    plane1.shooting = plane1_shooting

    plane2.desired_rotation = plane2_new_rotation
    plane2.shooting = plane2_shooting

    for plane in planes:
        ad = angle_diff(plane.desired_rotation, plane.rotation)
        plane.rotation = (plane.rotation + np.sign(ad) * min(PLANE_TURN_SPEED, abs(ad))) % 360
        plane_direction = angle_to_vector(plane.rotation)
        plane.position = np.clip(plane.position + PLANE_SPEED * plane_direction, min=[0,0], max=[GAME_WIDTH-1,GAME_HEIGHT-1])

        if plane.shoot_cooldown <= 0:
            if plane.shooting:
                bullets.append(Bullet(
                    canvas,
                    image_bullet,
                    plane.position + BULLET_SPAWN_DISTANCE * plane_direction,
                    plane.rotation
                    ))

                plane.shoot_cooldown = PLANE_SHOOT_COOLDOWN
        else:
            plane.shoot_cooldown -= 1

    for bullet in bullets:
        bullet.position = bullet.position + BULLET_SPEED * angle_to_vector(bullet.rotation)

        bullet.update_graphics()

    for plane in planes:
        for bullet in bullets:
            if np.linalg.norm(bullet.position - plane.position) <= PLANE_RADIUS + BULLET_RADIUS:
                plane.health -= 1
                bullet.lifetime = 0

    for bullet in [*bullets]:
        if bullet.lifetime <= 0:
            bullets.remove(bullet)
            bullet.destroy()

    for plane in [*planes]:
        if plane.health <= 0:
            planes.remove(plane)
            plane.destroy()

    for plane in planes:
        plane.update_graphics()

    for bullet in bullets:
        bullet.update_graphics()
        bullet.lifetime -= 1

    if game_timer <= 0:
        planes = []
    else:
        game_timer -= 1

    canvas.itemconfigure(tk_game_time_text, text=f"{TICK_TIME * game_timer / 1000}")

    match len(planes):
        case 0:
            messagebox.showinfo("Game over", "It's a draw!")
            root.quit()
        case 1:
            messagebox.showinfo("Game over", f"{planes[0].name} wins!")
            root.quit()
        case _:
            new_time = time()
            dt = new_time - last_tick_time
            last_tick_time = new_time
            time_profit += TICK_TIME - dt * 1000
            root.after(max(0, int(time_profit)), tick)

tick()

root.mainloop()
