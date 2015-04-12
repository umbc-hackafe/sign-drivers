import graphics
import numpy
import math
import driver
import sys
import game

class Breakout(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, framerate=120, **kwargs)

        self.reset()

    def reset(self):
        self.sprites.clear()
        
        self.paddle = graphics.Rectangle(2, 5, x=0, y=4)
        self.sprites.add(self.paddle)

        self.blocks = set()
        
        for row in range(0, 16, 2):
            for i in range(0 if row % 4 else 1, 5, 2):
                block = graphics.Rectangle(2, 3, x=112 - row, y=3*i)
                self.blocks.add(block)
                self.sprites.add(block)

        self.ball = graphics.Circle(1, x=8, y=7.5)
        self.sprites.add(self.ball)

        self.ballspeed = [2, 0.5]

        self.playing = True

    def loop(self):
        if self.playing and self.blocks:
            if 'w' in self.keys:
                self.paddle.y = max(self.paddle.y - 1, 0)
            if 's' in self.keys:
                self.paddle.y = min(self.paddle.y + 1, 15 - self.paddle.height)

            l = math.sqrt(self.ballspeed[0]**2 + self.ballspeed[1]**2)

            for block in list(self.blocks):
                if ((block.y <= self.ball.y < block.y + block.height)
                    and (block.x <= self.ball.x < block.x + block.width)):
                    self.ballspeed[0] *= -1
                    self.blocks.remove(block)
                    self.sprites.remove(block)
                    break
                
            if ((self.paddle.y <= self.ball.y < self.paddle.y + self.paddle.height)
                and (self.paddle.x <= self.ball.x < self.paddle.x + self.paddle.width)):
                self.ballspeed[0] *= -1

            self.ball.x += self.ballspeed[0]
            self.ball.y += self.ballspeed[1]

            if self.ball.y < 0 and self.ballspeed[1] <= 0:
                self.ballspeed[1] *= -1
            elif self.ball.y > 14 and self.ballspeed[1] >= 0:
                self.ballspeed[1] *= -1

            if self.ball.x > 111 and self.ballspeed[0] >= 0:
                self.ballspeed[0] *= -1
            elif self.ball.x < 0 and self.ballspeed[0] <= 0:
                self.playing = False
                self.sprites.clear()
                text = graphics.TextSprite('You Lose', width=5, height=7, x=1)
                self.sprites.add(text)
                text = graphics.TextSprite('R to restart', width=5, height=7, x=1, y=8)
                self.sprites.add(text)
        elif not self.blocks:
            self.sprites.clear()
            text = graphics.TextSprite('You WIN!!', width=5, height=7, x=1)
            self.sprites.add(text)
            text = graphics.TextSprite('R to restart', width=5, height=7, x=1, y=8)
            self.sprites.add(text)
        else:
            if 'r' in self.keys:
                self.reset()

        super().loop()

GAME = Breakout
