import driver
import game
import graphics
import itertools
import random
import time
import sys


class Lug(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.modes = [
            self.normal_mode,
            self.blink_mode,
            self.bounce_mode,
        ]

        self.cycle = itertools.chain.from_iterable(
            map(lambda x: random.shuffle(x) or x, itertools.repeat(self.modes)))

        self.current = next(self.cycle)()

    def loop(self):
        super().loop()

        try:
            next(self.current)
        except StopIteration:
            self.current = next(self.cycle)()


    def normal_mode(self):
        label = graphics.TextSprite('LINUX USERS GROUP', width=5, height=7, x=5, y=4)
        label.x = 5
        label.y = 4
        self.sprites.add(label)

        run_until = time.time() + random.uniform(5, 10)

        while time.time() < run_until:
            yield

        self.sprites.remove(label)

    def blink_mode(self):
        label = graphics.TextSprite('LINUX USERS GROUP', width=5, height=7, x=5, y=4)
        label.x = 5
        label.y = 4
        self.sprites.add(label)

        run_until = time.time() + random.uniform(5, 10)
        blink_at = time.time() + 0.5

        while time.time() < run_until:
            if blink_at < time.time():
                blink_at = time.time() + 0.5
                if label in self.sprites:
                    self.sprites.remove(label)
                else:
                    self.sprites.add(label)
            yield

        if label in self.sprites:
            self.sprites.remove(label)

    def bounce_mode(self):
        label = graphics.TextSprite('LINUX USERS GROUP', width=5, height=7, x=5, y=4)
        label.x = 5
        label.y = 4
        self.sprites.add(label)

        run_until = time.time() + random.uniform(5, 10)

        vx = random.choice([-1, 1])
        vy = random.choice([-1, 1])

        while time.time() < run_until:
            label.x += vx
            label.y += vy

            if label.x == 0 and vx < 0:
                vx = -vx
            if label.y == 0 and vy < 0:
                vy = -vy
            if label.x + (label.width + 1) * len(label.sprites) == 112 and vx > 0:
                vx = -vx
            if label.y + label.height == 15 and vy > 0:
                vy = -vy
            yield
            yield

        self.sprites.remove(label)


GAME = Lug
