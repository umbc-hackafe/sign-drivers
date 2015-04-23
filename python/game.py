import curses
import time
import queue
import sys
import requests
try:
    import RPi.GPIO as gpio
except:
    print("Couldn't load GPIO")
    global gpio
    gpio = lambda: None
    setattr(gpio, 'setup', lambda _, __: None)
    setattr(gpio, 'setwarnings', lambda _: None)
    setattr(gpio, 'setmode', lambda _: None)
    setattr(gpio, 'output', lambda _, __: None)
    setattr(gpio, 'BOARD', None)
    setattr(gpio, 'OUT', None)

BUZZER = 15
BEEPER = 13

gpio.setwarnings(False);
gpio.setmode(gpio.BOARD)
gpio.setup(BUZZER, gpio.OUT)
gpio.setup(BEEPER, gpio.OUT)

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
        for sprite in set(self.sprites):
            sprite.draw(self.graphics)

        self.graphics.draw(self.serial)
        time.sleep(1 / self.framerate)

    def stop(self):
        self.running = False
        self.trigger("alert", "off")
        self.trigger("buzzer", "off")
        self.trigger("beeper", "off")

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.loop()

    def trigger(self, item, act):
        if item == "alert" and requests:
            try:
                requests.get("http://localhost:5000/{}/a/7".format(act))
            except:
                pass
        elif item == "buzzer" and gpio:
            gpio.output(BUZZER, 1 if act == "on" else 0)
        elif item == "beeper" and gpio:
            gpio.output(BEEPER, 1 if act == "on" else 0)
