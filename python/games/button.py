import functools
import threading
import websocket
import graphics
import requests
import driver
import game
import json
from time import time as now
import sys
import re

def on_message(game, ws, message):
    a = json.loads(message)
    game.reset_time(a["payload"]["seconds_left"])
    game.reset_participants(a["payload"]["participants_text"])

def color(secs):
    if secs <= 11:
        return 6
    elif secs <= 21:
        return 5
    elif secs <= 31:
        return 4
    elif secs <= 41:
        return 3
    elif secs <= 51:
        return 2
    elif secs <= 60:
        return 1
    else:
        return 1

class Button(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.timer = graphics.Rectangle(112-12, 7, x=12, y=0)
        self.text_top = graphics.TextSprite("60", x=0, y=0, width=5, height=7)
        self.text_bottom = graphics.TextSprite("00", x=0, y=8, width=5, height=7)
        self.text_participants = graphics.TextSprite("???,???", x=112-6*7, y=8, width=5, height=7)
        self.at = now()
        self.time = 60.00
        self.total_width = 112-12

        self.last_time = 61
        self.real_time = 61
        self.bars = []

        self.sprites.add(self.timer)
        self.sprites.add(self.text_top)
        self.sprites.add(self.text_bottom)
        self.sprites.add(self.text_participants)


        regex = re.compile(r"(wss://wss\.redditmedia\.com/thebutton\?h=[^\"]*)")
        url = requests.get("https://www.reddit.com/r/thebutton")
        try:
            url = re.search(regex, requests.get("https://www.reddit.com/r/thebutton").text).group(1)
        except:
            url = "wss://wss.redditmedia.com/thebutton?h=7f66bf82878e6151f7688ead70;85eb63a0baff0b&e=1428621271"
        self.ws = websocket.WebSocketApp(url)
        self.ws.on_message = functools.partial(on_message, self)
        self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.ws_thread.start()

    def reset_time(self, time=60.00):
        self.last_time = self.real_time
        self.real_time = time
        self.time = time
        self.at = now()

        if self.real_time >= self.last_time:
            bar = graphics.Rectangle(1, color(self.last_time), x=112-6*len(self.text_participants.text)-2, y=15-color(self.last_time))
            for s in list(self.bars):
                s.x -= 1
                if s.x < 13:
                    self.bars.remove(s)
                    self.sprites.remove(s)
            self.bars.append(bar)
            self.sprites.add(bar)

    def reset_participants(self, participants="???,???"):
        self.text_participants.set_text(participants)
        self.text_participants.x = 112 - 6 * len(participants)

    def loop(self):
        self.time = max(self.time - (now() - self.at), 0)
        self.at = now()
        self.text_top.set_text("{:02}".format(int(self.time)))
        self.text_bottom.set_text("{:02}".format(int(self.time % 1 * 100)))
        self.timer.width = int(self.total_width * self.time / 60)
        super().loop()

GAME = Button
