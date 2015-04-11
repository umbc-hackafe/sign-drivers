import driver
import itertools
import math
import json

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
    
    def draw(self, display):
        pass

class Rectangle(Sprite):
    def __init__(self, width, height, *args, wrapx=False, wrapy=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height

        self.wrapx = wrapx
        self.wrapy = wrapy

    def draw(self, display):
        for r in range(round(self.y), round(self.y + self.height)):
            for c in range(round(self.x), round(self.x + self.width)):
                if (0 < r < display.height or self.wrapy) and (0 < c < display.width or self.wrapx):
                    display.buffer[r % display.height][c % display.width] = 1

class Circle(Sprite):
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    def draw(self, display):
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
    # XXX: replace hardcoding here
    with open('font/4x4.json', 'r') as f:
        fontspec = json.load(f)

    def __init__(self, letter, *args, width=4, height=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter = letter
        self.width  = width
        self.height = height

    def draw(self, display):
        # Get the letter, or a block if not available
        # XXX: document the uppercase more explicitly
        tflist = type(self).fontspec.get(self.letter.upper(), type(self).fontspec["__block__"])
        # Split the list into a nice matrix
        tfmatrix = ((tflist[i:i+self.width] for i in range(0, len(tflist), self.width)))
        for rownum, row in enumerate(tfmatrix):
            for colnum, pixel in enumerate(row):
                if (0 < rownum + self.y < display.height) and (0 < colnum +
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
        

    def draw(self, display):
        for i, x in enumerate(range(
                int(self.x),
                int(self.x + (self.width + 1) * len(self.sprites)), self.width + 1)):
            self.sprites[i].x = x
            self.sprites[i].y = self.y

        for sprite in self.sprites:
            sprite.draw(display)
                       
if __name__ == '__main__':
    disp = Display()
    circ = Circle(4, 15/2+1, 15/2)
    rect = Rectangle(3, 4, 25, 5)
    wrect = Rectangle(4, 4, 0, -1, wrapx=True, wrapy=True)
    charH = CharacterSprite("H", x=31, y=5)
    charI = CharacterSprite("I", x=36, y=5)

    world = TextSprite("World", x=41, y=5)

    circ.draw(disp)
    rect.draw(disp)
    wrect.draw(disp)
    charH.draw(disp)
    charI.draw(disp)
    world.draw(disp)

    print(disp)
