import tkinter as tk
import random
import math


# ==============================
# PASTEL PINK COLOR PALETTE
# ==============================

BG = "#FFF3F6"
PINK = "#F4A7B9"
DARK_PINK = "#C96F8C"
LIGHT_PINK = "#FFDCE5"
LAVENDER = "#DCCCF4"
PEACH = "#FFD8C2"
CREAM = "#FFF9F0"
WHITE = "#FFFFFF"
TEXT = "#9D6075"


# ==============================
# GAME OBJECT
# ==============================

class GameObject:
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


# ==============================
# BALL
# ==============================

class Ball(GameObject):
    def __init__(self, canvas, x, y, speed):
        self.radius = 9
        self.direction = [random.choice([-1, 1]), -1]
        self.speed = speed

        item = canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill=WHITE,
            outline=PINK,
            width=3,
            tags="ball"
        )

        super().__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1

        if coords[1] <= 0:
            self.direction[1] = 1

        self.move(
            self.direction[0] * self.speed,
            self.direction[1] * self.speed
        )


# ==============================
# PADDLE
# ==============================

class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 100
        self.height = 13

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill=DARK_PINK,
            outline="#E9A0B3",
            width=2,
            tags="paddle"
        )

        super().__init__(canvas, item)

    def move_paddle(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            self.move(offset, 0)