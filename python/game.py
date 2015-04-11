import curses
import time
import queue
import sys

class Game:
    
    def __init__(self, graphics, serial, stdscr, play, framerate=30):
        self.play = play
        self.stdscr = stdscr
        self.graphics = graphics
        self.serial = serial
        self.sprites = set()
        self.framerate = framerate
        self.input_queue = queue.Queue()
        self.keys = set()

    def send_input(self, name):
        self.input_queue.put(name)

    def handle_events(self):
        self.keys = set()

        try:
            while True:
                key = self.stdscr.getkey().lower()
                if key == '\x1b':
                    self.play.exec_game('menu')
                    return
                self.keys.add(key)
        except curses.error:
            pass

        try:
            while True:
                item = self.input_queue.get_nowait().lower()
                self.keys.add(item)
        except queue.Empty:
            pass
        
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
            self.handle_events()
            self.loop()
