import itertools
import threading
import datetime
import graphics
import requests
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
        self.expiration = expiration or 2147483647
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
                                           delay=.01, reverse=True)

            if effect:
                self.effects.append(effect)

TEMPERATURE = 0

def update_temp():
    while True:
        try:
            global TEMPERATURE
            TEMPERATURE = requests.get("http://idiotic.hackafe.net/api/item/Living_Room_Temperature/state").json()["result"]
            time.sleep(60)
        except:
            time.sleep(5)

def get_default_message():
    return Message("{:%H:%M:%S}   {:.1f}C".format(datetime.datetime.now(), TEMPERATURE), priority=.1)

class MessageBoard(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.messages = {}

        self.frame_lock = threading.Lock()

        self.api = flask.Flask(__name__)

        self.api.add_url_rule('/add_message', 'add_message', self.add_message, methods=['POST'])
        self.api.add_url_rule('/remove_message/<id>', 'remove_message', self.remove_message, methods=['GET', 'POST'])
        self.api.add_url_rule('/clear', 'clear', self.clear, methods=['POST'])

        self.server = simple_server.make_server('', 8800, self.api)

        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

        self.update_temp_thread = threading.Thread(target=update_temp, daemon=True)
        self.update_temp_thread.start()

        self.ids = 0

        self.cur_msg = None
        self.switch_time = 0
        self.queue = self.messages_gen()

    def stop(self):
        super().stop()
        self.server.shutdown()
        self.server.server_close()

    def add_message(self):
        text = request.form.get("text", "?")
        priority = int(request.form.get("priority", 5))
        expiration = int(request.form.get("expiration", 0))
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

    def clear(self):
        with self.frame_lock:
            self.messages = {}
        return ''

    def loop(self):
        super().loop()

        if time.time() >= self.switch_time:
            if self.cur_msg:
                self.sprites.remove(self.cur_msg.label)
                self.sprites.difference_update(set(self.cur_msg.effects))

            self.cur_msg = next(self.queue)

            if self.cur_msg:
                self.sprites.add(self.cur_msg.label)
                self.sprites.update(set(self.cur_msg.effects))

                self.switch_time = time.time() + self.cur_msg.priority
            else:
                self.switch_time = time.time() + .5

    def messages_gen(self):
        while True:
            msgs = []
            with self.frame_lock:
                msgs = list(self.messages.values())

            if msgs:
                yield from list(self.messages.values())
            else:
                yield get_default_message()

            with self.frame_lock:
                self.messages = {k: m for k, m in self.messages.items() if m.expiration > time.time()}

GAME = MessageBoard
