import curses
import graphics
import driver
import game
import string
import sys

class Shell(game.Game):
    valid = set(string.printable).union(['\b'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prompt  = graphics.TextSprite(">", x=0, y=0)
        self.user_in_buf = []
        self.user_in = graphics.TextSprite(''.join(self.user_in_buf), x=5, y=0)
        self.sprites.add(self.prompt)
        self.sprites.add(self.user_in)

    def handle_events(self):
#        try:
#            while True:
#                key = self.stdscr.getkey().lower()
#                if key in type(self).valid:
#                    if key in set(['\b']):
#                        self.user_in_buf.pop()
#                    else:
#                        self.user_in_buf.append(key)
#        except curses.error:
#            pass

#        keyid = self.stdscr.getch()
#        while keyid >= 0:
            
        
    def loop(self):
        self.handle_events()

        self.user_in.set_text(''.join(self.user_in_buf))
        
        super().loop()

GAME = Shell
