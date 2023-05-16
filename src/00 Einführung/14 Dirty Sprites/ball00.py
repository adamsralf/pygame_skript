import os
from math import atan2, cos, sin
from random import randint
from time import time

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0,0),(600, 600))
    FPS = 30
    DELTATIME = 1.0 / FPS


class Ball(pygame.sprite.DirtySprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.surface.Surface((30, 30)).convert()
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, "blue", (15, 15), 15)
        pygame.draw.rect(self.image, "red", (0, 0, 30, 30), 1)
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.speed = pygame.Vector2(-10, 5)
        self.dirty = 1

    def update(self) -> None:
        self.rect.move_ip(self.speed)
        if self.rect.left < 0 or self.rect.right > Settings.WINDOW.width:
            self.speed.x *= -1
        if self.rect.top < 0 or self.rect.bottom > Settings.WINDOW.height:
            self.speed.y *= -1
        self.dirty = 1

class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        self.background = pygame.surface.Surface(Settings.WINDOW.size)
        self.background.fill("white")
        pygame.display.set_caption("Ball mit DirtySprite")
        self.clock = pygame.time.Clock()
        self.ball = pygame.sprite.LayeredDirty(Ball())
        self.ball.clear(self.screen, self.background)
        self.ball.set_timing_threshold(1000.0/Settings.FPS)
        self.running = True

    def run(self) -> None:
        time_previous = time()
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.ball.update()


    def draw(self) -> None:
        rects = self.ball.draw(self.screen)
        pygame.display.update(rects)


if __name__ == '__main__':
    game = Game()
    game.run()
