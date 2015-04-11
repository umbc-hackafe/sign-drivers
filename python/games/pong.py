from scipy.signal import convolve2d
import graphics
import random
import driver
import game
import time
import sys

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
        self.ball.yv = -1
        self.ball.xv = -1
        self.rscore = 0
        self.lscore = 0
        self.leftScore = graphics.TextSprite("0", x=20, y=0, width=5, height=7)
        self.rightScore = graphics.TextSprite("0", x=87, y=0, width=5, height=7)
        self.sprites.add(self.leftScore)
        self.sprites.add(self.rightScore)
        self.leftVictory = graphics.TextSprite("LEFT WINS!", x=13, y=4, width=5, height=7)
        self.rightVictory = graphics.TextSprite("RIGHT WINS!", x=13, y=4, width=5, height=7)
        self.sprites.add(self.ball)
        self.end = False

    def loop(self):
        if self.end:
            time.sleep(3)
            self.sprites = set()
            self.sprites.add(self.lpaddle)
            self.sprites.add(self.rpaddle)
            self.sprites.add(self.leftScore)
            self.sprites.add(self.rightScore)
            self.sprites.add(self.ball)
            self.rscore = 0
            self.lscore = 0
            self.leftScore.set_text("0")
            self.rightScore.set_text("0")
            self.end = False
            self.ball.x = 56
            self.ball.y = 7
            self.ball.xv = -1
            self.ball.yv = -1
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
            self.ball.y = 7
            self.ball.x = 56
            self.ball.yv = -1
            self.ball.xv = 1
            self.rscore += 1
            self.rightScore.set_text(str(self.rscore))
            if self.rscore == 10:
                self.sprites = set()
                self.sprites.add(self.rightVictory)
                self.end = True
          else:
            self.ball.xv = -1*self.ball.xv
            self.ball.x += self.ball.xv
        if self.ball.x > 110:
          if ((self.ball.y < self.rpaddle.y) or (self.ball.y > (self.rpaddle.y + 4))):
            self.ball.y = 7
            self.ball.x = 56
            self.ball.yv = -1
            self.ball.xv = -1
            self.lscore += 1
            self.leftScore.set_text(str(self.lscore))
            if self.lscore == 10:
                self.sprites = set()
                self.sprites.add(self.leftVictory)
                self.end = True
          else:
            self.ball.xv = -1*self.ball.xv
            self.ball.x += self.ball.xv
        
        self.ball.x += self.ball.xv
        self.ball.y += self.ball.yv
        super().loop()

GAME = Pong
