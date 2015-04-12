import graphics
import driver
import game
import string
import sys
import time

class Navi(game.Game):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hey = graphics.TextSprite("HEY", x=47, y=3, width=5, height=7)
        self.sprites.add(self.hey)
        self.show = True
        self.listen = graphics.TextSprite("LISTEN: ...", x=3, y=3, width=5, height=7)
        self.push = False

    def loop(self):
        if self.show:
            self.sprites.remove(self.hey)
            self.show = False
            time.sleep(1)

        elif not self.keys:
            self.sprites.add(self.hey)
            self.show = True
            time.sleep(3)
            
        if self.push:
            time.sleep(6)
            print(self.sprites)
            self.sprites.remove(self.listen)
            self.push = False

        if self.keys:
            self.sprites.add(self.listen)
            self.push = True
            
            

        super().loop()


GAME = Navi
        
