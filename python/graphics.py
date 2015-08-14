import driver
import itertools
import math
import os.path
import json
import time

class Display(object):
    def __init__(self, width=112, height=15):
        self.width = width
        self.height = height
        self.buffer = [0] * height
        for i in range(height):
            self.buffer[i] = [0] * width;

    def clear(self):
        for r in range(self.height):
            for c in range(self.width):
                self.buffer[r][c] = 0

    def draw(self, serial_driver):
        serial_driver.draw(itertools.chain.from_iterable(self.buffer))

    def __str__(self):
        l = [0] * self.height
        for r in range(self.height):
            l[r] = ''.join('#' if i else ' ' for i in self.buffer[r]) + '\n'
        return ''.join(l)

class Sprite(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.visible = 1

    def draw(self, display):
        pass

class DisplayBox(Sprite):
    def __init__(self, *args, width=112, height=15, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height
        self.buffer = [0] * height
        self.sprites = set()
        for i in range(height):
            self.buffer[i] = [0] * width

    def add(self, sprite):
        self.sprites.add(sprite)

    def clear_sprites(self):
        self.sprites.clear()

    def clear(self):
        for r in range(self.height):
            for c in range(self.width):
                self.buffer[r][c] = 0

    def draw(self, display):
        if not self.visible:
            return

        self.clear()
        for sprite in self.sprites:
            sprite.draw(self)
        for row in range(0, self.height):
            for col in range(0, self.width):
                # It must be within both the actual and the virtual display
                # bounds in order to be drawn.
                if (0 <= row < self.height) \
                        and (0 <= self.y + row < display.height) \
                        and (0 <= col < self.width) \
                        and (0 <= self.x + col < display.width):
                    display.buffer[self.y + row][self.x + col] = self.buffer[row][col]


class Rectangle(Sprite):
    def __init__(self, width, height, *args, wrapx=False, wrapy=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height

        self.wrapx = wrapx
        self.wrapy = wrapy

    def draw(self, display):
        if not self.visible:
            return

        for r in range(round(self.y), round(self.y + self.height)):
            for c in range(round(self.x), round(self.x + self.width)):
                if (0 <= r < display.height or self.wrapy) and (0 <= c < display.width or self.wrapx):
                    display.buffer[r % display.height][c % display.width] = 1

class Circle(Sprite):
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    def draw(self, display):
        if not self.visible:
            return

        for r in range(
                max(int(self.y - self.radius + 0.5), 0),
                min(int(self.y + self.radius + 0.5) + 1, display.height)):
            for c in range(
                    max(int(self.x - self.radius + 0.5), 0),
                    min(int(self.x + self.radius + 0.5) + 1, display.width)):
                dx = c - self.x
                dy = r - self.y
                if math.sqrt(dx*dx + dy*dy) < self.radius:
                    display.buffer[r][c] = 1


class CharacterSprite(Sprite):
    class FontError(Exception): pass
    class FontNotImplementedError(FontError): pass
    fontspecs = {}

    def __init__(self, letter, *args, width=4, height=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = letter
        self.width  = width
        self.height = height

        # If not loaded, load the appropriate font size from a file.
        dimensionstr = "%dx%d" % (width, height)
        if (dimensionstr not in type(self).fontspecs):
            try:
                with open(os.path.join(os.path.dirname(
                        os.path.abspath(__file__)), "font",
                        "%s.json" % dimensionstr), 'r') as f:
                    type(self).fontspecs[dimensionstr] = json.load(f)
            except FileNotFoundError as e:
                raise type(self).FontNotImplementedError(dimensionstr)
            # except ValueError as e:
            #     raise type(self).FontError(str(e))

        self.fontspec = type(self).fontspecs[dimensionstr]

    def draw(self, display):
        if not self.visible:
            return

        # Get the letter, or a block if not available
        # XXX: document the uppercase more explicitly
        tfmatrix = self.fontspec.get(self.letter.upper(),
                [[1]*self.width]*self.height)
        for rownum, row in enumerate(tfmatrix):
            for colnum, pixel in enumerate(row):
                if (0 <= rownum + self.y < display.height) and (0 <= colnum +
                        self.x < display.width):
                    display.buffer[rownum + self.y][colnum + self.x] = pixel

class TextSprite(Sprite):
    def __init__(self, text, *args, width=4, height=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height
        self.set_text(text)

    def set_text(self, text):
        self.text = text.upper()
        self.sprites = [CharacterSprite(c, y=self.y, width=self.width, height=self.height) for c in self.text]

    def size(self):
        return (self.width + 1) * len(self.sprites)

    def draw(self, display):
        if not self.visible:
            return

        for i, x in enumerate(range(
                int(self.x),
                int(self.x + (self.width + 1) * len(self.sprites)), self.width + 1)):
            self.sprites[i].x = x
            self.sprites[i].y = self.y

        for sprite in self.sprites:
            sprite.draw(display)

class Animator(Sprite):
    def __init__(self, targets, attr="x", max=112, min=0,
                 step=1, delay=1, pause=0, loop=False, reverse=False):
        self.targets = [targets] if isinstance(targets, Sprite) else targets
        self.step = step
        self.pause = pause
        self.attr = attr
        self.min = min
        self.max = max
        self.loop = loop
        self.reverse = reverse
        self.delay = delay
        self.next_animate = time.time() + delay

    def draw(self, display):
        for s in self.targets:
            if time.time() >= self.next_animate:
                self.next_animate = time.time() + self.delay
                setattr(s, self.attr, getattr(s, self.attr) + self.step)

                if getattr(s, self.attr) > self.max:
                    if self.loop:
                        # simulate it wrapping around to the next location
                        setattr(s, self.attr, self.min + (getattr(s, self.attr) - self.max))
                    elif self.reverse:
                        # simulate it hitting the end and bouncing back
                        self.step = -self.step
                        setattr(s, self.attr, self.max - (getattr(s, self.attr) - self.max))
                    if self.pause:
                        self.next_animate += self.pause

                elif getattr(s, self.attr) < self.min:
                    if self.loop:
                        setattr(s, self.attr, self.max - (self.min - getattr(s, self.attr)))
                    elif self.reverse:
                        self.step = -self.step
                        setattr(s, self.attr, self.min + (self.min - getattr(s, self.attr)))

                    if self.pause:
                        self.next_animate += self.pause


if __name__ == '__main__':
    disp = Display()
    circ = Circle(4, 15/2+1, 15/2)
    rect = Rectangle(3, 4, 25, 5)
    wrect = Rectangle(4, 4, 0, -1, wrapx=True, wrapy=True)
    charH = CharacterSprite("H", x=31, y=5)
    charI = CharacterSprite("I", x=36, y=5)
    dispbox = DisplayBox(x=20, y=12, width=5, height=5)
    rectbox = Rectangle(10, 10, 0, 0)

    dispbox.add(rectbox)

    world = TextSprite("World", x=41, y=5)

    circ.draw(disp)
    rect.draw(disp)
    wrect.draw(disp)
    charH.draw(disp)
    charI.draw(disp)
    world.draw(disp)
    dispbox.draw(disp)

    print(disp)
