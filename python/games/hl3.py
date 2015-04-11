import graphics
import driver
import game
import math

HL3_LOGO = [[5, 5, 5, 5, 5, 5, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]

class HL3(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.timer = graphics.Rectangle(1, 7, x=20, y=8)
        self.loading = graphics.TextSprite("Loading...", width=5, height=7, x=20, y=0)
        self.max_width = 112-20
        self.time = 2

        self.hl3 = set()

        for y in range(len(HL3_LOGO)):
            for x in range(len(HL3_LOGO[y])):
                if HL3_LOGO[y][x]:
                    self.sprites.add(graphics.Rectangle(1, 1, x=x, y=y))
        self.sprites.add(self.timer)
        self.sprites.add(self.loading)

    def loop(self):
        self.time += 1

        self.timer.width = int(math.log(self.time, 3600 * 24 * 36) * self.max_width)
        super().loop()

GAME = HL3
