import graphics
import driver
import game
import pygame

class Shell(game.Game):
    norm_input_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
            pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
            pygame.K_9,
            pygame.K_a,
            pygame.K_b,
            pygame.K_c,
            pygame.K_d,
            pygame.K_e,
            pygame.K_f,
            pygame.K_g,
            pygame.K_h,
            pygame.K_i,
            pygame.K_j,
            pygame.K_k,
            pygame.K_l,
            pygame.K_m,
            pygame.K_n,
            pygame.K_o,
            pygame.K_p,
            pygame.K_q,
            pygame.K_r,
            pygame.K_s,
            pygame.K_t,
            pygame.K_u,
            pygame.K_v,
            pygame.K_w,
            pygame.K_x,
            pygame.K_y,
            pygame.K_z
            # pygame.K_SPACE,
            # pygame.K_EXCLAIM,
            # pygame.K_QUOTEDBL,
            # pygame.K_HASH,
            # pygame.K_QUOTE,
            # pygame.K_LEFTPAREN,
            # pygame.K_HASH,
            # pygame.K_HASH,
            # pygame.K_HASH,
            # pygame.K_HASH,
            # pygame.K_HASH,
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prompt  = graphics.TextSprite(">", x=0, y=0)
        self.user_in_buf = ""
        self.user_in = graphics.TextSprite(self.user_in_buf, x=5, y=0)
        self.sprites.add(self.prompt)
        self.sprites.add(self.user_in)


    def loop(self):
        self.handle_events()

        for key in type(self).norm_input_keys:
            if self.keys[key] and not self.old_keys[key]:
                print("Got key: %d" % key)
                self.user_in_buf += chr(key)
        if self.keys[pygame.K_BACKSPACE] and not self.old_keys[pygame.K_BACKSPACE] :
            self.user_in_buf = self.user_in_buf[:-1]

        self.user_in.set_text(self.user_in_buf)
        super().loop()

GAME = Shell
