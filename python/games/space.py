from scipy.signal import convolve2d
import graphics
import random
import driver
import game
import time

rows = 15
cols = 112

class Space(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invaders = []
        for i in range(5):
             for j in range(10):
                  invader = graphics.Rectangle(x=10*j, y=2*i+2, width=3, height=1)
                  self.invaders.append(invader)
                  self.sprites.add(invader)
        self.direction = 1
        self.ship = graphics.Rectangle(x=112, y=7, width=2, height=1)
        self.sprites.add(self.ship)
        self.bullets = []
        self.end = False
        self.victoryText = graphics.TextSprite("You Win!", width=5, height=7, x=10, y=4)

    def loop(self):
        if self.end == True:
            time.sleep(3)
            self.sprites = set()
            for i in range(5):
                for j in range(10):
                    invader = graphics.Rectangle(x=10*j, y=2*i+2, width=3, height=1)
                    self.invaders.append(invader)
                    self.sprites.add(invader)
            self.end = False
        self.handle_events()
        fire = False
        if 'a' in self.keys:
            self.ship.y += 1
        if 'd' in self.keys:
            self.ship.y -= 1
        if ' ' in self.keys:
            fire = True
        lowerY = -1
        upperY = 17
        for i in self.invaders:
           if i.y > lowerY:
               lowerY = i.y
           if i.y < upperY:
               upperY = i.y
        if lowerY == 15:
            self.direction *= -1
            for i in self.invaders:
                i.x += 1
                if i.x > 108:
                    print("You LOSE!")
        if upperY == 0:
            self.direction *= -1
        for i in self.invaders:
            i.y += self.direction
        if fire and len(self.bullets) < 3:
            newBullet = graphics.Rectangle(x=self.ship.x, y=self.ship.y, width=1, height=1)
            self.bullets.append(newBullet)
        for i in self.bullets:
            i.x -= 1
            self.sprites.add(i)
            if i.x < 0:
                self.sprites.remove(i)
            for j in self.invaders:
                if j.x == i.x and j.y == i.y:
                    self.invaders.remove(j)
                    self.sprites.remove(j)
                    self.sprites.remove(i)
                    self.bullets.remove(i)
        if not(self.invaders):
            self.sprites = set()
            self.bullets = list()
            self.sprites.add(self.victoryText)
            self.end = True
        super().loop()

GAME = Space
