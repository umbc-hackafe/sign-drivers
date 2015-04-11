import graphics
import driver
import game

class PixelMan(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pixel = graphics.Rectangle(1, 1, x=56, y=8, wrapx=True, wrapy=True)
        self.sprites.add(self.pixel)

    def loop(self):
        self.handle_events()

        if 'a' in self.keys:
            self.pixel.x -= 1
        elif 'd' in self.keys:
            self.pixel.x += 1
        if 'w' in self.keys:
            self.pixel.y -= 1
        elif 's' in self.keys:
            self.pixel.y += 1
            
        super().loop()

GAME = PixelMan
