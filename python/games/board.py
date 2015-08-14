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
    def __init__(self, text, priority=5, expiration=None, effects=[]):
        self.text = text

        self.label = graphics.TextSprite(text, width=5, height=7, y=4)
        self.label.x = (112 - self.label.size()) // 2

        self.priority = priority
        self.expiration = expiration or datetime.datetime.max.timestamp()
        self.effects = []

        for effect_type in effects:
            effect = None
            if effect_type == "scroll":
                self.label.x = 112
                effect = graphics.Animator(self.label, attr="x", max=112,
                                           min=-self.label.size(),
                                           loop=True, delay=.04, step=-1)
            elif effect_type == "scroll_y":
                effect = graphics.Animator(self.label, attr="y", max=15,
                                           min=-self.label.height,
                                           loop=True, delay=.4)
            elif effect_type == "bounce_x":
                self.label.x = 112
                effect = graphics.Animator(
                    self.label, attr="x",
                    min=(112 - self.label.size() if self.label.size() > 112 else 0),
                    max=(0 if self.label.size() > 112 else 112 - self.label.size()),
                    delay=.04,
                    reverse=True)
            elif effect_type == "bounce_y":
                effect = graphics.Animator(self.label, attr="y",
                                           max=15-self.label.height, min=0,
                                           reverse=True, delay=.4)
            elif effect_type == "blink":
                effect = graphics.Animator(self.label, attr="visible", max=1, min=0,
                                           reverse=True, delay=1.5)
            elif effect_type == "blink_fast":
                effect = graphics.Animator(self.label, attr="visible", max=1, min=0,
                                           reverse=True, delay=.25)
            elif effect_type == "shake":
                effect = graphics.Animator(self.label, attr="y", max=6, min=2,
                                           delay=.02, reverse=True)

            if effect:
                self.effects.append(effect)

class MessageBoard(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.messages = {}

        modes = [
            self.display_messages
        ]

        self.frame_lock = threading.Lock()

        self.api = flask.Flask(__name__)
        self.api.debug = True

        self.api.add_url_rule('/add_message', 'add_message', self.add_message, methods=['POST'])
        self.api.add_url_rule('/remove_message/<id>', 'remove_message', self.remove_message, methods=['GET', 'POST'])

        self.server = simple_server.make_server('', 8800, self.api)

        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

        self.ids = 0

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
        effects = filter(bool, request.form.get("effects", "").split(","))
        name = request.form.get("name", None)

        if name is None:
            name = str(self.ids)
            self.ids += 1

        with self.frame_lock:
            self.messages[name] = Message(text, priority, expiration, effects)

        return name

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
            messages = list(self.messages.values())

        for message in messages:
            self.sprites.add(message.label)
            for effect in message.effects:
                self.sprites.add(effect)

            run_until = time.time() + message.priority

            while time.time() < run_until:
                yield

            for effect in message.effects:
                self.sprites.remove(effect)
            self.sprites.remove(message.label)

        with self.frame_lock:
            self.messages = {k: m for k, m in self.messages.items() if m.expiration > time.time()}

GAME = MessageBoard
