import time
import pygame
import queue
import sys

class Game:
    def __init__(self, graphics, serial, framerate=30):
        pygame.init()
        pygame.display.set_mode((50,50))
        self.graphics = graphics
        self.serial = serial
        self.sprites = set()
        self.framerate = framerate
        self.input_queue = queue.Queue()
        self.old_keys = [False] * 500
        self.keys = [False] * 500

    def send_input(self, name):
        self.input_queue.put(name)

    def handle_events(self):
        self.old_keys = self.keys[:]
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
            if event.type == pygame.KEYUP:
                self.keys[event.key] = False
        
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
