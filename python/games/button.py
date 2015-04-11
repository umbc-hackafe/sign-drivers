import functools
import threading
import websocket
import graphics
import requests
import driver
import game
import json
import sys
import re

def on_message(game, ws, message):
    a = json.loads(message)
    game.reset_time(a["payload"]["seconds_left"])

class Button(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.timer = graphics.Rectangle(112-12, 15, x=12, y=0)
        self.text_top = graphics.TextSprite("60", x=0, y=0, width=5, height=7)
        self.text_bottom = graphics.TextSprite("00", x=0, y=8, width=5, height=7)
        self.time = 60.00
        self.total_width = 112-12

        self.sprites.add(self.timer)
        self.sprites.add(self.text_top)
        self.sprites.add(self.text_bottom)


        regex = re.compile(r"(wss://wss\.redditmedia\.com/thebutton\?h=[^\"]*)")
        url = requests.get("https://www.reddit.com/r/thebutton")
        print(url.text)
        try:
            url = re.search(regex, requests.get("https://www.reddit.com/r/thebutton").text).group(1)
        except:
            url = "wss://wss.redditmedia.com/thebutton?h=7f66bf82878e6151f7688ead7085eb63a0baff0b&e=1428621271"
        self.ws = websocket.WebSocketApp(url)
        self.ws.on_message = functools.partial(on_message, self)
        self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.ws_thread.start()

    def reset_time(self, time=60.00):
        self.time = time

    def loop(self):
        self.time -= 1 / self.framerate
        self.text_top.set_text(str(int(self.time)))
        self.text_bottom.set_text(str(int(self.time % 1 * 100)))
        self.timer.width = int(self.total_width * self.time / 60)
        super().loop()

GAME = Button
