import graphics
import time
import datetime
import game

class Countdown(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.timer = graphics.Rectangle(112, 7, x=0, y=8)
        self.text = graphics.TextSprite("1:00:00.000 REMAIN", x=0, y=0, width=5, height=7)
        self.end_time = datetime.datetime(2015, 4, 12, 10, 0, 0)
        #self.end_time = datetime.datetime(2015, 4, 12, 9, 53, 0)

        self.sprites.add(self.timer)
        self.sprites.add(self.text)

        self.framerate = 100
        self.light = False
        self.blink = False

    def loop(self):
        tdiff = self.end_time - datetime.datetime.now()

        if not self.light and tdiff.seconds <= 900:
            self.light = True
            self.trigger("alert", "on")

        if tdiff.seconds <= 0:
            if tdiff.seconds % 2 and not self.blink:
                self.sprites.remove(self.text)
                self.sprites.add(self.timer)
                self.blink = True
            elif self.blink:
                self.sprites.add(self.text)
                self.sprites.remove(self.timer)
                self.blink = False
        else:
            h, rem = divmod(tdiff.seconds, 3600)
            m, s = divmod(rem, 60)
            mls = tdiff.microseconds // 1000
            
            self.text.set_text("{:0>1}:{:0>2}:{:0>2}.{:0>3} REMAIN".format(
                h, m, s, mls))
        self.timer.width = max(0,int(112 * tdiff.secods / 3600))

        super().loop()

GAME = Countdown
