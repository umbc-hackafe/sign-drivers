import itertools
import threading
import datetime
import graphics
import random
import driver
import flask
from flask import request
import game
import time
import sys
from wsgiref import simple_server

class Message:
    def __init__(self, text, priority=5, expiration=None):
        self.text = text
        self.priority = priority
        self.expiration = expiration or datetime.datetime.max

class MessageBoard(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.messages = []

        modes = [
            self.display_messages
        ]

        self.frame_lock = threading.Lock()

        self.api = flask.Flask(__name__)
        self.api.debug = True

        self.api.add_url_rule('/add_message', 'add_message', self.add_message, methods=['POST'])
        self.api.add_url_rule('/remove_message/<int:id>', 'remove_message', self.remove_message, methods=['POST'])

        self.server = simple_server.make_server('', 8800, self.api)

        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

        self.things = 0

        self.cycle = itertools.chain.from_iterable(
            mode() for mode in itertools.chain.from_iterable(
                random.shuffle(x) or x for x in itertools.repeat(modes)))

    def stop(self):
        super().stop()
        self.server.shutdown()
        self.server.server_close()

    def add_message(self):
        text = request.form.get("text", "?")
        priority = request.form.get("priority", 5)
        expiration = request.form.get("expiration", None)

        with self.frame_lock:
            self.messages.append(Message(text, priority, expiration))
            return str(len(self.messages)-1)

    def remove_message(self, id):
        with self.frame_lock:
            del self.messages[id]
        return ''

    def loop(self):
        super().loop()

        next(self.cycle)

    def display_messages(self):
        messages = None
        with self.frame_lock:
            messages = list(self.messages)

        for message in messages:
            label = graphics.TextSprite(message.text, width=5, height=7, x=5, y=4)

            self.sprites.add(label)

            next_animate = time.time() + .25
            while label.x + len(label.text) * (label.width + 1) > 112:
                while time.time() < next_animate:
                    yield
                label.x -= 5
                next_animate = time.time() + .25

            run_until = time.time() + message.priority

            while time.time() < run_until:
                yield

            self.sprites.remove(label)

    def normal_mode(self):
        label = graphics.TextSprite('LINUX USERS GROUP', width=5, height=7, x=5, y=4)
        label.x = 5
        label.y = 4
        self.sprites.add(label)

        run_until = time.time() + random.uniform(5, 10)

        while time.time() < run_until:
            yield

        self.sprites.remove(label)

    def blink_mode(self):
        label = graphics.TextSprite('LINUX USERS GROUP', width=5, height=7, x=5, y=4)
        label.x = 5
        label.y = 4
        self.sprites.add(label)

        run_until = time.time() + random.uniform(5, 10)
        blink_at = time.time() + 0.5

        while time.time() < run_until:
            if blink_at < time.time():
                blink_at = time.time() + 0.5
                if label in self.sprites:
                    self.sprites.remove(label)
                else:
                    self.sprites.add(label)
            yield

        if label in self.sprites:
            self.sprites.remove(label)

    def bounce_mode(self):
        label = graphics.TextSprite('LINUX USERS GROUP', width=5, height=7, x=5, y=4)
        label.x = 5
        label.y = 4
        self.sprites.add(label)

        run_until = time.time() + random.uniform(5, 10)

        vx = random.choice([-1, 1])
        vy = random.choice([-1, 1])

        while time.time() < run_until:
            label.x += vx
            label.y += vy

            if label.x == 0 and vx < 0:
                vx = -vx
            if label.y == 0 and vy < 0:
                vy = -vy
            if label.x + (label.width + 1) * len(label.sprites) == 113 and vx > 0:
                vx = -vx
            if label.y + label.height == 15 and vy > 0:
                vy = -vy
            yield
            yield

        self.sprites.remove(label)


GAME = MessageBoard
