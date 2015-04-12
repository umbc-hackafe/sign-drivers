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
        self.end = False
        self.victoryText = graphics.TextSprite("You Win!", width=5, height=7, x=24, y=4)
        self.loseText = graphics.TextSprite("You Lose!", width=5, height=7, x=24, y=4)
        self.start()

    def start(self):
        if self.end == True:
            time.sleep(3)
        self.paused = True
        self.end = False
        self.sprites = set()
        self.invaders = list()
        for i in range(5):
            for j in range(10):
                invader = graphics.Rectangle(x=5*j, y=2*i+2, width=3, height=1)
                self.invaders.append(invader)
                self.sprites.add(invader)
        self.direction = 1
        self.ship = graphics.Rectangle(x=110, y=7, width=2, height=1)
        self.sprites.add(self.ship)
        self.bullets = []
        self.enemyBullets = []

    def win(self):
        self.end = True
        self.sprites = set()
        self.sprites.add(self.victoryText)

    def lose(self):
        self.end = True
        self.sprites = set()
        self.sprites.add(self.loseText)

    def loop(self):
        fire = False
        if 's' in self.keys or 'a' in self.keys:
            self.paused = False
            self.ship.y += 1
            if self.ship.y > 15:
                self.ship.y = 15
        if 'w' in self.keys or 'd' in self.keys:
            self.paused = False
            self.ship.y -= 1
            if self.ship.y < 0:
                self.ship.y = 0
        if ' ' in self.keys:
            self.paused = False
            fire = True

        if not self.paused:
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
            if upperY == 0:
                self.direction *= -1
                for i in self.invaders:
                    i.x += 1
            for i in self.invaders:
                i.y += self.direction
            if fire:
                newBullet = graphics.Rectangle(x=self.ship.x, y=self.ship.y, width=1, height=1)
                self.bullets.append(newBullet)
            for i in self.invaders:
                if random.random() < 0.02:
                    newBullet = graphics.Rectangle(x=i.x, y=i.y, width=1, height=1)
                    newBullet.speed=random.randint(1,3)
                    self.enemyBullets.append(newBullet)
                    self.sprites.add(newBullet)
            for i in self.enemyBullets:
                i.x += i.speed
                if i.x >= self.ship.x and i.y == self.ship.y:
                    self.lose()
            toremove = list()
            invadersToRemove = list()
            invaderBulletsToRemove = list()
            for i in self.enemyBullets:
                if i.x >= 112:
                    invaderBulletsToRemove.append(i)
            for i in invaderBulletsToRemove:
                if i in self.enemyBullets:
                    self.enemyBullets.remove(i)
            for i in self.bullets:
                if i.x < 0:
                    toremove.append(i)
                i.x -= 1
                if not self.end:
                    self.sprites.add(i)
                if i.x < 0:
                    if i in self.sprites:
                        self.sprites.discard(i)
                for j in self.invaders:
                    if j.x <= i.x < (j.x+3) and j.y == i.y:
                        invadersToRemove.append(j)
                        self.sprites.discard(j)
                        self.sprites.discard(i)
                        toremove.append(i)
            for i in invadersToRemove:
                if i in self.invaders:
                    self.invaders.remove(i)
            for i in toremove:
                if i in self.bullets:
                    self.bullets.remove(i)
            if not(self.invaders):
                self.win()
            for i in self.invaders:
                if i.x > 108:
                    self.lose()
        super().loop()
        if self.end:
            self.start()

GAME = Space
