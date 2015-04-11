import graphics
import driver
import game
import random
import string

class FlappyPixel(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reset()

    def reset(self):
        self.sprites.clear()
        self.playing = True
        
        self.flappy = graphics.Rectangle(1, 1, x=24, y=0, wrapx=False, wrapy=False)
        self.sprites.add(self.flappy)

        # XXX: hard-coded width
        self.scoretext = graphics.TextSprite("0", width=4, height=4, x=1, y=0)
        self.sprites.add(self.scoretext)

        self.terrain = self.terrain_gen()
        self.ticks = 0
        self.score = 0

        self.up = 0

    def terrain_gen(self):
        while True:
            width, height = 2, random.randint(1, 10)
            if random.randint(0, 1):
                top = 0
            else:
                top = 15 - height
            yield graphics.Rectangle(width, height, 113, top)

    def check_collision(self):
        for sprite in self.sprites:
            if sprite is self.flappy:
                continue
            if sprite.x <= self.flappy.x <= (sprite.x+sprite.width) and sprite.y <= self.flappy.y <= (sprite.y+sprite.height):
                return True
        return False

    def scroll_terrain(self):
        for sprite in list(self.sprites):
            if sprite is not self.flappy and sprite is not self.scoretext:
                sprite.x -= 1
                if sprite.x < -sprite.width:
                    self.sprites.remove(sprite)

    def loop(self):
        if self.playing:
            if set(string.ascii_lowercase + ' ').intersection(self.keys) and not self.up:
                print("AHH")
                self.up = 3

            if self.up and not self.ticks % 3:
                self.up -= 1
                self.flappy.y -= self.up
            elif not self.ticks % 4:
                self.flappy.y += 1

            if self.flappy.y > 15 or self.flappy.y < 0 or self.check_collision():
                self.sprites = set([graphics.TextSprite("GAME OVER", width=5, height=7),
                                    graphics.TextSprite("R TO RELOAD", width=5, height=7, y=8)])
                self.playing = False
                return

            if not self.ticks % 3:
                self.scroll_terrain()

            if not self.ticks % 45:
                self.sprites.add(next(self.terrain))
                self.score += 1
                self.scoretext.set_text(str(self.score))


            self.ticks += 1
        else:
            if 'r' in self.keys:
                self.reset()
            
        super().loop()

GAME = FlappyPixel
