from scipy.signal import convolve2d
import graphics
import random
import driver
import game
import time

rows = 15
cols = 112

class Pong(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lpaddle = graphics.Rectangle(x=0, y=5, width=1, height=5)
        self.rpaddle = graphics.Rectangle(x=111, y=5, width=1, height=5)
        self.ball = graphics.Circle(x=56, y=7, radius=1)
        self.sprites.add(self.lpaddle)
        self.sprites.add(self.rpaddle)
        self.sprites.add(self.ball)
        self.ball.yv = -1
        self.ball.xv = -1
        self.rscore = 0
        self.lscore = 0

    def loop(self):
        if 'w' in self.keys:
            self.lpaddle.y += 1
            if self.lpaddle.y > 11:
                 self.lpaddle.y = 11
        if 's' in self.keys:
            self.lpaddle.y -= 1
            if self.lpaddle.y < 0:
                 self.lpaddle.y = 0
        if 'o' in self.keys:
            self.rpaddle.y += 1
            if self.rpaddle.y > 11:
                 self.rpaddle.y = 11
        if 'l' in self.keys:
            self.rpaddle.y -= 1
            if self.rpaddle.y < 0:
                 self.rpaddle.y = 0
        if (self.ball.y < (self.ball.radius)) or (self.ball.y > (15-self.ball.radius)):
            self.ball.yv = -1*self.ball.yv
            self.ball.y += self.ball.yv
        if self.ball.x < 1:
          if ((self.ball.y < self.lpaddle.y) or (self.ball.y > (self.lpaddle.y + 4))):
            print(self.ball.y, self.lpaddle.y)
            self.ball.y = 7
            self.ball.x = 56
            self.ball.yv = -1
            self.ball.xv = 1
            self.rscore += 1
          else:
            self.ball.xv = -1*self.ball.xv
            self.ball.x += self.ball.xv
        if self.ball.x > 110:
          if ((self.ball.y < self.rpaddle.y) or (self.ball.y > (self.rpaddle.y + 4))):
            print(self.ball.y, self.rpaddle.y)
            self.ball.y = 7
            self.ball.x = 56
            self.ball.yv = -1
            self.ball.xv = -1
            self.lscore += 1
          else:
            self.ball.xv = -1*self.ball.xv
            self.ball.x += self.ball.xv
        
        self.ball.x += self.ball.xv
        self.ball.y += self.ball.yv
        super().loop()

GAME = Pong
