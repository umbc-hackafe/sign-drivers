import graphics
import driver
import game

class PixelMan(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pixel = graphics.Rectangle(1, 1, x=56, y=8)
        self.sprites.add(self.pixel)

    def loop(self):
        while not self.input_queue.empty():
            evt = self.input_queue.get().upper()
            if evt == "W":
                self.pixel.y -= 1
            elif evt == "A":
                self.pixel.x -= 1
            elif evt == "S":
                self.pixel.y += 1
            elif evt == "D":
                self.pixel.x += 1

        super().loop()

GAME = PixelMan
