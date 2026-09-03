from PIL import Image, ImageTk
import numpy as np

from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
from time import time

from constants import *
import plane1_ai
import plane2_ai

image_plane1 = Image.open("assets/plane1.png")
image_plane2 = Image.open("assets/plane2.png")
image_bullet = Image.open("assets/bullet.png")

def flip_angle(a: float) -> float:
    return (180 - a) % 360

def angle_to_vector(a: float) -> np.ndarray:
    a = np.radians(a)
    return np.array([np.cos(a), np.sin(a)])

def angle_diff(a, b):
    return (a - b + 180) % 360 - 180

class Plane:
    class Bullet:
        @dataclass
        class BulletData:
            x: float
            y: float
            rotation: float
            lifetime: int

        def __init__(self, position: np.ndarray, rotation: float, canvas: tk.Canvas, truly_flipped: bool):
            self.position = position
            self.rotation = rotation
            self.lifetime = BULLET_LIFETIME

            self.new_lifetime = self.lifetime

            self.truly_flipped = truly_flipped

            self.canvas = canvas
            self.rendered_image = None
            self.tk_image = self.canvas.create_image((0, 0))

        def get_position(self, flipped = False):
            return np.array([GAME_WIDTH - self.position[0], self.position[1]]) if flipped else self.position

        def get_rotation(self, flipped = False):
            return flip_angle(self.rotation) if flipped else self.rotation

        def get_data(self, flipped = False):
            position = self.get_position(flipped)
            rotation = self.get_rotation(flipped)
            return Plane.Bullet.BulletData(position[0], position[1], rotation, self.lifetime)

        def update_graphics(self):
            position = self.get_position(self.truly_flipped)
            self.canvas.coords(self.tk_image, position[0], GAME_HEIGHT - position[1])
            self.rendered_image = ImageTk.PhotoImage(image_bullet.rotate(self.get_rotation(self.truly_flipped), expand=True))
            self.canvas.itemconfigure(self.tk_image, image=self.rendered_image)

        def destroy(self):
            self.canvas.delete(self.tk_image)

    @dataclass
    class PlaneData:
        x: float
        y: float
        rotation: float
        health: int
        shoot_cooldown: int

    def __init__(self, name: str, ai: callable[PlaneData, PlaneData, list[Bullet.BulletData]], canvas: tk.Canvas, image: Image, truly_flipped: bool):
        self.name = name
        self.position = np.array([100, GAME_HEIGHT / 2])
        self.throttle = 1
        self.rotation = 0
        self.health = PLANE_HEALTH
        self.shooting = False
        self.shoot_cooldown = 0
        self.ai = ai

        self.desired_throttle = self.throttle
        self.desired_rotation = self.rotation
        self.new_health = self.health

        self.bullets = []

        self.other_plane = None

        self.truly_flipped = truly_flipped

        self.canvas = canvas
        self.image = image
        self.tk_image = self.canvas.create_image((0, 0))
        self.rendered_image = None

        self.tk_health_text = canvas.create_text((0, 0), font=(None, 16), fill="white")

    def get_position(self, flipped = False):
        return np.array([GAME_WIDTH - self.position[0], self.position[1]]) if flipped else self.position

    def get_rotation(self, flipped = False):
        return flip_angle(self.rotation) if flipped else self.rotation

    def get_data(self, flipped = False):
        position = self.get_position(flipped)
        rotation = self.get_rotation(flipped)
        return Plane.PlaneData(position[0], position[1], rotation, self.health, self.shoot_cooldown)

    def pre_tick(self):
        desired_throttle, desired_rotation, shooting = self.ai(
            self.get_data(),
            self.other_plane.get_data(True),
            [b.get_data() for b in self.bullets] + [b.get_data(True) for b in self.other_plane.bullets]
        )

        self.desired_throttle = np.clip(float(desired_throttle), 0, 1)
        self.desired_rotation = float(desired_rotation) % 360
        self.shooting = bool(shooting)

        for bullet in self.bullets:
            bullet.new_lifetime -= 1

        for bullet in self.bullets + self.other_plane.bullets:
            position = bullet.get_position(bullet in self.other_plane.bullets)

            if np.linalg.norm(position - self.position) <= PLANE_RADIUS + BULLET_RADIUS:
                self.new_health -= 1
                bullet.new_lifetime = 0

    def post_tick(self):
        self.health = self.new_health
        self.throttle = self.desired_throttle

        for bullet in self.bullets.copy():
            bullet.lifetime = bullet.new_lifetime

            if bullet.lifetime <= 0:
                self.bullets.remove(bullet)
                bullet.destroy()

        ad = angle_diff(self.desired_rotation, self.rotation)
        self.rotation = (self.rotation + np.sign(ad) * min(PLANE_TURN_SPEED, abs(ad))) % 360
        direction = angle_to_vector(self.rotation)
        self.position = np.clip(self.position + PLANE_SPEED * self.throttle * direction, min=[0,0], max=[GAME_WIDTH,GAME_HEIGHT])

        if self.shoot_cooldown <= 0:
            if self.shooting:
                self.bullets.append(Plane.Bullet(
                    self.position + BULLET_SPAWN_DISTANCE * direction,
                    self.rotation,
                    self.canvas,
                    self.truly_flipped
                    ))

                self.shoot_cooldown = PLANE_SHOOT_COOLDOWN
        else:
            self.shoot_cooldown -= 1

        for bullet in self.bullets:
            if not 0 <= bullet.position[0] < GAME_WIDTH:
                bullet.rotation = (180 - bullet.rotation) % 360
    
            if not 0 <= bullet.position[1] < GAME_HEIGHT:
                bullet.rotation = 360 - bullet.rotation
    
            bullet.position = bullet.position + BULLET_SPEED * angle_to_vector(bullet.rotation)

            bullet.update_graphics()

        self.update_graphics()

    def update_graphics(self):
        position = self.get_position(self.truly_flipped)

        self.rendered_image = ImageTk.PhotoImage(self.image.rotate(self.get_rotation(self.truly_flipped), expand=True))
        self.canvas.coords(self.tk_image, position[0], GAME_HEIGHT - position[1])
        self.canvas.itemconfigure(self.tk_image, image=self.rendered_image)

        self.canvas.coords(self.tk_health_text, *np.clip([position[0], GAME_HEIGHT - position[1] + 30], min=[20, 20], max=[GAME_WIDTH - 20, GAME_HEIGHT - 20]))
        self.canvas.itemconfigure(self.tk_health_text, text=f"{self.health}")

root = tk.Tk()
root.title("Planes!")
root.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")

canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg="black")
canvas.pack()

tk_game_time_text = canvas.create_text((10, 10), font=(None, 20), fill="white", anchor="nw")

plane1 = Plane(
        "Plane 1",
        plane1_ai.plane_ai,
        canvas,
        image_plane1,
        False
        )

plane2 = Plane(
        "Plane 2",
        plane2_ai.plane_ai,
        canvas,
        image_plane2,
        True
        )

plane1.other_plane = plane2
plane2.other_plane = plane1

time_profit = 0

last_tick_time = time()

game_timer = TIME_LIMIT

def tick():
    global root
    global game_timer
    global last_tick_time
    global time_profit

    plane1.pre_tick()
    plane2.pre_tick()

    plane1.post_tick()
    plane2.post_tick()

    if game_timer <= 0:
        plane1.health = 0
        plane2.health = 0
    else:
        game_timer -= 1

    canvas.itemconfigure(tk_game_time_text, text=f"{TICK_TIME * game_timer / 1000}")
    
    match int(plane1.health > 0) + int(plane2.health > 0):
        case 0:
            messagebox.showinfo("Game over", "It's a draw!")
            root.quit()
        case 1:
            messagebox.showinfo("Game over", f"{(plane1 if plane1.health else plane2).name} wins!")
            root.quit()
        case _:
            new_time = time()
            dt = new_time - last_tick_time
            last_tick_time = new_time
            time_profit += TICK_TIME - dt * 1000
            root.after(max(0, int(time_profit)), tick)

tick()

root.mainloop()