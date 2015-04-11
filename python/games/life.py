from scipy.signal import convolve2d
import numpy as np
import graphics
import random
import driver
import game
import time

rows = 15
cols = 112

class Life(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = time.time()
        self.randomize()

    def randomize(self):
        self.graphics.buffer = [[random.getrandbits(1) for y in range(cols)] for x in range(rows)]

    def recv_input(self, evt):
        self.randomize()

    def loop(self):
        while not self.input_queue.empty():
            evt = self.input_queue.get()
            self.recv_input(evt)

        nbrs_count = convolve2d(self.graphics.buffer, np.ones((3, 3)), mode='same', boundary='wrap') - self.graphics.buffer
        self.graphics.buffer =  (nbrs_count == 3) | (self.graphics.buffer & (nbrs_count == 2))

        self.graphics.draw(self.serial)
        time.sleep(1 / self.framerate)
        if time.time() > self.start+20:
            self.randomize()
            self.start = time.time()

GAME = Life
