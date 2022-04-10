import os
from time import time
from typing import Any

import pygame


class Settings:
    window = {'width': 600, 'height': 100}
    fps = 60
    deltatime = 1.0 / fps

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] // 2
        self.rect.bottom = Settings.window['height'] - 5
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.speed = pygame.math.Vector2(300, 0)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "newpos":        # Neue Position berechnen §\label{srcInvader06e01}§
                self.position = self.position + (self.speed * Settings.deltatime)
                self.rect.left = round(self.position.x)
            elif kwargs["action"] == "direction":   # Richtung wechseln§\label{srcInvader06e02}§
                self.change_direction()

    def change_direction(self) -> None:
        self.speed.x *= -1


class Border(pygame.sprite.Sprite):

    def __init__(self, leftright: str) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick01.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (35, Settings.window['height']))
        self.rect = self.image.get_rect()
        if leftright == 'right':
            self.rect.left = Settings.window['width'] - self.rect.width


class Game(object):

    def __init__(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.window_dim())
        pygame.display.set_caption("Sprite")
        self.clock = pygame.time.Clock()
        self.defender = pygame.sprite.GroupSingle(Defender())
        self.all_border = pygame.sprite.Group()
        self.all_border.add(Border('left'))
        self.all_border.add(Border('right'))
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.fps)
            time_current = time()
            Settings.deltatime = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        if pygame.sprite.spritecollide(self.defender.sprite, self.all_border, False):
            self.defender.update(action="direction")  # Besser §\label{srcInvader06e03}§
        self.defender.update(action="newpos")

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.defender.draw(self.screen)
        self.all_border.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
