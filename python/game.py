import time
import queue

class Game:
    def __init__(self, graphics, serial, framerate=30):
        self.graphics = graphics
        self.serial = serial
        self.sprites = set()
        self.framerate = framerate
        self.input_queue = queue.Queue()

    def send_input(self, name):
        self.input_queue.put(name)

    def loop(self):
        self.graphics.clear()
        for sprite in self.sprites:
            sprite.draw(self.graphics)

        self.graphics.draw(self.serial)
        time.sleep(1 / self.framerate)

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.loop()