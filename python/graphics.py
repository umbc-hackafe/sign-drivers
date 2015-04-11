import itertools
import driver

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

class Sprite(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def draw(self, display):
        pass


        
