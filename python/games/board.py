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
        priority = int(request.form.get("priority", 5))
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

            next_animate = time.time() + .05
            while label.x + len(label.text) * (label.width + 1) > 112:
                while time.time() < next_animate:
                    yield
                label.x -= 1
                next_animate = time.time() + .05

            run_until = time.time() + message.priority

            while time.time() < run_until:
                yield

            self.sprites.remove(label)

GAME = MessageBoard
