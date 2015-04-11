import graphics
import driver
import game

class Shell(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prompt  = graphics.TextSprite(">", x=0, y=0)
        self.user_in_buf = ""
        self.user_in = graphics.TextSprite(self.user_in_buf, x=5, y=0)
        self.sprites.add(self.prompt)
        self.sprites.add(self.user_in)

    def recv_input(self, evt):
        if evt == "^H" or evt == "^?":
            if len(self.user_in.text) > 0:
                self.user_in_buf = self.user_in_buf[:-1]
        else:
            self.user_in_buf += evt

        self.user_in.set_text(self.user_in_buf)

    def loop(self):
        while not self.input_queue.empty():
            evt = self.input_queue.get()
            self.recv_input(evt)

        super().loop()

GAME = Shell
