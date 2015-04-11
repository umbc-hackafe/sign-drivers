import graphics
import driver
import game
import pygame

class PixelMan(game.Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pixel = graphics.Rectangle(1, 1, x=56, y=8, wrapx=True, wrapy=True)
        self.sprites.add(self.pixel)

    def loop(self):
        self.handle_events()

        if self.keys[pygame.K_a]:
            self.pixel.x -= 1
        elif self.keys[pygame.K_d]:
            self.pixel.x += 1
        if self.keys[pygame.K_s]:
            self.pixel.y += 1
        elif self.keys[pygame.K_w]:
            self.pixel.y -= 1
            
        super().loop()

GAME = PixelMan
