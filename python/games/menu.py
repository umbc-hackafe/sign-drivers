import graphics
import driver
import game

class Menu(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.i = 0
        
        self.games = [
            'life',
            'twitter',
            'fft',
            'button',
            'stocks',
            'flappypixel',
            'pong',
            'snake',
            'space',
        ]

        self.game_names = dict(zip(self.games, [
            'CONWAY LIFE',
            'TWITTER',
            'FAST FOURIER',
            'R/BUTTON',
            'STOCK TICKER',
            'FLAPPYPIXEL',
            'PONG',
            'SNAKE',
            'SPACE INVADERS',
        ]))

        self.label = graphics.TextSprite('{} {}'.format(self.i + 1, self.game_names[self.games[self.i]]), width=5, height=7, x=5, y=4)
        self.sprites.add(self.label)

    def loop(self):
        if 'a' in self.keys:
            self.i = (self.i - 1) % len(self.games)
            self.label.set_text('{} {}'.format(self.i + 1, self.game_names[self.games[self.i]]))
        elif 'd' in self.keys:
            self.i = (self.i + 1) % len(self.games)
            self.label.set_text('{} {}'.format(self.i + 1, self.game_names[self.games[self.i]]))

        if '\n' in self.keys:
            self.play.exec_game(self.games[self.i])
            
        super().loop()

GAME = Menu
