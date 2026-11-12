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


# ==============================
# BRICK
# ==============================

class Brick(GameObject):

    COLORS = {
        1: "#F7B6C8",
        2: "#DCCCF4",
        3: "#F9D3B9"
    }

    def __init__(self, canvas, x, y, hits):
        self.width = 78
        self.height = 22
        self.hits = hits

        color = self.COLORS[hits]

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill=color,
            outline=WHITE,
            width=2,
            tags="brick"
        )

        super().__init__(canvas, item)

    def hit(self):
        self.hits -= 1

        if self.hits <= 0:
            self.delete()
            return True

        self.canvas.itemconfig(
            self.item,
            fill=self.COLORS[self.hits]
        )

        return False


# ==============================
# PARTICLE EFFECT
# ==============================

class Particle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)

        self.life = 15

        color = random.choice([
            PINK, DARK_PINK, WHITE, LAVENDER, PEACH
        ])

        self.item = canvas.create_oval(
            x, y, x + 6, y + 6,
            fill=color,
            outline=""
        )

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

        self.canvas.move(
            self.item,
            self.dx,
            self.dy
        )

        if self.life <= 0:
            self.canvas.delete(self.item)
            return False

        return True


# ==============================
# MAIN GAME
# ==============================

class Game(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.width = 760
        self.height = 560

        self.level = 1
        self.score = 0
        self.lives = 3

        self.running = False
        self.particles = []

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg=BG,
            highlightthickness=0
        )

        self.canvas.pack()
        self.pack()

        self.draw_background()

        self.paddle = Paddle(
            self.canvas,
            self.width / 2,
            505
        )

        self.ball = None
        self.bricks = {}
        self.hud = None

        self.create_hud()
        self.create_level()

        self.add_ball()

        self.show_message(
            "♡ FLOWER BREAKER ♡",
            "Press SPACE to start"
        )

        self.canvas.focus_set()

        self.canvas.bind(
            "<Left>",
            lambda e: self.paddle.move_paddle(-20)
        )

        self.canvas.bind(
            "<Right>",
            lambda e: self.paddle.move_paddle(20)
        )

        self.canvas.bind(
            "<space>",
            lambda e: self.start_game()
        )

    # ==========================
    # BACKGROUND DECORATION
    # ==========================

    def draw_flower(self, x, y, size=10):

        for angle in range(0, 360, 72):
            rad = math.radians(angle)

            px = x + math.cos(rad) * size
            py = y + math.sin(rad) * size

            self.canvas.create_oval(
                px - size / 1.5,
                py - size / 1.5,
                px + size / 1.5,
                py + size / 1.5,
                fill="#F8C6D4",
                outline=""
            )

        self.canvas.create_oval(
            x - 5, y - 5,
            x + 5, y + 5,
            fill="#F5D89A",
            outline=""
        )

    def draw_background(self):

        # Decorative flowers
        self.draw_flower(30, 45, 9)
        self.draw_flower(725, 45, 9)
        self.draw_flower(35, 535, 8)
        self.draw_flower(725, 535, 8)

        self.draw_flower(150, 30, 5)
        self.draw_flower(610, 30, 5)

        # Small sparkles
        for i in range(35):
            x = random.randint(15, self.width - 15)
            y = random.randint(15, self.height - 15)

            self.canvas.create_text(
                x, y,
                text=random.choice(["✦", "♡", "·"]),
                fill=random.choice([
                    "#F2B7C8",
                    "#E5C9ED",
                    "#F5D5BD"
                ]),
                font=("Arial", random.randint(9, 16))
            )

        # Decorative border
        self.canvas.create_rectangle(
            8, 8,
            self.width - 8,
            self.height - 8,
            outline="#F3C5D2",
            width=2
        )

        self.canvas.create_text(
            380, 65,
            text="✿  BLOOM & PLAY  ✿",
            font=("Georgia", 18, "bold"),
            fill=TEXT
        )

        self.canvas.create_text(
            380, 90,
            text="A little game full of flowers",
            font=("Georgia", 10, "italic"),
            fill=DARK_PINK
        )