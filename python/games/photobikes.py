import graphics
import driver
import game
import random

class Nort(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reset()

    def reset(self):
        self.sprites.clear()

        self.playing = True
        
        self.snake_a = [graphics.Rectangle(1, 1, x=7, y=7)]
        self.direction_a = (1,0)

        self.snake_b = [graphics.Rectangle(1, 1, x=112-7, y=7)]
        self.direction_b = (-1,0)
        
        self.sprites.add(self.snake_a[0])
        self.sprites.add(self.snake_b[0])

        self.count = 0
        self.buzzer = 0
        self.beeping = False

    def loop(self):
        if self.buzzer > 0:
            self.buzzer -= 1
        elif self.buzzer == 0:
            self.trigger("buzzer", "off")

        if self.beeping:
            self.trigger("beeper", "off")
            self.beeping = False

        if self.playing:
            if 'a' in self.keys and not self.direction_a[0]:
                self.direction_a = (-1, 0)
                self.beeping = True
                self.trigger("beeper", "on")
            elif 'd' in self.keys and not self.direction_a[0]:
                self.direction_a = (1, 0)
                self.beeping = True
                self.trigger("beeper", "on")
            if 's' in self.keys and not self.direction_a[1]:
                self.direction_a = (0, 1)
                self.beeping = True
                self.trigger("beeper", "on")
            elif 'w' in self.keys and not self.direction_a[1]:
                self.direction_a = (0, -1)
                self.beeping = True
                self.trigger("beeper", "on")

            if 'k' in self.keys and not self.direction_b[0]:
                self.direction_b = (-1, 0)
                self.beeping = True
                self.trigger("beeper", "on")
            elif ';' in self.keys and not self.direction_b[0]:
                self.direction_b = (1, 0)
                self.beeping = True
                self.trigger("beeper", "on")
            if 'l' in self.keys and not self.direction_b[1]:
                self.direction_b = (0, 1)
                self.beeping = True
                self.trigger("beeper", "on")
            elif 'o' in self.keys and not self.direction_b[1]:
                self.direction_b = (0, -1)
                self.beeping = True
                self.trigger("beeper", "on")

            self.count = 0

            if not self.count:
                poses = set((s.x, s.y) for s in self.snake_a[1:] + self.snake_b[1:])
                for snake, direction in [(self.snake_a, self.direction_a), (self.snake_b, self.direction_b)]:
                    for i in range(len(snake) - 1, 0, -1):
                        snake[i].x = snake[i-1].x
                        snake[i].y = snake[i-1].y
                    snake[0].x += direction[0]
                    snake[0].y += direction[1]

                    if (snake[0].x < 0 or snake[0].x >= 112
                        or snake[0].y < 0 or snake[0].y >= 15
                        or (snake[0].x, snake[0].y) in poses) \
                        or (self.snake_a[0].x, self.snake_a[0].y) == (self.snake_b[0].x, self.snake_b[0].y):
                        self.trigger("buzzer", "on")
                        self.buzzer = 5
                        self.sprites.clear()

                        if (self.snake_a[0].x, self.snake_a[0].y) == (self.snake_b[0].x, self.snake_b[0].y):
                            self.sprites.add(graphics.TextSprite("DRAW", width=5, height=7))
                        elif snake == self.snake_b:
                            self.sprites.add(graphics.TextSprite("LEFT WINS", width=5, height=7))
                        elif snake == self.snake_a:
                            self.sprites.add(graphics.TextSprite("RIGHT WINS", width=5, height=7))

                        self.sprites.add(graphics.TextSprite(
                            'R TO RELOAD'.format(len(snake)),
                            width=5, height=7, y=8))
                        self.playing = False
                    
                        poses.add((snake[0].x, snake[0].y))

                    new_seg = graphics.Rectangle(1, 1, x=snake[0].x, y=snake[0].y)
                    snake.append(new_seg)
                    poses.add((snake[0].x, snake[0].y))
                    self.sprites.add(new_seg)
        else:
            if 'r' in self.keys:
                self.reset()
                
        super().loop()

GAME = Nort
