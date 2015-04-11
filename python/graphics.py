import driver
import itertools
import math

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

if __name__ == '__main__':
    disp = Display()
    circ = Circle(4, 15/2+1, 15/2)
    rect = Rectangle(3, 4, 25, 5)
    wrect = Rectangle(4, 4, 0, -1, wrapx=True, wrapy=True)

    circ.draw(disp)
    rect.draw(disp)
    wrect.draw(disp)

    print(disp)
