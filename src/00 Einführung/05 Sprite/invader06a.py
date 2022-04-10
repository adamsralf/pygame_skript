import os
from time import time

import pygame


class Settings:
    window = {'width': 600, 'height': 100}
    fps = 60
    deltatime = 1.0 / fps

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


class Defender(pygame.sprite.Sprite):               # Kindklasse von Sprite §\label{srcInvader0601}§

    def __init__(self) -> None:                     # Konstruktor §\label{srcInvader0602}§
        super().__init__()
        self.image: pygame.surface.Surface = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] // 2
        self.rect.bottom = Settings.window['height'] - 5
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.speed = pygame.math.Vector2(300, 0)

    def update(self) -> None:                       # Zustandsberechnung §\label{srcInvader0603}§
        newpos = self.position + (self.speed * Settings.deltatime)
        if newpos.x + self.rect.width >= Settings.window['width']:
            self.change_direction()
        elif newpos.x <= 0:
            self.change_direction()
        else:
            self.position = newpos
            self.rect.left = round(newpos.x)

    def draw(self, screen: pygame.surface.Surface) -> None:  # Malen §\label{srcInvader0604}§
        screen.blit(self.image, self.rect)

    def change_direction(self) -> None:             # OO style §\label{srcInvader0608}§
        self.speed.x *= -1


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.window_dim())
    pygame.display.set_caption("Sprite")
    clock = pygame.time.Clock()
    defender = Defender()                           # Objekt anlegen §\label{srcInvader0605}§

    time_previous = time()
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender.update()                           # Aufruf §\label{srcInvader0606}§

        # Draw
        screen.fill("white")
        defender.draw(screen)                       # Aufruf §\label{srcInvader0607}§
        pygame.display.flip()

        clock.tick(Settings.fps)
        time_current = time()
        Settings.deltatime = time_current - time_previous
        time_previous = time_current
    pygame.quit()


if __name__ == '__main__':
    main()
