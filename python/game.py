import curses
import time
import queue
import sys

BUZZER = 15
BEEPER = 13

try:
    import requests
    import RPi.GPIO as gpio
    gpio.setmode(gpio.BOARD)
    gpio.setup(BUZZER, gpio.OUT)
    gpio.setup(BEEPER, gpio.OUT)
except:
    pass

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

    def trigger(self, item, act):
        if kind == "alert" and requests:
            requests.get("localhost:5000/{}/a/7".format(act))
        elif kind == "buzzer" and gpio:
            gpio.output(BUZZER, 1 if act == "on" else 0)
        elif kind == "beeper" and gpio:
            gpio.output(BEEPER, 1 if act == "on" else 0)
