import os
from time import time
from typing import Any, Dict, Tuple
from random import randint, choice

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 300))
    FPS = 60
    DELTATIME = 1.0/FPS


class Game:

    def __init__(self) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "650, 70"
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Event (0)")
        self._running = True

    def run(self) -> None:
        time_previous = time()
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            print(event)                                    # Eventinfo ausgeben§\label{srcEvents0001}§
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False

    def update(self):
        pass

    def draw(self) -> None:
        self._screen.fill((250, 250, 250))
        pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
