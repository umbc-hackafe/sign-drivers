import graphics
import driver
import game
import random

class Snake(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reset()

    def reset(self):
        self.sprites.clear()

        self.playing = True
        
        self.snake = [graphics.Rectangle(1, 1, x=7, y=7)]
        self.direction = (1,0)
        
        self.sprites.add(self.snake[0])

        self.food = graphics.Rectangle(1, 1, x=17, y=7)
        self.sprites.add(self.food)

        self.count = 0

    def loop(self):
        if self.playing:
            if 'a' in self.keys and not self.direction[0]:
                self.direction = (-1, 0)
            elif 'd' in self.keys and not self.direction[0]:
                self.direction = (1, 0)
            if 's' in self.keys and not self.direction[1]:
                self.direction = (0, 1)
            elif 'w' in self.keys and not self.direction[1]:
                self.direction = (0, -1)

            self.count = (self.count + 1) % 2

            if not self.count:
                for i in range(len(self.snake) - 1, 0, -1):
                    self.snake[i].x = self.snake[i-1].x
                    self.snake[i].y = self.snake[i-1].y
                self.snake[0].x += self.direction[0]
                self.snake[0].y += self.direction[1]

                poses = set((s.x, s.y) for s in self.snake[1:])
                if (self.snake[0].x < 0 or self.snake[0].x >= 112
                    or self.snake[0].y < 0 or self.snake[0].y >= 15
                    or (self.snake[0].x, self.snake[0].y) in poses):
                    self.sprites.clear()
                    self.sprites.add(graphics.TextSprite(
                        'GAME OVER. LEN:{}'.format(len(self.snake)),
                        width=5, height=7))
                    self.sprites.add(graphics.TextSprite(
                        'R TO RELOAD'.format(len(self.snake)),
                        width=5, height=7, y=8))
                    self.playing = False
                    
                if (self.snake[0].x, self.snake[0].y) == (self.food.x, self.food.y):
                    self.snake.append(self.food)
                    poses.add((self.snake[0].x, self.snake[0].y))
                    nx, ny = random.randrange(0, 112), random.randrange(0, 15)
                    while (nx,ny) in poses:
                        nx, ny = random.randrange(0, 112), random.randrange(0, 15)
                    self.food = graphics.Rectangle(1, 1, x=nx, y=ny)
                    self.sprites.add(self.food)

        else:
            if 'r' in self.keys:
                self.reset()
                
        super().loop()

GAME = Snake
